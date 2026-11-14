# Ensure that the Controller Manager --root-ca-file argument is set as appropriate (C-0148)

Evaluates the kube-controller-manager Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the Controller Manager pod specification file `/etc/kubernetes/manifests/kube-controller-manager.yaml` on the Control Plane node and set the `--root-ca-file` parameter to the certificate bundle file`.

```
--root-ca-file=<path/to/file>

```

**Admission resources**  `pods`.

**Kubescape severity score**  7/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0148-ensurethatthecontrollermanagerrootcafileargumentissetasappropriate.json) · [Installing and binding policies](../../README.md#using-the-library)
