# Ensure that the Controller Manager --service-account-private-key-file argument is set as appropriate (C-0147)

Evaluates the kube-controller-manager Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the Controller Manager pod specification file `/etc/kubernetes/manifests/kube-controller-manager.yaml` on the Control Plane node and set the `--service-account-private-key-file` parameter to the private key file for service accounts.

```
--service-account-private-key-file=<filename>

```

**Admission resources**  `pods`.

**Kubescape severity score**  6/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0147-ensurethatthecontrollermanagerserviceaccountprivatekeyfileargumentissetasappropriate.json) · [Installing and binding policies](../../README.md#using-the-library)
