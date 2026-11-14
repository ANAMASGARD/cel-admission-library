"""Exercise one control on a disposable Kubernetes cluster with server dry-runs."""
import argparse
from contextlib import ExitStack
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import yaml


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "test-resources"


def kubectl(*args, **kwargs):
    return subprocess.run(["kubectl", *args], check=True, text=True, **kwargs)


def create_owned(stack, manifest):
    # create fails on collision. Only register cleanup after we created the object.
    kubectl("create", "-f", str(manifest))
    stack.callback(kubectl, "delete", "--ignore-not-found", "-f", str(manifest))


def render(template, dest, changes):
    if changes:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/change-yaml-field.py"),
             "-i", str(template), "-o", str(dest), *changes], check=True,
        )
    else:
        dest.write_bytes(template.read_bytes())


def verdict(expected, proc, policy_name):
    diagnostic = proc.stderr
    named = policy_name in diagnostic
    error = any(marker in diagnostic.lower() for marker in (
        "failed to evaluate", "evaluation error", "resulted in error",
        "no such key", "compilation failed", "exceeds budget",
    ))
    if error:
        return False
    if expected == "pass":
        return proc.returncode == 0 and not named
    if expected == "warn":
        return proc.returncode == 0 and any(
            "Warning:" in line and policy_name in line for line in diagnostic.splitlines()
        )
    if expected == "fail":
        return proc.returncode != 0 and named and "denied request" in diagnostic
    raise ValueError(f"Unknown expected result {expected!r}")


def run_case(test, policy_name, directory):
    obj = directory / "object.yaml"
    params = directory / "params.yaml"
    binding = directory / "binding.yaml"
    render(FIXTURES / test["template"], obj, test.get("field_change_list", []))
    render(FIXTURES / test.get("param_template", "default-control-configuration.yaml"),
           params, ["metadata.name=" + policy_name + "-params"])
    changes = ["metadata.name=" + policy_name + "-binding", "spec.policyName=" + policy_name]
    if not test.get("omit_param_ref"):
        changes.append("spec.paramRef.name=" + policy_name + "-params")
    render(FIXTURES / test.get("binding_template", "policy-binding.yaml"), binding, changes)
    labels = yaml.safe_load(obj.read_text())["metadata"].get("labels", {})
    selector = yaml.safe_load(binding.read_text())["spec"]["matchResources"]["objectSelector"]
    if not all(labels.get(k) == v for k, v in selector["matchLabels"].items()):
        raise ValueError(f"{test['name']}: binding does not select the fixture")
    with ExitStack() as stack:
        subresource = test.get("subresource")
        if subresource:
            if subresource != "status":
                raise ValueError(f"Unsupported subresource {subresource}")
            base = directory / "base.yaml"
            document = yaml.safe_load(obj.read_text())
            status = document.pop("status")
            base.write_text(yaml.safe_dump(document))
            create_owned(stack, base)
        create_owned(stack, params)
        create_owned(stack, binding)
        # Admission configuration is propagated asynchronously.
        time.sleep(1)
        command = ["kubectl", "apply", "--dry-run=server", "-f", str(obj)]
        if subresource:
            command = ["kubectl", "patch", "--subresource=status", "--dry-run=server",
                       "--type=merge", "-f", str(base), "-p", json.dumps({"status": status})]
        proc = subprocess.run(command,
                              capture_output=True, text=True)
        if not verdict(test["expected"], proc, policy_name):
            print(f"{test['name']}: expected {test['expected']}, exit {proc.returncode}\n"
                  f"{proc.stderr}", file=sys.stderr)
            return False
        print(f"{test['name']}: {test['expected']}")
        return True


def run(directory):
    policy = Path("policy.yaml")
    name = yaml.safe_load(policy.read_text())["metadata"]["name"]
    with ExitStack() as stack:
        kubectl("create", "namespace", "test-namespace")
        stack.callback(kubectl, "delete", "namespace", "test-namespace")
        crd = ROOT / "configuration/policy-configuration-definition.yaml"
        existing = kubectl("get", "-f", str(crd), "--ignore-not-found", "-o", "name",
                           capture_output=True).stdout.strip()
        if not existing:
            create_owned(stack, crd)
        kubectl("wait", "--for=condition=Established", "-f", str(crd), "--timeout=60s")
        create_owned(stack, policy)
        outcomes = [run_case(test, name, directory) for test in json.loads(Path("tests.json").read_text())]
        return all(outcomes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-d", "--dont-cleanup", action="store_true",
                        help="keep the generated manifests of the last case")
    args = parser.parse_args()
    if args.dont_cleanup:
        directory = Path(tempfile.mkdtemp())
        print(f"Generated manifests: {directory}", flush=True)
        sys.exit(0 if run(directory) else 1)
    with tempfile.TemporaryDirectory() as temp:
        sys.exit(0 if run(Path(temp)) else 1)
