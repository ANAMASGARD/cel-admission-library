#!/usr/bin/env python3
"""Render all public policy assets and record the exact coverage of each API."""

import argparse
import hashlib
import re
import shutil
import subprocess
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "kubescape-validating-admission-policies"
OVERLAYS = {
    "v1": ("k8s-v1", "admissionregistration.k8s.io/v1"),
    "v1beta1": ("k8s-v1beta1", "admissionregistration.k8s.io/v1beta1"),
    "v1alpha1": ("k8s-v1alpha1", "admissionregistration.k8s.io/v1alpha1"),
    "x-v1alpha1": ("x-k8s-v1alpha1", "admissionregistration.x-k8s.io/v1alpha1"),
}


def source_policies():
    policies = {}
    ids = set()
    for path in sorted([*ROOT.glob("controls/*/policy.yaml"), *ROOT.glob("runtime-policies/*/policy.yaml")]):
        policy = yaml.safe_load(path.read_text())
        name = policy["metadata"]["name"]
        control_id = policy["metadata"].get("labels", {}).get("controlId")
        if path.parent.parent.name == "controls":
            if control_id != path.parent.name or not re.fullmatch(r"C-\d{4}", control_id) or control_id in ids:
                raise ValueError(f"Invalid or duplicate control ID in {path}")
            ids.add(control_id)
        if name in policies:
            raise ValueError(f"Duplicate policy name {name} in {path}")
        policies[name] = policy
    if not ids:
        raise ValueError("No control policies found")
    return policies


def render(directory, api_version, source, stable=None):
    content = subprocess.check_output(["kubectl", "kustomize", str(directory)])
    rendered = {}
    for policy in yaml.safe_load_all(content):
        name = policy["metadata"]["name"]
        if policy["kind"] != "ValidatingAdmissionPolicy" or policy["apiVersion"] != api_version:
            raise ValueError(f"{directory.name} contains an unexpected kind or API version for {name}")
        if name in rendered or name not in source:
            raise ValueError(f"{directory.name} contains an unexpected or duplicate policy {name}")
        if policy["metadata"].get("labels", {}).get("controlId") != source[name]["metadata"].get("labels", {}).get("controlId"):
            raise ValueError(f"{directory.name} changes the control ID of {name}")
        if stable is not None and policy != dict(stable[name], apiVersion=api_version):
            raise ValueError(f"{directory.name} changes the source policy {name}")
        rendered[name] = policy
    if not rendered or (stable is None and rendered.keys() != source.keys()):
        raise ValueError(f"{directory.name} has an empty or incomplete catalog")
    return content, rendered


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    source = source_policies()
    assets = []
    coverage = {}
    stable = None
    for suffix, (overlay, api_version) in OVERLAYS.items():
        content, rendered = render(ROOT / "apis" / overlay, api_version, source, stable)
        if suffix == "v1":
            stable = rendered
        coverage[suffix] = set(rendered)
        artifact = output / f"{PREFIX}-{suffix}.yaml"
        artifact.write_bytes(content)
        assets.append(artifact)

    if coverage["x-v1alpha1"] != coverage["v1alpha1"]:
        raise ValueError("The webhook and native alpha subsets must contain the same policies")

    default = output / f"{PREFIX}.yaml"
    shutil.copyfile(assets[0], default)
    assets.append(default)
    for config in ["policy-configuration-definition.yaml", "basic-control-configuration.yaml"]:
        assets.append(output / config)
        shutil.copyfile(ROOT / "configuration" / config, assets[-1])

    rows = [
        "# Policy coverage by release artifact",
        "",
        "The default YAML is identical to the v1 artifact. A dash marks a policy omitted from that artifact.",
        "",
        "| Control | Policy | " + " | ".join(OVERLAYS) + " |",
        "| --- | --- | " + " | ".join("---" for _ in OVERLAYS) + " |",
    ]
    for name, policy in sorted(source.items()):
        control_id = policy["metadata"].get("labels", {}).get("controlId", "runtime")
        columns = [control_id, name] + ["yes" if name in names else "—" for names in coverage.values()]
        rows.append("| " + " | ".join(columns) + " |")
    manifest = output / "policy-coverage.md"
    manifest.write_text("\n".join(rows) + "\n")
    assets.append(manifest)
    checksums = [f"{hashlib.sha256(asset.read_bytes()).hexdigest()}  {asset.name}" for asset in assets]
    (output / "SHA256SUMS").write_text("\n".join(checksums) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    build(parser.parse_args().output)
