# Ensure that the Scheduler --bind-address argument is set to 127.0.0.1 (C-0152)

Evaluates the kube-scheduler Pod manifest against the pinned benchmark rule. The kubelet can start static Pods without admission. This policy can evaluate their submitted manifests or mirror objects.

Edit the Scheduler pod specification file `/etc/kubernetes/manifests/kube-scheduler.yaml` on the Control Plane node and ensure the correct value for the `--bind-address` parameter

**Admission resources**  `pods`.

**Kubescape severity score**  5/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0152-ensurethattheschedulerbindaddressargumentissetto127001.json) · [Installing and binding policies](../../README.md#using-the-library)
