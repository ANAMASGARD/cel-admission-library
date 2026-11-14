kubescape-c-0055-linux-hardening
# Kubescape C-0055: Linux Hardening

## Why this policy is required:
In order to reduce the attack surface, it is recommend, when it is possible, to harden your application using security services such as SELinux®, AppArmor®, and seccomp. Starting from Kubernetes version 22, SELinux is enabled by default.

## Severity Level: Medium

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
This Policy checks if there is `AppArmor` or `Seccomp` or `SELinux` or `Capabilities` are defined in the `securityContext` of the pod and of every container, init container, and ephemeral container (added with `kubectl debug`). If none of these fields are defined for the pod, and they are also missing for any of these containers, the resource is denied from being deployed in the cluster. AppArmor counts whether it is set with the `appArmorProfile` field or with the older `container.apparmor.security.beta.kubernetes.io/*` annotation on the pod (for a workload, on its pod template), as long as it enforces a profile: `Unconfined` (or the annotation value `unconfined`) turns AppArmor off and doesn't count.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)

Each container inherits its pod's settings unless it has an override. For AppArmor the kubelet checks the container field, then that container's legacy annotation, then the pod field. A container that overrides an enforcing pod profile with `Unconfined` needs another hardening measure. Dropping at least one capability or supplying SELinux options also satisfies the policy. Windows workloads are exempt. [Kubelet AppArmor selection](https://github.com/kubernetes/kubernetes/blob/v1.35.1/pkg/security/apparmor/helpers.go#L54-L73)

The pinned Rego rule checks seccomp field presence on regular and init containers. It reports an AppArmor-only workload and accepts an explicit unconfined seccomp profile. The admission policy retains the library's broader hardening alternatives and checks ephemeral containers too. [Rego source](https://github.com/kubescape/regolibrary/blob/b7e57060ca90c41fe15359383245a7c62f09487c/rules/linux-hardening/raw.rego)
