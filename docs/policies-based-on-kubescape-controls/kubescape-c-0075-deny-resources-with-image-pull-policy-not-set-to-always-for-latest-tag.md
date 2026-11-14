# Kubescape C-0075: Deny resources with imagePullPolicy not set to always for image with latest tag

## Why this policy is required:
While usage of the latest tag is not generally recommended, in some cases this is necessary. If it is, the ImagePullPolicy must be set to Always, otherwise Kubernetes may run an older image with the same name that happens to be present in the node cache. Note that using Always will not cause additional image downloads because Kubernetes will check the image hash of the local local against the registry and only pull the image if this hash has changed, which is exactly what users want when use the latest tag.


## Severity Level: Low

## Configuration Parameters:
* `floatingImageTags` adds mutable tag names such as `stable` or `nightly`.

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
* This Policy checks if `imagePullPolicy` is set to `Always` for images with `latest` tag, for every container, init container, and ephemeral container (added with `kubectl debug`). If not, the resource is denied from being deployed in the cluster.

With no configured tags the policy still checks untagged images and `:latest`. A configured floating tag pinned by digest is allowed. To supply additional tags when upgrading, apply the updated ControlConfiguration CRD, populate the settings, then set the binding’s `paramRef` to that object.


## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)