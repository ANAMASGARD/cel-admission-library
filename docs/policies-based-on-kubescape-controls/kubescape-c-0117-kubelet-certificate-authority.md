# Ensure that the API Server --kubelet-certificate-authority argument is set as appropriate (C-0117)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Follow the Kubernetes documentation and setup the TLS connection between the apiserver and kubelets. Then, edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the Control Plane node and set the `--kubelet-certificate-authority` parameter to the path to the cert file for the certificate authority.

```
--kubelet-certificate-authority=<ca-string>

```

**Admission resources**  `pods`.

**Kubescape severity score**  8/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0117-ensurethattheapiserverkubeletcertificateauthorityargumentissetasappropriate.json) · [Installing and binding policies](../../README.md#using-the-library)
