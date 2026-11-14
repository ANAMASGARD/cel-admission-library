# Images not pinned to digest (C-0306)

Checks regular, init and ephemeral container images. Optional exempt repository prefixes match only at the repository boundary.

**Admission resources**  `pods`, `pods/ephemeralcontainers`, `deployments`, `replicasets`, `daemonsets`, `statefulsets`, `jobs`, `cronjobs`.

**Configuration**  `imageDigestExemptRepositories`.

**Kubescape severity score**  3.0/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0306-imagenotpinnedtodigest.json) · [Installing and binding policies](../../README.md#using-the-library)
