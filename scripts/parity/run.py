#!/usr/bin/env python3
"""Compare this checkout's release bundle with pinned Kubescape and Rego fixtures."""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PINS = {
    "kubescape": "fc41d73e9d5399120283ea19c54af8801546a8e4",
    "regolibrary": "b7e57060ca90c41fe15359383245a7c62f09487c",
}
ARCHIVE_SHA256 = {
    "kubescape": "4242c68ef2eb3db0a49b12d634ba58333a49498b820eda44010c56b55d09d7fb",
    "regolibrary": "36b77587cf73ccfe987e4bfd8c2b613845d0c8b9132ff233c8c48219d1eaf67c",
}
SCANNER_VERSION = (4, 0, 21)


def source(repo, cache, work):
    commit = PINS[repo]
    cache.mkdir(parents=True, exist_ok=True)
    archive = cache / f"{repo}-{commit}.tar.gz"
    if not archive.exists():
        url = f"https://codeload.github.com/kubescape/{repo}/tar.gz/{commit}"
        with tempfile.NamedTemporaryFile(dir=cache, delete=False) as temp:
            try:
                with urllib.request.urlopen(url, timeout=120) as response:
                    shutil.copyfileobj(response, temp)
                temp.close()
                with tarfile.open(temp.name) as tar:
                    tar.getmembers()  # Refuse a truncated download before caching.
                os.replace(temp.name, archive)
            finally:
                Path(temp.name).unlink(missing_ok=True)
    with archive.open("rb") as handle:
        if hashlib.file_digest(handle, "sha256").hexdigest() != ARCHIVE_SHA256[repo]:
            raise ValueError(f"wrong SHA256 for {archive}. Remove it and retry the download.")
    with tarfile.open(archive) as tar:
        tar.extractall(work, filter="data")
    return work / f"{repo}-{commit}"


def read_json(path):
    return json.loads(path.read_text())


def object_id(obj):
    meta = obj.get("metadata", {})
    return (obj["apiVersion"], obj["kind"], meta.get("namespace", ""), meta["name"])


def normalize(obj):
    served = {("CronJob", "batch/v1beta1"): "batch/v1",
              ("CSIStorageCapacity", "storage.k8s.io/v1beta1"): "storage.k8s.io/v1"}
    key = obj["kind"], obj["apiVersion"]
    if key in served:
        obj["apiVersion"] = served[key]
        return True
    return False


def objects_for(case, rule):
    if (case / "input").is_dir():
        paths = sorted((case / "input").iterdir())
    else:
        paths = [p for p in [case / "input.yaml", case / "input.json"] if p.exists()]
        if not paths:
            # Some Rego fixtures store the manifest directly as deployment1.yaml.
            paths = sorted(case.glob("*.yaml")) + sorted(case.glob("*.yml"))
    objects, notes = [], set()
    for p in paths:
        raw = p.read_text()
        if rule == "role-in-default-namespace" and p.name == "role.yaml":
            raw = raw.replace(']\t  #', ']   #')
        for index, obj in enumerate(yaml.safe_load_all(raw)):
            if obj is None:
                continue
            if normalize(obj):
                notes.add("removed API version upgraded")
            if (rule, case.name, p.name) == (
                    "ensure-https-loadbalancers-encrypted-with-tls-aws",
                    "failed_multiple_loadbalancers", "loadbalancer_success.yaml"):
                obj["metadata"]["name"] = "api-tls"
                notes.add("duplicate passing Service renamed")
            if rule == "linux-hardening" and case.name == "passed" and index:
                obj["metadata"]["name"] += f"-variant-{index}"
                notes.add("same-name documents distinguished")
            objects.append(obj)
    if not objects:
        raise ValueError("no input manifests")
    return objects, sorted(notes)


def matches_subset(expected, actual):
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and matches_subset(value, actual[key]) for key, value in expected.items()
        )
    if isinstance(expected, list):
        return isinstance(actual, list) and len(actual) == len(expected) and all(
            matches_subset(e, a) for e, a in zip(expected, actual)
        )
    return expected == actual


