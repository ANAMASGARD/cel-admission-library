# Prefer using dedicated AKS Service Accounts (C-0239)

The AKS benchmark checks direct ServiceAccount subjects named default and exempts bindings carrying the Kubernetes bootstrap label. Bind this policy in the AKS profile. The label exemption follows the source rule and is not authentication of the caller.

**Admission resources**  `rolebindings`, `clusterrolebindings`.

**Kubescape severity score**  7/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0239-preferusingdedicatedaksserviceaccounts.json) · [Installing and binding policies](../../README.md#using-the-library)
