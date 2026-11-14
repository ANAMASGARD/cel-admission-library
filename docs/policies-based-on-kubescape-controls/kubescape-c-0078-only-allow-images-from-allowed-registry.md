# Kubescape C-0078: Deny resources with images not from allowed registry

## Why this policy is required:
If attackers get access to the cluster, they can re-point kubernetes to a compromized container repository. This control is intended to ensure that all the container images are taken from the authorized repositories only.

## Severity Level: Medium

## Configuration Parameters:
* [imageRepositoryAllowList](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#imagerepositoryallowlist)

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
This Policy checks that all the containers, init containers, and ephemeral containers (added with `kubectl debug`) in the resource are using images from the [imageRepositoryAllowList](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#imagerepositoryallowlist). If not, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)

Entries may name a host, a repository namespace such as `quay.io/kubescape/`, or an exact repository. Docker Hub short names use the canonical path, so `docker.io/library/nginx` admits `nginx:1.27`. Entry boundaries prevent a lookalike host or repository from inheriting permission. The shipped list is empty: a Deny binding rejects matching workloads until an operator populates it. To preserve the previous example configuration on upgrade, set `imageRepositoryAllowList: ["gcr.io"]` before binding C-0078.
