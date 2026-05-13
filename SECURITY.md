# Security Policy

This is a public portfolio repository. Do not open issues or pull requests that
include secrets, private logs, customer data, internal hostnames, or personal
records.

If you notice accidentally exposed sensitive material, contact the repository
owner privately and include only the file path and line number. Do not paste the
secret value into an issue.

Before publishing changes:

```sh
gitleaks detect --source . --redact
```

All examples should use synthetic fixtures and placeholders.
