# speclint

Stdlib-only CLI that lints `spec.md` structural rules (IDs, justified rows,
observable triggers, lane/tier bans, baseline size).

Docs: `docs/` in this repo.

## Run

```sh
python3 -m src.speclint --help
python3 -m src.speclint /path/to/spec.md
python3 -m src.speclint /path/to/spec.md --format json
```

## Verify

```sh
task verify
```

No undocumented setup. Tools are pinned in `.github/workflows/ci.yml`.
If a new binary leaves the team, checksums plus an expectation note will
ship with it; new binaries may warn until reputation accumulates.
