# Ensure that the API Server --authorization-mode argument includes Node (C-0119)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the Control Plane node and set the `--authorization-mode` parameter to a value that includes `Node`.

```
--authorization-mode=Node,RBAC

```

**Admission resources**  `pods`.

**Kubescape severity score**  5/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0119-ensurethattheapiserverauthorizationmodeargumentincludesnode.json) · [Installing and binding policies](../../README.md#using-the-library)
