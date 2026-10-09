# meta/

Ansible Galaxy metadata for the `gantsign.golang` role.

## Key Fields

- **min_ansible_version**: `2.17` — update this when dropping support for older Ansible versions
- **platforms**: lists supported distros/versions (EL 9, Ubuntu jammy/noble, Debian bullseye/bookworm, Fedora 41, openSUSE). Keep in sync with molecule scenarios
- **dependencies**: none

## When Adding Platform Support

1. Add the platform to `galaxy_info.platforms` in `main.yml`
2. Create a corresponding molecule scenario in `molecule/`
3. Add the scenario to the CI matrix in `.github/workflows/ci.yml`
