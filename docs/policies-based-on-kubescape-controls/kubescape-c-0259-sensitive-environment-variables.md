# Workload with credential access (C-0259)

Checks literal environment variables on Pods and workload templates. Absolute file paths, empty values, and valueFrom references pass. Allowed key names are case-insensitive substrings and allowed values are regular expressions. The source checks value patterns in regular containers and sensitive names in regular, init and ephemeral Pod containers. Empty allowlist patterns are ignored so older configurations containing an empty string continue to protect workloads.

**Admission resources**  `pods`, `pods/ephemeralcontainers`, `deployments`, `replicasets`, `daemonsets`, `statefulsets`, `jobs`, `cronjobs`.

**Configuration**  `sensitiveKeyNames`, `sensitiveKeyNamesAllowed`, `sensitiveValues`, `sensitiveValuesAllowed`.

**Kubescape severity score**  8.0/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0259-workloadwithcredentialaccess.json) · [Installing and binding policies](../../README.md#using-the-library)
