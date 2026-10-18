# Design — slice 1 (v0.1.0)

Date: 2026-10-18. Follows Brief `docs/brief.md`. One slice, one branch.

## Outcome

A stdlib-only CLI `speclint` that lints `spec.md` for C1/C2/C3/C8 structure
and reports PASS/FAIL per check with evidence.

## Acceptance

Same as REQ-1..REQ-6 in Brief. Verified by:
`task test` (unit + integration) green, `task verify` green on PR,
`spliced fixtures` 5/5 fail as expected, current `spec.md` v2 passes,
runtime <2s, `task build` produces `speclint:local` image.

## Context

Solo, local + CI. No service to run, no DB, no secrets, no contract.
Source language Python 3.12 (matches CI). No new tools. Reuses de-slopped
Taskfile shape (1–3 line shell, no glue scripts) + single-gate `ci.yml`.

## §3 checklist (triggered rules — fire only when observed)

- T1 Auth/sensitive/external surface: NO. CLI parses local markdown, no
  logins, no PII, no network, no new surface. No threat model.
- T2 Schema/data compat: NO. No persistent data, no readers to break.
- T3 Versioned contract: NO. No openapi/docs/contracts in v0.1.0.
- T4 Real users/prod deploy: NO. Local + CI only. No prod, no rollout.
  First-release minimum N/A (no prod deploy claimed).
- T5 Loss-cost: NO. Re-run cost is seconds. No recovery objectives.
- T6 Incident: NO (none observed). If CI breaks, one record will be kept.
- T7 Compliance: NO. No law/contract/auditor obligation.
- T8 AI-material: YES. Code is AI-assisted. Actions: zero external packages
  (stdlib only, verified by import scan in tests); `check:secrets` +
  `check:audit` run on PR via `task verify`; human reviews test deletions /
  weakened assertions / mocks / build changes (none in v0.1.0 — no test
  deletions, no mocks, build is `docker build` only).
- E1 Production change: NO. No prod.
- E2 Access: NO team, NO regulated prod. Solo checks-only (CODEOWNERS
  requires checks only, never approval). No separation needed.
- E3 Retention: NO. No obligation.
- E4 Supply-chain/external distribution: NO. No binary leaves the team.
  Release is git tag + source + local Docker image + sha256 manifest.
  No registry push, no store, no signed external binary. Y6/E4 evaluated,
  judged not fired (recorded here).
- Y1 Service: NO. CLI, not a runnable service. No livez/readyz.
- Y2 Library: NO. CLI, not a published library (no registry API).
- Y3 Mobile: NO.
- Y4 Model/data: NO.
- Y5 IaC: NO.
- Y6 External binary: NO. Internal-only CLI. Checksums published in release
  for integrity, but no OS-store distribution, no signing identity needed.
  Expectation note in README covers reputation warning if ever distributed.

Fired: T8 only. All others explicitly evaluated, absent means omitted
(never stubbed) per B9.
