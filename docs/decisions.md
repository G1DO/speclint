# Decisions

Date format YYYY-MM-DD. One record per costly-to-reverse, cross-slice,
contract/data/prod choice.

## 2026-10-18 — Stdlib only, no external packages

Context: T8 fires (AI-assisted code). Verifying every suggested package
exists in its registry is required.

Decision: zero external dependencies. Only `argparse/json/re/sys/pathlib`
from stdlib. Import scan in `tests/unit/test_speclint.py` fails on any
non-stdlib import.

Consequences: `check:audit` is osv-scanner clean + pip-audit N/A;
no registry verification burden; future deps need T8 re-check.

## 2026-10-18 — Adapt de-slopped verbs minimally for CLI

Context: P7 verbs assume a service (`src.app` with `/livez`, `scripts/`,
image `service-starter:local`).

Decision: keep verb names + single gate + 1–3 line shell + no glue;
change only `dev` (CLI help), `test:e2e` (CLI fixture probes),
`build` image name (`speclint:local`), `check:sast` path (`src` only).

Consequences: `task verify` green for CLI; adaptations logged in friction
log; CB1–CB9 semantics unchanged.

## 2026-10-18 — No external binary in v0.1.0

Context: Y6/E4 fire only on external distribution.

Decision: release is git tag + source + local Docker image + sha256
manifest. No registry push, no store, no signed binary.

Consequences: Y6/E4 judged not fired (recorded in design); integrity via
checksums; if a binary ever leaves the team, Y6 signing + E4 provenance/SBOM
apply.
