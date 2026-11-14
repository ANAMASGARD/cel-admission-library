# Ensure that the --peer-client-cert-auth argument is set to true (C-0157)

Evaluates the etcd Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the etcd pod specification file `/etc/kubernetes/manifests/etcd.yaml` on the master node and set the below parameter. ```--peer-client-cert-auth=true```

**Admission resources**  `pods`.

**Kubescape severity score**  7/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0157-ensurethatthepeerclientcertauthargumentissettotrue.json) · [Installing and binding policies](../../README.md#using-the-library)
