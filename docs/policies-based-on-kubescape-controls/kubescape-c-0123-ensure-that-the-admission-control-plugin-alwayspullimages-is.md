# Ensure that the admission control plugin AlwaysPullImages is set (C-0123)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the Control Plane node and set the `--enable-admission-plugins` parameter to include `AlwaysPullImages`.

```
--enable-admission-plugins=...,AlwaysPullImages,...

```

**Admission resources**  `pods`.

**Kubescape severity score**  4/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0123-ensurethattheadmissioncontrolpluginalwayspullimagesisset.json) · [Installing and binding policies](../../README.md#using-the-library)
