# Ensure that the --peer-auto-tls argument is not set to true (C-0158)

Evaluates the etcd Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the etcd pod specification file `/etc/kubernetes/manifests/etcd.yaml` on the master node and either remove the `--peer-auto-tls` parameter or set it to `false`.

```
--peer-auto-tls=false

```

**Admission resources**  `pods`.

**Kubescape severity score**  6/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0158-ensurethatthepeerautotlsargumentisnotsettotrue.json) · [Installing and binding policies](../../README.md#using-the-library)
