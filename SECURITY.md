# Security and privacy boundaries

This is an offline portfolio prototype, not a hosted production service or certified compliance tool.

- Runtime code makes no network requests and accepts no credentials.
- Reports embed supplied source records. Treat real-data reports as sensitive even if IDs are pseudonymized.
- The HTML renderer escapes record strings and uses no JavaScript or external assets. A restrictive content security policy is embedded.
- Strict field validation is not a general PII detector. Review allowed string values before use or sharing.
- Output files inherit local OS permissions; encryption, access control and retention are the operator's responsibility.
- `private-data/` and `local-reports/` are ignored by Git, but ignore patterns do not secure files or undo prior commits.
- This release is batch-only. Do not expose it as a public web service without authentication, authorization, upload hardening and security review.

If published on GitHub, use private vulnerability reporting if the maintainer has enabled it. Otherwise open a minimal issue requesting a private reporting route without exploit details, merchant data or secrets. Never publish credentials in an issue.
