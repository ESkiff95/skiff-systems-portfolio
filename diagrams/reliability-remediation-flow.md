# Reliability Remediation Flow

```mermaid
flowchart LR
    A[Operational Services] --> B[Health And Restore Checks]
    B --> C[Backup Drill]
    C --> D[Restore Validation Wrapper]
    D --> E[Structured Pass/Fail Evidence]

    F[Local Git Repos] --> G[Tracked Tree Scan]
    F --> H[Full History Scan]
    G --> I[Sanitized Source Baseline]
    H --> I

    I --> J[Private Source Backup]
    I --> K[Encrypted Git Bundles]
    K --> L[Restore-Tested Offsite Backup]

    E --> M[Operator Confidence]
    L --> M
```

The pattern is deliberately simple:

1. Find the places where the system can silently lie.
2. Make the check produce explicit evidence.
3. Separate source from generated/private state.
4. Verify recovery from the artifact that would be used in an outage.
