# Ensure that the admission control plugin ServiceAccount is set (C-0125)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Follow the documentation and create `ServiceAccount` objects as per your environment. Then, edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the master node and ensure that the `--disable-admission-plugins` parameter is set to a value that does not include `ServiceAccount`.

**Admission resources**  `pods`.

**Kubescape severity score**  3/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0125-ensurethattheadmissioncontrolpluginserviceaccountisset.json) · [Installing and binding policies](../../README.md#using-the-library)
