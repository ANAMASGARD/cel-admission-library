// Compiled inside the pinned Kubescape opaprocessor test package by run.py.
package opaprocessor

import (
	"context"
	"encoding/json"
	"fmt"
	"maps"
	"os"
	"path/filepath"
	"testing"

	"github.com/kubescape/k8s-interface/workloadinterface"
	"github.com/kubescape/kubescape/v4/core/pkg/opaprocessor/cel"
	"github.com/kubescape/opa-utils/reporthandling"
	"github.com/stretchr/testify/require"
	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
)

type fixture struct {
	Name, Source, Origin, FixtureError string
	CheckExpected, CheckCEL            bool
	Notes                              []string
	Objects, Expected, CELExpected     []map[string]any
	Data                               struct {
		PostureControlInputs map[string][]string
		DataControlInputs    map[string]string
	}
	Params map[string]any
}

type candidate struct {
	ID    string
	Rules []reporthandling.PolicyRule
	Fixed map[string][]string
	Cases []fixture
}

type outcome struct {
	Control  string                   `json:"control"`
	Rule     string                   `json:"rule"`
	Origin   string                   `json:"origin"`
	Case     string                   `json:"case"`
	Mode     string                   `json:"mode"`
	Status   string                   `json:"status"`
	Detail   []string                 `json:"detail,omitempty"`
	Notes    []string                 `json:"normalizations,omitempty"`
	Rego     map[string]parityVerdict `json:"rego,omitempty"`
	CEL      map[string]parityVerdict `json:"cel,omitempty"`
	Expected []string                 `json:"expectedSourceFailures,omitempty"`
}

func (r *outcome) problem(status, detail string) {
	if r.Status == "agree" || status == "unknown" {
		r.Status = status
	}
	r.Detail = append(r.Detail, detail)
}

