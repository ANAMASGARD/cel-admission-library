# Ensure that the API Server --service-account-lookup argument is set to true (C-0135)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the Control Plane node and set the below parameter.

```
--service-account-lookup=true

```
 Alternatively, you can delete the `--service-account-lookup` parameter from this file so that the default takes effect.

**Admission resources**  `pods`.

**Kubescape severity score**  6/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0135-ensurethattheapiserverserviceaccountlookupargumentissettotrue.json) · [Installing and binding policies](../../README.md#using-the-library)
