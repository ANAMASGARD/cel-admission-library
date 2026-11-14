# Ensure that the Controller Manager --profiling argument is set to false (C-0145)

Evaluates the kube-controller-manager Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the Controller Manager pod specification file `/etc/kubernetes/manifests/kube-controller-manager.yaml` on the Control Plane node and set the below parameter.

```
--profiling=false

```

**Admission resources**  `pods`.

**Kubescape severity score**  3/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0145-ensurethatthecontrollermanagerprofilingargumentissettofalse.json) · [Installing and binding policies](../../README.md#using-the-library)
