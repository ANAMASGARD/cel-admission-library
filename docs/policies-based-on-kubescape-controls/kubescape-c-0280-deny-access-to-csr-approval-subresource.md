# Kubescape C-0280: Deny access to certificatesigningrequests/approval sub-resource

## Why this policy is required:
Users with access to update the approval sub-resource of certificatesigningrequests objects can approve new client certificates for the Kubernetes API, effectively allowing them to create new high-privileged user accounts. This can allow for privilege escalation to full cluster administrator.

## Severity Level: Medium

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* ClusterRole
* Role

## What does this policy do:
This Policy checks whether any Role or ClusterRole grants access to the `certificatesigningrequests/approval` or `certificatesigningrequests/*` sub-resource. If such access is found, the resource is denied.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)

Admission checks Role and ClusterRole definitions before a binding exists. The API group must be `certificates.k8s.io` or `*` and the verbs must include `update`, `patch` or `*`. Kubernetes grants subresource access for the exact resource, `*/approval` or `*`. The admission rule also retains the library’s preventive restriction on the literals `certificatesigningrequests/*` and `*/*`. The RBAC authorizer does not expand those literals for CSR approval. Rego reports the subject of an effective ClusterRoleBinding, since CSRs are cluster-scoped. [RBAC resource matching](https://github.com/kubernetes/kubernetes/blob/v1.35.1/pkg/apis/rbac/v1/evaluation_helpers.go#L52-L76) · [Rego rule](https://github.com/kubescape/regolibrary/blob/b7e57060ca90c41fe15359383245a7c62f09487c/rules/rule-can-approve-cert-signing-request/raw.rego)
