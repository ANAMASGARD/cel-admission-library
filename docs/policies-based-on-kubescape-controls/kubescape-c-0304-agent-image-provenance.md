# Agent Sandbox image provenance (C-0304)

Validates the configured registry list and tag policy for regular and init containers. An empty allowlist denies each nonempty image.

**Admission resources**  `sandboxtemplates`.

**Configuration**  `floatingImageTags`, `imageRepositoryAllowList`.

**Kubescape severity score**  7.0/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0304-agentsandboximageprovenance.json) · [Installing and binding policies](../../README.md#using-the-library)
