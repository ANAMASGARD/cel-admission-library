# API server insecure port is enabled (C-0005)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Set the insecure-port flag of the API server to zero.

**Admission resources**  `pods`.

**Kubescape severity score**  9/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0005-apiserverinsecureportisenabled.json) · [Installing and binding policies](../../README.md#using-the-library)
