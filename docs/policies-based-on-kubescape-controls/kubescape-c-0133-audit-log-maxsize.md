# Ensure that the API Server --audit-log-maxsize argument is set to 100 or as appropriate (C-0133)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects. Use a Warn or Audit binding for the required manual review.

Edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the Control Plane node and set the `--audit-log-maxsize` parameter to an appropriate size in MB. For example, to set it as 100 MB:

```
--audit-log-maxsize=100

```

**Admission resources**  `pods`.

**Kubescape severity score**  4/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0133-ensurethattheapiserverauditlogmaxsizeargumentissetto100orasappropriate.json) · [Installing and binding policies](../../README.md#using-the-library)
