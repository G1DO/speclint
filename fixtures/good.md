# Fixture good — minimal passing spec

## 1. Principles

P1. Smallest safe path.
P2. Depth follows risk.

## 2. Baseline

- B1 Path: define then build. Prevents skipping. Check: history shows order.
- B2 Brief: problem plus who. Prevents wrong thing. Check: brief first.

## 3. Triggered

| ID | Rule | Failure prevented | How to tell it was followed | Applies when | Source | Status |
|---|---|---|---|---|---|---|
| T1 | Check logins | Auth bypass | Threat model linked | Logins observed | Playbook | Proposed |
| B1 | Do path | Skipped steps | History shows order | Every project | Playbook | Proposed |
| B2 | Do brief | Wrong thing | Brief first | Every project | Playbook | Proposed |
