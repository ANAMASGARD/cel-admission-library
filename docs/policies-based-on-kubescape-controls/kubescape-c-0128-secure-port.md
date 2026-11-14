# Ensure that the API Server --secure-port argument is not set to 0 (C-0128)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the Control Plane node and either remove the `--secure-port` parameter or set it to a different (non-zero) desired port.

**Admission resources**  `pods`.

**Kubescape severity score**  8/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0128-ensurethattheapiserversecureportargumentisnotsetto0.json) · [Installing and binding policies](../../README.md#using-the-library)
