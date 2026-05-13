# Reliability Remediation And Repo Sanitization

## Reviewer Summary

I took a private operational system from "mostly works, but has hidden recovery
and repo hygiene risk" to a cleaner baseline with explicit restore validation,
sanitized Git history, and verified offsite backup.

This case study is redacted and public-safe. It preserves the engineering
pattern without exposing live infrastructure, credentials, customers, or private
operational context.

## Impact

- Reduced recovery ambiguity by making restore validation produce explicit
  pass/fail evidence.
- Removed old Git history from the active repo paths after creating private
  quarantine bundles.
- Produced sanitized source baselines that could be stored off-network.
- Verified that encrypted backup bundles could be decrypted and restored into
  clean repos.
- Created a separate public portfolio path rather than exposing private
  operational repositories.

## Context

The system had grown organically. That left several common operational risks:

- Restore checks existed, but the success criteria needed to be more explicit.
- Failure notification behavior had drift between live services and managed
  infrastructure.
- Some service restart policy was too permissive for critical processes.
- Repositories mixed source, generated artifacts, private state, and old history
  containing secret-like examples.
- Off-network backup existed as an intention, but not as a restore-tested
  artifact.

## Failure Surface

I treated the cleanup as a reliability problem, not just a Git problem.

| Risk | Failure Mode | Remediation |
| --- | --- | --- |
| Restore validation | Backup appears present but cannot be restored | Add wrapper and explicit evidence record |
| Failure notification | Service fails but operator does not get useful signal | Repair managed notification template |
| Restart policy | Bad restart settings hide unstable services | Remove unsafe restart-limit behavior |
| Git history | Old refs keep sensitive examples reachable | Create sanitized root commits and prune old objects |
| Backup confidence | Offsite backup exists but restore path is untested | Encrypt bundles, restore from them, scan restored clones |

## Architecture

See [Reliability Remediation Flow](../diagrams/reliability-remediation-flow.md).

The important design choice was to verify the artifact that would actually be
used during recovery. A backup file that has never been restored is only a
theory.

## Decisions And Tradeoffs

### Sanitize History Instead Of Publishing Private Repos

I created sanitized single-root histories for the publishable backup path. That
preserved the current source state while removing old refs and unreachable
objects from active storage.

Tradeoff: old commit history is no longer available in the active repo. I kept
private quarantine bundles locally so recovery remained possible without
carrying sensitive history into normal remotes.

### Use Encrypted Bundles For Complete Offsite Backup

One repo could be pushed directly as a private source backup. Another included
workflow files that required additional GitHub token scope. Rather than expand
token privileges just to push source, I used encrypted Git bundles for the
complete backup.

Tradeoff: encrypted bundles are less convenient than a normal remote, but they
are portable, explicit, and easy to restore-test.

### Separate Portfolio From Operations

The private operational repos contain useful work, but they are not appropriate
as public job artifacts. I created this separate portfolio repo so public
examples can be written for reviewers instead of leaked from production context.

Tradeoff: this takes more writing effort, but it produces a much better hiring
surface.

## Verification

The final verification pass included:

- Tracked-tree secret scans.
- Branch-diff secret scans.
- Full-history scans after ref deletion and garbage collection.
- Bare remote scans.
- Encrypted bundle checksum verification.
- Decrypt-and-restore tests from the encrypted bundle backup.
- Secret scans against restored clones.

All final publishable paths scanned clean.

## What I Would Automate Next

- Scheduled encrypted bundle creation with retention policy.
- A CI check that blocks commits if generated/private artifact patterns appear.
- A small restore-drill command that creates a temp clone, scans it, and reports
  the exact commit and checksum restored.
- A portfolio publishing checklist that runs privacy and secret scans before
  public push.

## What This Shows

This work is representative of how I approach systems:

- Start with the failure surface.
- Fix the recovery path, not just the visible symptom.
- Prefer evidence-producing checks over hopeful scripts.
- Treat secrets and history as part of the system boundary.
- Leave behind a workflow that is easier to audit next time.
