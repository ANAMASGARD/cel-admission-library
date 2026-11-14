# Ensure that the API Server --DenyServiceExternalIPs is set (C-0283)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects. C-0115 and C-0283 implement opposite benchmark recommendations for DenyServiceExternalIPs. Bind the applicable profile.

Edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the master node and add the `--enable-admission-plugins=DenyServiceExternalIPs` parameter

 or

 The Kubernetes API server flag disable-admission-plugins takes a comma-delimited list of admission control plugins to be disabled, even if they are in the list of plugins enabled by default.

 `kube-apiserver --disable-admission-plugins=DenyServiceExternalIPs,AlwaysDeny ...`

**Admission resources**  `pods`.

**Kubescape severity score**  4/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0283-ensurethattheapiserverdenyserviceexternalipsisset.json) · [Installing and binding policies](../../README.md#using-the-library)
