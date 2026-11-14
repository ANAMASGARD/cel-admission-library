# Ensure that the admission control plugin EventRateLimit is set (C-0121)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Follow the Kubernetes documentation and set the desired limits in a configuration file.

 Then, edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` and set the below parameters.

```
--enable-admission-plugins=...,EventRateLimit,...
--admission-control-config-file=<path/to/configuration/file>

```

**Admission resources**  `pods`.

**Kubescape severity score**  4/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0121-ensurethattheadmissioncontrolplugineventratelimitisset.json) · [Installing and binding policies](../../README.md#using-the-library)
