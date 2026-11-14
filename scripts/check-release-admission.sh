#!/usr/bin/env bash
# Run against a disposable cluster serving the requested API.
set -euo pipefail
release_dir=${1:?supply the rendered artifact directory}
suffix=${2:?supply the artifact suffix}
case "$suffix" in
  v1|v1beta1|v1alpha1) api="admissionregistration.k8s.io/$suffix" ;;
  x-v1alpha1) api=admissionregistration.x-k8s.io/v1alpha1 ;;
  *) echo "Unknown release API $suffix" >&2; exit 1 ;;
esac
name=kubescape-c-0041-deny-resources-with-host-network-access
namespace=release-policy-probe
kubectl apply -f "$release_dir/policy-configuration-definition.yaml"
kubectl wait --for=condition=Established --timeout=60s crd/controlconfigurations.kubescape.io
kubectl apply -f "$release_dir/basic-control-configuration.yaml"
kubectl apply --server-side --validate=strict -f "$release_dir/kubescape-validating-admission-policies-$suffix.yaml"
kubectl create namespace "$namespace"
kubectl create -f - <<YAML
apiVersion: $api
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: release-host-network-probe
spec:
  policyName: $name
  validationActions: [Deny]
  matchResources:
    namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: $namespace
YAML
probe() {
  kubectl -n "$namespace" run release-test --image=registry.k8s.io/pause:3.10 \
    --restart=Never --dry-run=server --overrides="{\"spec\":{\"hostNetwork\":$1}}"
}
# The apiserver and the webhook observe a new binding asynchronously.
for attempt in {1..30}; do
  if ! output=$(probe true 2>&1) && [[ "$output" == *"$name"*"release-host-network-probe"*"denied request"*"hostNetwork"* ]]; then
    probe false
    exit 0
  fi
  sleep 1
done
echo "Expected the host-network policy to deny the matching Pod. Last response was $output" >&2
exit 1
