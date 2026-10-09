# requirements/

Python dependencies managed with pip-tools. Each `.in` file defines direct dependencies; `.txt` files are compiled with `--generate-hashes` for reproducible, verified installs.

## Files

| `.in` | Purpose |
|---|---|
| `ansible-min.in` | Pins minimum ansible-core (2.17.7) + molecule deps |
| `ansible-max.in` | Pins maximum ansible-core (2.18.1) + molecule deps |
| `molecule.in` | molecule, molecule-plugins[docker], pytest-testinfra |
| `lint.in` | ansible-lint, flake8, yamllint (pinned versions) |
| `tox.in` | tox (pinned version) |
| `dev.in` | Aggregates ansible-max + lint + tox + pip-tools |

## Recompiling

```bash
cd requirements && ./compile.sh
```

This runs `pip-compile --resolver=backtracking --generate-hashes` on all `.in` files and a hash-less compile for `dev.in`.

## When Updating Dependencies

Edit the `.in` file, then run `./compile.sh` to regenerate the `.txt`. Never hand-edit `.txt` files.
