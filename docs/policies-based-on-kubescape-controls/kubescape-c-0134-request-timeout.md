# Ensure that the API Server --request-timeout argument is set as appropriate (C-0134)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects. Use a Warn or Audit binding for the required manual review.

Edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` and set the below parameter as appropriate and if needed. For example,

```
--request-timeout=300s

```

**Admission resources**  `pods`.

**Kubescape severity score**  4/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0134-ensurethattheapiserverrequesttimeoutargumentissetasappropriate.json) · [Installing and binding policies](../../README.md#using-the-library)
