# Ensure that the API Server --service-account-key-file argument is set as appropriate (C-0136)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the Control Plane node and set the `--service-account-key-file` parameter to the public key file for service accounts:

```
--service-account-key-file=<filename>

```

**Admission resources**  `pods`.

**Kubescape severity score**  5/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0136-ensurethattheapiserverserviceaccountkeyfileargumentissetasappropriate.json) · [Installing and binding policies](../../README.md#using-the-library)
