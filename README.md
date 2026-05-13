# Eric Skiff Systems Portfolio

Curated, public-safe portfolio workspace for reliability engineering,
automation, operations, and applied AI systems work.

This repository is intentionally separate from private operational repos.
Use it to publish selected writeups, sanitized architecture notes, and small
standalone artifacts that demonstrate judgment without exposing live systems,
credentials, customer data, or private operating context.

## Positioning

I build practical automation systems that survive contact with production:
service health checks, recovery drills, credential hygiene, deployment
guardrails, observability, and operator workflows.

## Candidate Public Artifacts

- Reliability remediation case study
- Backup and restore validation case study
- Git history sanitation and offsite backup case study
- Selected standalone scripts with dummy fixtures
- Architecture diagrams redrawn without private hostnames, credentials, or
  client-specific details

## Publication Rules

- No secrets, tokens, keys, hostnames, private IPs, customer data, or personal
  records.
- No direct dumps of private runbooks.
- Prefer narrative case studies over raw operational files.
- Keep examples runnable with synthetic fixtures.
- Scan every commit with `gitleaks` before publishing.

## Current Status

Local draft only. Do not push publicly until each artifact has been reviewed
for privacy and audience fit.
