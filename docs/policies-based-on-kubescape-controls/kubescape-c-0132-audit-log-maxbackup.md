# Ensure that the API Server --audit-log-maxbackup argument is set to 10 or as appropriate (C-0132)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects. Use a Warn or Audit binding for the required manual review.

Edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the Control Plane node and set the `--audit-log-maxbackup` parameter to 10 or to an appropriate value.

```
--audit-log-maxbackup=10

```

**Admission resources**  `pods`.

**Kubescape severity score**  4/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0132-ensurethattheapiserverauditlogmaxbackupargumentissetto10orasappropriate.json) · [Installing and binding policies](../../README.md#using-the-library)
