# Ensure that the API Server --token-auth-file parameter is not set (C-0114)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Follow the documentation and configure alternate mechanisms for authentication. Then, edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the master node and remove the `--token-auth-file=<filename>` parameter.

**Admission resources**  `pods`.

**Kubescape severity score**  8/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0114-ensurethattheapiservertokenauthfileparameterisnotset.json) · [Installing and binding policies](../../README.md#using-the-library)