func checkFixture(t *testing.T, ctrl candidate, f fixture, defaults map[string][]string, mode string) outcome {
	t.Helper()
	row := outcome{Control: ctrl.ID, Rule: f.Source, Case: f.Name, Mode: mode, Origin: f.Origin, Status: "agree", Notes: f.Notes}
	settings := maps.Clone(defaults)
	cloud := ""
	if mode == "fixture" {
		if f.FixtureError != "" {
			row.problem("unknown", f.FixtureError)
			return row
		}
		maps.Copy(settings, f.Data.PostureControlInputs)
		cloud = f.Data.DataControlInputs["cloudProvider"]
	}
	ctx := context.Background()
	source := newParityScanner(t, f.Objects, settings)
	source.Report.ClusterCloudProvider = cloud
	control := reporthandling.Control{ControlID: ctrl.ID, Rules: ctrl.Rules, FixedInput: ctrl.Fixed}
	row.Rego = map[string]parityVerdict{}
	for i := range ctrl.Rules {
		rule := &ctrl.Rules[i]
		found, err := source.processRule(ctx, rule, ctrl.Fixed, evaluationScope{}, &control)
		if err != nil {
			row.problem("unknown", fmt.Sprintf("Rego %s: %v", rule.Name, err))
			return row
		}
		mergeVerdicts(row.Rego, found)
		if rule.Name == f.Source && mode == "fixture" && f.CheckExpected {
			actual := map[string]parityVerdict{}
			mergeVerdicts(actual, found)
			expected := map[string]bool{}
			for _, obj := range f.Expected {
				id := workloadinterface.NewWorkloadObj(obj).GetID()
				expected[id] = true
				row.Expected = append(row.Expected, id)
			}
			for id := range expected {
				if actual[id] != "failed" {
					row.problem("source-mismatch", fmt.Sprintf("expected source finding on %s, got %s", id, verdictOr(actual, id)))
				}
			}
			for id, status := range actual {
				if status == "failed" && !expected[id] {
					row.problem("source-mismatch", "unexpected source finding on "+id)
				}
			}
		}
	}

	// Give the VAP every input kind. Copying only Rego's match blocks would hide
	// a policy which applies more broadly than the Rego rule.
	vap, err := cel.LoadVAP(ctrl.ID)
	if err != nil {
		row.problem("unknown", err.Error())
		return row
	}
	rule := reporthandling.PolicyRule{RuleLanguage: reporthandling.CELLanguage}
	rule.Name = "cel-" + ctrl.ID
	groups := map[string]bool{}
	for _, obj := range f.Objects {
		key := resourceGroupKey(t, obj)
		if !groups[key] {
			wl := workloadinterface.NewWorkloadObj(obj)
			rule.Match = append(rule.Match, reporthandling.RuleMatchObjects{
				APIGroups: []string{wl.GetGroup()}, APIVersions: []string{wl.GetVersion()}, Resources: []string{wl.GetKind()},
			})
			groups[key] = true
		}
	}
	params, err := cel.ResolveParamObject(vap, nil, "", nil)
	require.NoError(t, err)
	objects := f.Objects
	var bindings []unstructured.Unstructured
	if mode == "fixture" && vap.TakesParams() && len(f.Params) > 0 {
		// Deep-copy the bundled defaults; parameter resolution caches that object.
		config := (&unstructured.Unstructured{Object: params.(map[string]any)}).DeepCopy()
		config.SetName("candidate-parity-fixture")
		configSettings := config.Object["settings"].(map[string]any)
		maps.Copy(configSettings, f.Params)
		params = config.Object
		objects = append(append([]map[string]any{}, objects...), config.Object)
		bindings = []unstructured.Unstructured{{Object: map[string]any{"spec": map[string]any{
			"policyName": vap.PolicyName, "paramRef": map[string]any{"name": config.GetName(), "parameterNotFoundAction": "Deny"},
		}}}}
	}
	scanner := newParityScanner(t, objects, settings)
	scanner.VAPBindings = bindings
	celControl := reporthandling.Control{ControlID: ctrl.ID, Rules: []reporthandling.PolicyRule{rule}}
	found, err := scanner.processRule(ctx, &rule, nil, evaluationScope{}, &celControl)
	if err != nil {
		row.problem("unknown", "CEL: "+err.Error())
		return row
	}
	row.CEL = map[string]parityVerdict{}
	mergeVerdicts(row.CEL, found)
	if mode == "fixture" && f.CheckCEL {
		denied := map[string]bool{}
		for _, obj := range f.CELExpected {
			denied[workloadinterface.NewWorkloadObj(obj).GetID()] = true
		}
		for _, obj := range f.Objects {
			id := workloadinterface.NewWorkloadObj(obj).GetID()
			want := parityVerdict("passed")
			if denied[id] {
				want = "failed"
			}
			if verdictOr(row.CEL, id) != want {
				row.problem("cel-mismatch", fmt.Sprintf("authored CEL expectation on %s: expected %s, got %s", id, want, verdictOr(row.CEL, id)))
			}
		}
	}
	// Under failurePolicy: Fail an expression error can look identical to a
	// genuine denial in processRule's status. Inspect the evaluator diagnostics.
	evaluator, err := scanner.getCELEvaluator()
	require.NoError(t, err)
	for _, obj := range f.Objects {
		id := workloadinterface.NewWorkloadObj(obj).GetID()
		evaluation, err := evaluator.EvaluateVAP(ctx, vap, obj, scanner.celNamespaceObjectFor(obj), params)
		if err != nil {
			row.problem("unknown", id+": "+err.Error())
			continue
		}
		for _, v := range evaluation.Results {
			if v.Err != nil {
				row.problem("unknown", id+": "+v.Err.Error())
			}
		}
	}
	for _, side := range []map[string]parityVerdict{row.Rego, row.CEL} {
		for id, verdict := range side {
			if verdict != "passed" && verdict != "failed" {
				row.problem("unknown", fmt.Sprintf("%s: %s", id, verdict))
			}
		}
	}
	for _, diff := range compareVerdicts(row.Rego, row.CEL) {
		row.problem("disagree", diff)
	}
	if len(row.Rego) == 0 && len(row.CEL) == 0 {
		row.problem("uncovered", "neither engine evaluated a resource")
	}
	return row
}

func TestCandidateParity(t *testing.T) {
	dir := os.Getenv("PARITY_WORK")
	raw, err := os.ReadFile(filepath.Join(dir, "cases.json"))
	require.NoError(t, err)
	var plan struct {
		Defaults map[string][]string
		Controls []candidate
	}
	require.NoError(t, json.Unmarshal(raw, &plan))
	out, err := os.Create(filepath.Join(dir, "outcomes.jsonl"))
	require.NoError(t, err)
	defer out.Close()
	encoder := json.NewEncoder(out)
	for _, ctrl := range plan.Controls {
		for _, f := range ctrl.Cases {
			for _, mode := range []string{"default", "fixture"} {
				row := checkFixture(t, ctrl, f, plan.Defaults, mode)
				require.NoError(t, encoder.Encode(row))
			}
		}
	}
}
