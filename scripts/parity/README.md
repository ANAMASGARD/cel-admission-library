# Rego and CEL fixture parity

From the repository root, run a control or omit its ID to check every control in the rendered bundle.

```sh
python3 scripts/parity/run.py C-0013 --report /tmp/c-0013.json
python3 scripts/parity/run.py --report /tmp/control-parity.json
```

Install Python 3.12+, PyYAML, kubectl (with Kustomize), and Go with the Kubescape module's toolchain (1.27.4). The first run downloads two pinned source archives and Go dependencies. The scanner is large. Use `--cache /path/on/disk` to choose a directory with space for archives, sources, and temporary build files. Go uses its normal module and build caches. This command runs offline evaluations after the downloads and needs no Kubernetes cluster.

The runner checks the archive SHA-256 digests, extracts fresh copies, and renders this checkout with `kubectl kustomize apis/k8s-v1`. It embeds the rendered policies, configuration and CRD in that temporary Kubescape tree. Both implementations run through the pinned scanner's `processRule`, including pass inference, resource matching and aggregation. The runner uses `rulesNames` from the control metadata, resolves rules by the name in their metadata, and honors the pinned v4 scanner's version gates. This includes controls with multiple rules.

Each upstream input case runs twice. In `default` mode Rego reads its shipped defaults and CEL reads the candidate bundle's defaults. In `fixture` mode the source's `data.json` overrides Rego settings and supplies the equivalent CEL `ControlConfiguration` through a binding. The runner converts quantity and array fields to the parameter CRD's representation. It compares the fixture's `expected.json` failure subjects against its originating Rego rule and compares both engines' verdicts at the whole-control level. The report includes source mismatches, engine disagreements, uncovered cases and unknowns. A case in which neither engine evaluated an object does not demonstrate coverage. The runner reports CEL evaluation errors separately, including errors that would deny admission under `failurePolicy: Fail`.

The JSON report records the inputs' source, rule and case, configuration mode, per-resource verdicts, and the rendered policy digest. The exit code is zero when every selected comparison agrees. A build error, missing fixture, unresolvable expectation or different verdict produces a nonzero exit. `expectedSourceFailures` contains resource IDs. The comparison does not test path-by-path remediation, findings multiplicity, admission webhook behavior, or enforcement actions. Run the library's server-side admission tests for the last two.

Sources are pinned in [run.py](run.py). [Kubescape scanner harness](https://github.com/kubescape/kubescape/blob/fc41d73e9d5399120283ea19c54af8801546a8e4/core/pkg/opaprocessor/processorhandler_regocelparity_test.go) · [Rego control and fixture sources](https://github.com/kubescape/regolibrary/tree/b7e57060ca90c41fe15359383245a7c62f09487c)

## Fixture handling

The runner preserves all objects from a case, including multi-document YAML. It upgrades removed CronJob and CSIStorageCapacity API versions, fixes a tab before a comment in a Role, and distinguishes same-name fixture variants in the known AppArmor and AWS Service cases. Component-flag cases that use the same resource identity for multiple alternative Pods run each variant in isolation. A stripped namespace is recovered from the inputs only when the expected subject has exactly one match. Ambiguous upstream subjects and other unsupported cases appear in the report.

Additional cases belong in `scripts/parity/fixtures/<rule metadata name>/<case>/`. Use either `input.yaml` or `input/` containing manifests, and the upstream `expected.json` format. Add an optional `data.json` for settings. Prefixes such as `apps/v1` and namespaces in the expected subject should match the input. An empty array means the source rule should produce no findings. The report labels these fixtures `authored` and continues to flag rules without any upstream fixtures.

For an intentional policy difference on a set of applicable resources, supply an extra `cel-expected.json` in the same finding-subject format. The fixture-mode report checks this assertion independently. A source-versus-CEL difference still appears as a disagreement.
