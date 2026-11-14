# Ensure that the API Server --kubelet-client-certificate and --kubelet-client-key arguments are set as appropriate (C-0116)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Follow the Kubernetes documentation and set up the TLS connection between the apiserver and kubelets. Then, edit API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the Control Plane node and set the kubelet client certificate and key parameters as below.

```
--kubelet-client-certificate=<path/to/client-certificate-file>
--kubelet-client-key=<path/to/client-key-file>

```

**Admission resources**  `pods`.

**Kubescape severity score**  7/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0116-ensurethattheapiserverkubeletclientcertificateandkubeletclientkeyargumentsaresetasappropriate.json) · [Installing and binding policies](../../README.md#using-the-library)
