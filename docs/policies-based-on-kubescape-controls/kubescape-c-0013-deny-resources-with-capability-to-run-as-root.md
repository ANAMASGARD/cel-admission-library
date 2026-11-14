# C-0013 Non-root containers

Each regular, init and ephemeral container needs either an effective nonzero UID or an effective `runAsNonRoot: true`. Linux containers also need a nonzero group. For each field independently, a container setting overrides the Pod setting. Missing UID and GID default to zero for this check. Windows Pods omit the group check.

Earlier releases also required `allowPrivilegeEscalation: false`. To retain escalation enforcement when upgrading, bind C-0016 alongside C-0013. Existing Linux workloads relying on an unspecified group need an explicit non-root GID.

[Source rule](https://github.com/kubescape/regolibrary/tree/b7e5706/rules/non-root-containers) · [Installing the policies](../../README.md#using-the-library)
