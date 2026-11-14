# Ensure that a minimal audit policy is created (C-0160)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Create an audit policy file for your cluster.

**Admission resources**  `pods`.

**Kubescape severity score**  5/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0160-ensurethataminimalauditpolicyiscreated.json) · [Installing and binding policies](../../README.md#using-the-library)
