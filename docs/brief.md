# Brief — speclint

Date: 2026-10-18. Repo: https://github.com/G1DO/speclint

## Problem

Manual C1/C2/C3/C8 checks on `spec.md` are grep-based, error-prone, and slow.
Every acceptance re-run hand-counts IDs, eyeballs Failure/How cells, and
searches lane/tier/freeze wording. A second person cannot re-check quickly.

## Who

Workflow maintainers (solo, G1DO). No external users. No auth, no personal
data, no payments, no persistent data, no versioned contract, no production
users, no loss-cost, no compliance obligation.

## Success number

`speclint spec.md` exits 0 on current `spec.md` v2 (39 unique IDs,
baseline 26 lines / 377 words / 1 page), exits 1 on each of 5 sabotage
fixtures, runs <2s on a clean checkout, zero external dependencies.

## Numbered reqs with acceptance

- REQ-1 Unique IDs: parse rule IDs (B1–B12, T1–T8, E1–E4, Y1–Y6, CB1–CB9),
  report duplicates, fail on duplicate. Acceptance: current spec 39 unique;
  fixture with duplicate B1 fails.
- REQ-2 Justified rows: every rule row has non-empty Failure prevented and
  How to tell / NEGATIVE TEST. Acceptance: fixture with empty Failure fails;
  current spec passes (30 + 9 rows non-empty).
- REQ-3 Observable triggers: every conditional Applies when names an
  observable fact, rejects easy/medium/hard/team-size. Acceptance: fixture
  with "easy" fails; current spec passes.
- REQ-4 No mandates: no mandating lane/tier/level-as-mandate/version-label/
  freeze (disclaimers, diagram-name mentions, and deletion notes excepted).
  Acceptance: fixture with "must follow lane gate" fails; current spec passes.
- REQ-5 Baseline size: report lines/words/chars + page estimate for §§1–2.
  Acceptance: current baseline 26 lines, 2491 chars, 377 words, 1 page Letter/A4.
- REQ-6 CLI shape: `python3 -m src.speclint SPEC [--format text|json]`,
  exit 0 pass / 1 fail, stdlib only, no network. Acceptance: `task test`
  green, `task verify` green, import scan shows stdlib only.

## Scope

CLI only. Stdlib only. No service, no DB, no auth, no contract, no prod,
no external binary distribution. Out of scope: PDF rendering, Notion fetch,
auto-fix, semgrep pinning.

## Risks with owners

- Markdown parsing brittle (owner: agent). Mitigation: fixtures + unit tests
  for each check; integration runs CLI on real spec.md.
- Semgrep `--config auto` drift (owner: agent). Mitigation: pinned CI
  (1.181.0) + `task verify` green before merge; S14 gap noted, not solved here.
- Scope creep into auto-fix (owner: G1DO). Mitigation: REQ list frozen for v0.1.0;
  extra ideas go to backlog.

## Repo link

https://github.com/G1DO/speclint — own repo, not `/home/thoth/workflow` skeleton.
Taskfile verbs + single gate copied from P7 shell-verbs branch
(`b78af2e798fc2499885023c1230e0ba93f18f28a`), adapted minimally for CLI
(dev/e2e/build image name/sast path — see friction log).