def expected_objects(path, objects):
    # The source test runner strips namespaces from many expected objects.
    # Recover a missing namespace only when the original input is unambiguous.
    expected = []
    for finding in read_json(path):
        alert = finding["alertObject"]
        subjects = next((v for k, v in alert.items() if k.lower() == "k8sapiobjects"), None)
        if subjects is None:
            subjects = [alert["externalObjects"]]
        for subject in subjects:
            if not isinstance(subject, dict) or "metadata" not in subject:
                raise ValueError("expected finding has an aggregated external subject")
            normalize(subject)
            version, kind, ns, name = object_id(subject)
            matches = [o for o in objects if object_id(o)[:2] == (version, kind)
                       and object_id(o)[3] == name and (not ns or object_id(o)[2] == ns)]
            if len(matches) > 1:
                # Use the source fixture's retained fields (including spec when
                # provided), without consulting either engine's answer.
                matches = [o for o in matches if matches_subset(subject, o)]
            if len(matches) != 1:
                raise ValueError(f"expected subject {(version, kind, ns, name)} has {len(matches)} matches")
            expected.append(matches[0])
    return expected


def version(text):
    return tuple(map(int, text.lstrip("v").split(".")))


def active_rules(rego):
    rules = {}
    for p in sorted((rego / "rules").glob("*/rule.metadata.json")):
        rule = read_json(p)
        attrs = rule.get("attributes") or {}
        if "useUntilKubescapeVersion" in attrs and version(attrs["useUntilKubescapeVersion"]) <= SCANNER_VERSION:
            continue
        if "useFromKubescapeVersion" in attrs and version(attrs["useFromKubescapeVersion"]) > SCANNER_VERSION:
            continue
        rule["rule"] = (p.parent / "raw.rego").read_text()
        if (p.parent / "filter.rego").exists():
            rule["resourceEnumerator"] = (p.parent / "filter.rego").read_text()
        if rule["name"] in rules:
            raise ValueError(f"ambiguous active rule {rule['name']}")
        rules[rule["name"]] = (rule, p.parent)
    return rules


def param_overrides(control, data, schema):
    params = {}
    for key, values in data.get("postureControlInputs", {}).items():
        chunks = key.split("_")
        name = chunks[0] + "".join(s.capitalize() for s in chunks[1:])
        if control == "C-0317" and key in {"cpu_limit_max", "memory_limit_max"}:
            name = "worker" + name[0].upper() + name[1:]
        prop = schema.get(name)
        if not prop:
            raise ValueError(f"no ControlConfiguration field for {key}")
        if prop["type"] == "array":
            params[name] = values
            continue
        if len(values) != 1:
            raise ValueError(f"{key} cannot map to scalar {name}")
        value = values[0]
        if prop["type"] == "number":
            # The CRD accepts CPU cores as a number, while Rego takes quantities.
            if value.endswith("m"):
                value = float(value[:-1]) / 1000
            else:
                value = float(value)
        elif prop["type"] != "string":
            raise ValueError(f"unsupported field type for {name}")
        params[name] = value
    for key, value in data.get("dataControlInputs", {}).items():
        if key != "cloudProvider":
            raise ValueError(f"unsupported dataControlInputs.{key}")
        params[key] = value
    return params


