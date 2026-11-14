# Ensure that the --cert-file and --key-file arguments are set as appropriate (C-0153)

Evaluates the etcd Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Follow the etcd service documentation and configure TLS encryption.

 Then, edit the etcd pod specification file `/etc/kubernetes/manifests/etcd.yaml` on the master node and set the below parameters.

```
--cert-file=</path/to/ca-file>
--key-file=</path/to/key-file>

```

**Admission resources**  `pods`.

**Kubescape severity score**  8/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0153-ensurethatthecertfileandkeyfileargumentsaresetasappropriate.json) · [Installing and binding policies](../../README.md#using-the-library)
