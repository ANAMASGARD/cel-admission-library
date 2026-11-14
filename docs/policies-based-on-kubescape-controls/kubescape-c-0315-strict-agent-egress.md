# Agent Sandbox strict egress policy (C-0315)

In strict mode the SandboxTemplate must explicitly deny all egress. Managed mode leaves the strict check disabled.

**Admission resources**  `sandboxtemplates`.

**Configuration**  `agentSandboxEgressMode`.

**Kubescape severity score**  8.0/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0315-agent-sandbox-strict-egress.json) · [Installing and binding policies](../../README.md#using-the-library)
