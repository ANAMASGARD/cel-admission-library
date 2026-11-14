# Ensure that the admission control plugin NodeRestriction is set (C-0127)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Follow the Kubernetes documentation and configure `NodeRestriction` plug-in on kubelets. Then, edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the master node and set the `--enable-admission-plugins` parameter to a value that includes `NodeRestriction`.

```
--enable-admission-plugins=...,NodeRestriction,...

```

**Admission resources**  `pods`.

**Kubescape severity score**  4/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0127-ensurethattheadmissioncontrolpluginnoderestrictionisset.json) · [Installing and binding policies](../../README.md#using-the-library)
