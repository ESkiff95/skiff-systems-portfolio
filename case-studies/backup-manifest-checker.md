# Backup Manifest Checker

## Summary

`backup_manifest_check.py` is a small public-safe CLI for validating backup
artifacts from a JSON manifest. It checks whether files exist, whether they are
fresh enough, whether optional SHA-256 digests match, and whether gzip archives
can be read.

The tool is intentionally boring. That is the point: recovery checks should be
easy to run, easy to automate, and difficult to misread.

## Why This Exists

Many backup systems fail in quiet ways:

- A scheduled job writes no file.
- A file exists but is stale.
- A compressed archive is corrupt.
- A checksum no longer matches the expected artifact.
- A human sees "backup succeeded" but no one has tested the restore path.

This artifact models the first layer of defense: make backup evidence explicit.

## Example Manifest

```json
{
  "backups": [
    {
      "name": "nightly-database-dump",
      "path": "/path/to/backup.sql.gz",
      "max_age_hours": 48,
      "gzip": true,
      "sha256": ""
    }
  ]
}
```

## Example Run

```sh
python3 artifacts/backup_manifest_check.py artifacts/backup-manifest.example.json --pretty
```

Example output shape:

```json
{
  "checked": 1,
  "ok": true,
  "results": [
    {
      "details": ["fresh age_hours=0.00", "sha256_ok", "gzip_ok"],
      "name": "synthetic",
      "ok": true,
      "path": "/tmp/example/backup.sql.gz"
    }
  ]
}
```

## Design Notes

- The tool exits nonzero when any backup fails validation.
- It uses a manifest instead of hardcoded paths.
- It reads gzip files fully, not just by extension.
- It reports machine-readable JSON so a timer, CI job, or health check can
  consume the result.

## What I Would Add In Production

- Restore drill support for selected backup types.
- Retention policy checks.
- Alert routing on stale or corrupt backups.
- Signed manifests for stronger chain-of-custody.
