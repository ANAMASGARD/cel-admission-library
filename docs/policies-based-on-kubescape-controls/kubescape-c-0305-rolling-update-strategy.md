# No rolling update strategy (C-0305)

A Deployment passes when its strategy is omitted or set to RollingUpdate. Explicit Recreate fails.

**Admission resources**  `deployments`.

**Kubescape severity score**  3.0/10.

[Source control](https://github.com/kubescape/regolibrary/blob/b7e5706/controls/C-0305-norollingupdatestrategy.json) · [Installing and binding policies](../../README.md#using-the-library)
