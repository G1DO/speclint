# Delivery record — v0.1.0

Date: 2026-10-18. Version: v0.1.0. Tag: `v0.1.0` on `main`.

## What shipped

`speclint` v0.1.0 — stdlib-only CLI that lints `spec.md` for C1/C2/C3/C8
structure (REQ-1..REQ-6 in `docs/brief.md`). Slice 1 + release docs.

Commits: `9ee18b1` Define, `5b4cf18` Design, `ec7c9e2` Implement,
`42b2ca9` bash fix, merge `03dbd59`, plus this release record.

## Where it ran (target proof)

- Repo: https://github.com/G1DO/speclint
- PR 1 (slice): https://github.com/G1DO/speclint/pull/1 — `task verify` pass
  41s + `gate` pass (run 39160320735, 2026-10-18).
- PR 2 (release record): link added after merge (see below).
- Local: `task verify` green on clean checkout (see CI + local log).
- CLI proof: `python3 -m src.speclint /home/thoth/chat/workflow-spec/spec.md`
  → TOTAL PASS (39 IDs, 27 rows justified/observable, no mandates,
  baseline 1 page, <2s).
- Docker: `speclint:local` builds (`task build` green, image ID recorded in CI).
- Checksums: `docs/sha256-manifest.txt` (source integrity, no binary leaves team).
- Clean install: fresh `git clone` + `task verify` green (CI does exactly this).

No registry push, no store, no apply log (no service/IaC). Internal-only CLI,
so Y6/E4 judged not fired (see `docs/design.md`).

## Rollback

- Previous state: pre-v0.1.0 `main` at `9ee18b1` (brief only).
- Roll forward: new version tag (preferred — forward-only).
- Roll back: `git revert` the merge or reset tag to `9ee18b1`; no data to migrate
  (`task migrate` N/A absent); no prod users affected.
- Owner: G1DO. Monitoring: CI `verify` + `gate` on every PR; nightly not
  configured (solo, no prod — recorded as N/A).

## Verification (B7)

Each REQ linked to evidence + date (see `docs/verification.md` after release).
CI green is not verification by itself — human confirms acceptance below.
