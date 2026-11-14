# Ensure that the API Server --profiling argument is set to false (C-0129)

Evaluates the kube-apiserver Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the API server pod specification file `/etc/kubernetes/manifests/kube-apiserver.yaml` on the Control Plane node and set the below parameter.

```
--profiling=false

```

**Admission resources**  `pods`.

**Kubescape severity score**  3/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0129-ensurethattheapiserverprofilingargumentissettofalse.json) · [Installing and binding policies](../../README.md#using-the-library)
