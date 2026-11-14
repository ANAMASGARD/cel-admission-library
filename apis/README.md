# Policy release artifacts

Use `kubescape-validating-admission-policies.yaml` for the full stable catalog. It is byte-identical to the `-v1.yaml` asset. The legacy artifacts include subsets that their API and CEL implementation can load. Before installing one, consult the release's **policy-coverage.md**, which lists every policy and marks membership in each artifact. Every release also includes the configuration CRD, default parameter object, and SHA-256 checksums.

| Asset suffix | Implementation exercised | Contents |
| --- | --- | --- |
| v1 | Native `admissionregistration.k8s.io/v1`, Kubernetes 1.31 | All control-backed and runtime VAPs registered in Kustomize |
| v1beta1 | Native `admissionregistration.k8s.io/v1beta1`, Kubernetes 1.28 | Policies accepted by the beta API and its CEL compiler. This server rejected optional field-selection syntax in new expressions. |
| v1alpha1 | Native `admissionregistration.k8s.io/v1alpha1`, Kubernetes 1.27 | The alpha schema lacks `spec.variables`. The overlay selects the compatible controls and runtime policies tested on this API. |
| x-v1alpha1 | `admissionregistration.x-k8s.io/v1alpha1` CRDs and CEL admission webhook | Same policy bodies as the native alpha subset. Requires deployment of the separate webhook and its CRDs. [Upstream installation](https://github.com/kubernetes/cel-admission-webhook/blob/4d862d34ffeec39f15fa4b21263529b5b813b179/INSTALL.md) |

Build the artifacts from the repository root with `python scripts/build-release.py release`. The script checks every control ID against its directory, verifies all registered names, checks the rendered API versions and compares the legacy policy bodies with the stable render. It writes the coverage table and digests from those same bytes. [Build script](../scripts/build-release.py)

The release workflow installs each bundle on a disposable server, exercises a named policy denial and admits a compliant Pod. The x-k8s check runs the pinned webhook. The Kubernetes 1.27 checker may report field warnings on kind-guarded expressions, for example a Pod field under the Deployment schema. Live admission exercises the Pod branch. Apply the binding required for each policy and install any referenced resource APIs to exercise those scopes. [Qualification workflow](../.github/workflows/release.yaml) · [Policy conversion guide](../CONVERSION_GUIDE.md)
