# Kubescape C-0225: Prefer using dedicated EKS Service Accounts

## Why this policy is required:
Every namespace gets a ServiceAccount called `default`, and every pod that does not name one runs as it. So `default` is shared by everything in the namespace, and nothing that runs as it can be told apart from anything else that runs as it.

Two things follow, and this policy checks both. Granting the `default` ServiceAccount extra permissions hands those permissions to every pod in the namespace, including ones added later by someone who has no idea the binding exists. And leaving `automountServiceAccountToken` on means the token is mounted into pods that never asked for an identity at all, so anything that reads the filesystem of a compromised container gets a usable credential.

## Severity Level: High

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* ClusterRoleBinding
* RoleBinding
* ServiceAccount

## What does this policy do:
This policy is two independent checks under one control ID, each matching different kinds.

On a RoleBinding or ClusterRoleBinding:
* An explicit ServiceAccount named `default` or its User spelling `system:serviceaccount:<namespace>:default` triggers a finding.
* Unless the binding carries the label `kubernetes.io/bootstrapping: rbac-defaults`, which is how Kubernetes marks its own built-in bindings. Several of those bind the `default` ServiceAccount on purpose, so without this exemption the policy would fire on the cluster's own RBAC in every namespace.

On a ServiceAccount:
* If it is named `default` and `automountServiceAccountToken` is not explicitly `false`, it is denied.
* An absent field counts as a failure, not a pass. Kubernetes mounts the token when nothing says otherwise, so silence means yes. This is the same reasoning as [C-0034](/docs/policies-based-on-kubescape-controls/kubescape-c-0034-deny-resources-with-automount-service-account-token-enabled.md).

A ServiceAccount with any other name is not touched by this policy, whatever it does with its token.

## How to satisfy it:
Give each workload its own ServiceAccount, bind permissions to that, and set `automountServiceAccountToken: false` on the `default` one in every namespace so nothing picks up a token by accident.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)


### Namespace bootstrap and binding scope

A default ServiceAccount created by the namespace controller has no explicit token setting. A Deny binding covering all ServiceAccounts can prevent that account from being provisioned. The example below applies Deny to RBAC bindings and Warn to ServiceAccounts. Remove any broader Deny binding for this policy when switching to the split configuration. Set `automountServiceAccountToken: false` on each default account after provisioning.

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: c-0225-rbac
spec:
  policyName: kubescape-c-0225-deny-default-service-account-rbac-and-automount
  validationActions: [Deny]
  matchResources:
    resourceRules:
    - apiGroups: ["rbac.authorization.k8s.io"]
      apiVersions: ["v1"]
      operations: [CREATE, UPDATE]
      resources: [rolebindings, clusterrolebindings]
---
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: c-0225-serviceaccounts
spec:
  policyName: kubescape-c-0225-deny-default-service-account-rbac-and-automount
  validationActions: [Warn, Audit]
  matchResources:
    resourceRules:
    - apiGroups: [""]
      apiVersions: ["v1"]
      operations: [CREATE, UPDATE]
      resources: [serviceaccounts]
```

Both the source and the admission policy trust the binding's bootstrap label. Its presence does not authenticate the creator. They also allow Group subjects, including `system:serviceaccounts` and `system:serviceaccounts:<namespace>`, which grant access to the default account indirectly. These cases remain tracked upstream. [C-0225 follow-up](https://github.com/kubescape/cel-admission-library/issues/168)
