# Agent Substrate Worker Pod resource ceilings (C-0317)

A WorkerPool needs a Pod-level limit for each configured ceiling. Empty ceilings disable their respective checks.

**Admission resources**  `workerpools`.

**Configuration**  `workerCpuLimitMax`, `workerMemoryLimitMax`.

**Kubescape severity score**  7.0/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0317-worker-pod-resource-ceilings.json) · [Installing and binding policies](../../README.md#using-the-library)
