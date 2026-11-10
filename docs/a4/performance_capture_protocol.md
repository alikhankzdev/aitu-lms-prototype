# B2. Actual DevTools measurement protocol

Sources: Assignment 4 page 2 B2; End-term page 2 B3. File sizes are not network results. This pack contains no claimed Fast 4G measurement.

1. Preserve a runnable baseline build before image changes. Keep user, data, viewport, route and browser version identical in both builds.
2. Chrome DevTools → Network → Disable cache. Choose Fast 4G and keep DevTools open.
3. Clear the log, reload the main screen, wait for loading to finish and record total transferred bytes, request count and Load or Finish (choose one consistently).
4. Save a screenshot showing route, throttling, cache setting and summary; save HAR when permitted (inspect and remove credentials before sharing).
5. Repeat at least three times for both builds; avoid unrelated network/background activity. Record raw runs before calculating averages.
6. Explain whether the exact Stage 1 performance target is met. Do not substitute a new easier target.

| Build | Run | Transferred KB | Requests | Chosen timing metric | Seconds | Screenshot |
|---|---:|---:|---:|---|---:|---|
| Baseline | 1 | pending | pending | pending | pending | pending |
| Baseline | 2 | pending | pending | pending | pending | pending |
| Baseline | 3 | pending | pending | pending | pending | pending |
| Optimised | 1 | pending | pending | pending | pending | pending |
| Optimised | 2 | pending | pending | pending | pending | pending |
| Optimised | 3 | pending | pending | pending | pending | pending |

Mean = (run1 + run2 + run3) / 3. Percentage size reduction = 100 × (baseline mean − optimised mean) / baseline mean. If requests increase, say so. A smaller file does not guarantee a faster page under every test condition.
