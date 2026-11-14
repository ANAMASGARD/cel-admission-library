# C-0210 RuntimeDefault seccomp profile

Linux containers must use an effective seccomp profile of `RuntimeDefault`. A container-level setting takes precedence over Pod-level configuration. An unspecified, Localhost or Unconfined effective profile fails. Windows workloads are exempt.

[Source rule](https://github.com/kubescape/regolibrary/tree/b7e5706/rules/set-seccomp-profile-RuntimeDefault) · [Installation](../../README.md#using-the-library)
