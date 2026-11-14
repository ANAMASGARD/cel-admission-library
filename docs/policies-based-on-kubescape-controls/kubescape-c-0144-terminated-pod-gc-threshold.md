# Ensure that the Controller Manager --terminated-pod-gc-threshold argument is set as appropriate (C-0144)

Evaluates the kube-controller-manager Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects. Use a Warn or Audit binding for the required manual review.

Edit the Controller Manager pod specification file `/etc/kubernetes/manifests/kube-controller-manager.yaml` on the Control Plane node and set the `--terminated-pod-gc-threshold` to an appropriate threshold, for example:

```
--terminated-pod-gc-threshold=10

```

**Admission resources**  `pods`.

**Kubescape severity score**  4/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0144-ensurethatthecontrollermanagerterminatedpodgcthresholdargumentissetasappropriate.json) · [Installing and binding policies](../../README.md#using-the-library)
