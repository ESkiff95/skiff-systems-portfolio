# Skiff Systems Portfolio

Public-safe portfolio of reliability engineering, automation, and applied AI
operations work.

This repo is not a dump of private infrastructure. It is a curated set of case
studies and small standalone artifacts that show how I approach production
systems: failure modes first, observability, recovery drills, security hygiene,
and practical automation.

## What This Demonstrates

- Reliability remediation for service-backed systems
- Backup and restore validation
- Git history sanitation and secret-prevention workflow
- Operational runbook design
- Small automation tools built for boring, repeatable checks

## Case Studies

- [Reliability Remediation And Repo Sanitization](case-studies/reliability-remediation.md)

## Artifacts

- [Backup Manifest Check](artifacts/backup_manifest_check.py): a small Python
  CLI that validates backup freshness, optional SHA-256 digests, and gzip
  readability from a JSON manifest.

## Safety Model

The original work was done in private operational repositories. This public
repo uses synthetic examples and redacted descriptions only.

Before anything is published here:

- No secrets, tokens, keys, private IPs, customer data, personal records, or raw
  logs.
- No private hostnames, live domains, credential paths, or customer/prospect
  lists.
- Examples must run against synthetic fixtures or operator-provided paths.
- Every commit should pass a secret scan.

## Contact Framing

If you are reviewing this for hiring, the interesting part is not the exact
stack. It is the operating style: define the failure surface, write the check,
wire the recovery path, verify it, and leave the system easier to audit next
time.
