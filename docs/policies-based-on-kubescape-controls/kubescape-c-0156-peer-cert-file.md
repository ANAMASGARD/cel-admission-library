# Ensure that the --peer-cert-file and --peer-key-file arguments are set as appropriate (C-0156)

Evaluates the etcd Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Follow the etcd service documentation and configure peer TLS encryption as appropriate for your etcd cluster.

 Then, edit the etcd pod specification file `/etc/kubernetes/manifests/etcd.yaml` on the master node and set the below parameters.

```
--peer-client-file=</path/to/peer-cert-file>
--peer-key-file=</path/to/peer-key-file>

```

**Admission resources**  `pods`.

**Kubescape severity score**  7/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0156-ensurethatthepeercertfileandpeerkeyfileargumentsaresetasappropriate.json) · [Installing and binding policies](../../README.md#using-the-library)
