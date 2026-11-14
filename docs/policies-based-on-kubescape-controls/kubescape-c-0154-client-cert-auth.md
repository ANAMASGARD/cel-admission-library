# Ensure that the --client-cert-auth argument is set to true (C-0154)

Evaluates the etcd Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the etcd pod specification file `/etc/kubernetes/manifests/etcd.yaml` on the master node and set the below parameter.

```
--client-cert-auth="true"

```

**Admission resources**  `pods`.

**Kubescape severity score**  8/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0154-ensurethattheclientcertauthargumentissettotrue.json) · [Installing and binding policies](../../README.md#using-the-library)