def prepare(rego, selected, schema):
    rules = active_rules(rego)
    controls = {c["controlID"]: c for c in map(read_json, (rego / "controls").glob("*.json"))}
    plan = []
    issues = []
    for cid in selected:
        if cid not in controls:
            issues.append(dict(control=cid, status="unknown", detail="no upstream control"))
            continue
        ctrl = controls[cid]
        resolved = [rules[name] for name in ctrl["rulesNames"] if name in rules]
        cases = []
        for rule, directory in resolved:
            upstream = sorted(p for p in (directory / "test").glob("*") if p.is_dir())
            authored = sorted(p for p in (HERE / "fixtures" / rule["name"]).glob("*") if p.is_dir())
            if not upstream:
                issues.append(dict(control=cid, rule=rule["name"], status="unknown", detail="no upstream fixture"))
            for p in upstream + authored:
                origin = "upstream" if p in upstream else "authored"
                info = dict(control=cid, rule=rule["name"], case=p.name, origin=origin)
                try:
                    objects, notes = objects_for(p, directory.name)
                    data = read_json(p / "data.json") if (p / "data.json").exists() else {}
                    case = dict(name=p.name, source=rule["name"], origin=origin, notes=notes, data=data)
                    try:
                        case["params"] = param_overrides(cid, data, schema)
                        if set(data) - {"postureControlInputs", "dataControlInputs"}:
                            raise ValueError("unsupported fixture inputs")
                    except (KeyError, TypeError, ValueError) as exc:
                        case["fixtureError"] = str(exc)
                    try:
                        expected = expected_objects(p / "expected.json", objects)
                    except (KeyError, TypeError, ValueError, OSError) as exc:
                        issues.append(dict(**info, status="unknown", detail=f"source expectation: {exc}"))
                        expected = None
                    cel_expected = None
                    if (p / "cel-expected.json").exists():
                        cel_expected = expected_objects(p / "cel-expected.json", objects)
                    batches = [objects]
                    if len({object_id(o) for o in objects}) != len(objects):
                        # These control-plane rules independently inspect a single
                        # component's command/args. Never split a correlation rule.
                        if not (len(resolved) == 1 and len(rule["match"]) == 1
                                and rule["match"][0]["resources"] == ["Pod"]
                                and not rule.get("dynamicMatch")
                                and ("kube-apiserver" in rule["rule"] or "kubelet" in rule["rule"]
                                     or "kube-controller-manager" in rule["rule"] or "kube-scheduler" in rule["rule"])):
                            raise ValueError("duplicate resource identity in a potentially correlated case")
                        notes.append("duplicate identities evaluated in separate input batches")
                        batches = [[obj] for obj in objects]
                    for i, batch in enumerate(batches, 1):
                        name = p.name if len(batches) == 1 else f"{p.name}/variant-{i}"
                        cases.append(dict(case, name=name, objects=batch, checkExpected=expected is not None,
                                          expected=[o for o in (expected or []) if o in batch],
                                          checkCEL=cel_expected is not None,
                                          celExpected=[o for o in (cel_expected or []) if o in batch]))
                except (KeyError, TypeError, ValueError, OSError, yaml.YAMLError) as exc:
                    issues.append(dict(**info, status="unknown", detail=str(exc)))
        if not resolved:
            issues.append(dict(control=cid, status="unknown", detail="no active source rules"))
        plan.append(dict(id=cid, rules=[r for r, _ in resolved], fixed=ctrl.get("fixedInput", {}), cases=cases))
    return plan, issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("control", nargs="*", help="control IDs (defaults to the rendered bundle)")
    parser.add_argument("--cache", type=Path, default=Path.home() / ".cache/cel-admission-parity")
    parser.add_argument("--report", type=Path, help="save per-case outcomes as JSON")
    args = parser.parse_args()
    args.cache = args.cache.resolve()
    args.cache.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.cache) as tmp:
        work = Path(tmp)
        ks = source("kubescape", args.cache, work)
        rego = source("regolibrary", args.cache, work)
        bundle = subprocess.check_output(["kubectl", "kustomize", str(ROOT / "apis/k8s-v1")])
        bundled = {doc["metadata"]["labels"]["controlId"] for doc in yaml.safe_load_all(bundle)
                   if doc and doc["metadata"].get("labels", {}).get("controlId")}
        selected = sorted(set(args.control) or bundled)
        if set(selected) - bundled:
            parser.error(f"controls missing from the rendered bundle: {sorted(set(selected) - bundled)}")
        vapdata = ks / "core/pkg/opaprocessor/cel/vapdata"
        (vapdata / "kubescape-validating-admission-policies.yaml").write_bytes(bundle)
        for filename in ["basic-control-configuration.yaml", "policy-configuration-definition.yaml"]:
            shutil.copyfile(ROOT / "configuration" / filename, vapdata / filename)
        crd = yaml.safe_load((vapdata / "policy-configuration-definition.yaml").read_text())
        props = crd["spec"]["versions"][0]["schema"]["openAPIV3Schema"]["properties"]["settings"]["properties"]
        controls, rows = prepare(rego, selected, props)
        defaults = read_json(rego / "default-config-inputs.json")["settings"]["postureControlInputs"]
        spec = dict(controls=controls, defaults=defaults)
        (work / "cases.json").write_text(json.dumps(spec))
        shutil.copyfile(HERE / "candidate_test.go", ks / "core/pkg/opaprocessor/candidate_test.go")
        env = dict(os.environ, PARITY_WORK=str(work))
        env.setdefault("GOTMPDIR", str(work))
        result = subprocess.run(["go", "test", "-count=1", "-p=3", "-ldflags=-s -w", "-timeout=30m",
                                 "-run=^TestCandidateParity$", "./core/pkg/opaprocessor"], cwd=ks, env=env)
        if result.returncode:
            return result.returncode
        with (work / "outcomes.jsonl").open() as f:
            rows.extend(json.loads(line) for line in f)
        digest = hashlib.sha256(bundle).hexdigest()
        report = dict(sources=PINS, policyBundleSHA256=digest, controls=selected, outcomes=rows)
        if args.report:
            args.report.write_text(json.dumps(report, indent=2) + "\n")
        for cid in selected:
            counts = collections.Counter(r["status"] for r in rows if r["control"] == cid)
            print(cid, " ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        return int(any(row["status"] != "agree" for row in rows) or not rows)


if __name__ == "__main__":
    sys.exit(main())
