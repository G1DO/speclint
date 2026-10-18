# Incident record

Date: 2026-10-18. Status: one record, timeline-to-postmortem (T6 fires only
if a user-impacting production failure is observed — none here; this is a
CI-break record kept as evidence, not a prod incident).

## Timeline

- 19:43 UTC CI run 39160026463 FAIL: `task test:e2e` → `sh: 1: set: Illegal
  option -o pipefail`. Local `task verify` had been green.
- Cause: de-slopped verbs use `sh -c 'set -euo pipefail'`; GitHub
  ubuntu-latest `/bin/sh` (dash) rejects `-o pipefail` in combined form,
  while local shell accepted it. Latent in P7 (PR #11 CI never ran).
- Fix: `s/sh -c/bash -c/` (7 verbs) on branch, `task verify` green locally,
  push, CI run 39160320735 PASS (verify 41s + gate 2s).

## Contributing factors

- P7 shell-verbs negatives ran locally only, no CI run URL (see acceptance C6).
- `task` default shell differs from explicit `sh -c` portability.

## Action items

- [x] Fix verbs to `bash -c` — owner G1DO, done 2026-10-18.
- [ ] Upstream note: suggest `bash -c` in workflow repo if P7 verbs land —
  owner G1DO, expires 2026-11-18. (No spec/repo change without evidence;
  logged here only.)
