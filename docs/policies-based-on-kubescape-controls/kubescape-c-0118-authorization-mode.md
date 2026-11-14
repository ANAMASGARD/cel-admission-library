# Ensure that the API Server --authorization-mode argument is not set to AlwaysAllow (C-0118)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the Control Plane node and set the `--authorization-mode` parameter to values other than `AlwaysAllow`. One such example could be as below.

```
--authorization-mode=RBAC

```

**Admission resources**  `pods`.

**Kubescape severity score**  7/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0118-ensurethattheapiserverauthorizationmodeargumentisnotsettoalwaysallow.json) · [Installing and binding policies](../../README.md#using-the-library)
