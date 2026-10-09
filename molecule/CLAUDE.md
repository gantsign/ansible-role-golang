# molecule/

Molecule test scenarios using Docker driver and testinfra verifier.

## Scenarios

| Scenario | Image | Purpose |
|---|---|---|
| `default` | `ubuntu:24.04` | Primary test — also holds shared converge.yml and tests |
| `ubuntu-min` | `ubuntu:22.04` | Minimum supported Ubuntu |
| `debian-max` | `debian:bookworm` | Latest Debian |
| `debian-min` | `debian:bullseye` | Oldest Debian |
| `rocky` | `rockylinux/rockylinux:9` | RHEL-compatible |
| `fedora` | `fedora:41` | Latest Fedora |
| `opensuse` | `opensuse/tumbleweed` | SUSE family |
| `ubuntu-arm32v7` | `ubuntu:24.04` (linux/arm/v7) | ARM 32-bit |
| `ubuntu-arm64v8` | `ubuntu:24.04` (linux/arm64) | ARM 64-bit |
| `ubuntu-max-go-eol` | `ubuntu:24.04` | Tests installing an older Go version (1.23.x) |

## Structure

Most scenarios reuse `default/converge.yml` and `default/tests/` via relative paths in their `molecule.yml`:
```yaml
provisioner:
  playbooks:
    converge: ../default/converge.yml
verifier:
  directory: ../default/tests
```

Only `default` and `ubuntu-max-go-eol` have their own converge and test files. The EOL scenario uses a different `golang_version` and its test assertions reference that version.

## Shared Files in `default/`

- **`converge.yml`** — applies the role with `golang_gopath: '$HOME/workspace-go'`, includes Fedora dnf5 workaround and post-tasks to install `which`/`aaa_base` for test dependencies
- **`tests/conftest.py`** — pytest fixture that skips tests outside molecule and configures testinfra hosts from `MOLECULE_INVENTORY_FILE`
- **`tests/test_role.py`** — verifies GOROOT, GOPATH, PATH env vars and that `go version` / `gofmt` work

## Running Tests

```bash
molecule test --scenario-name default     # single scenario
tox run -e ansible-max -- --scenario-name=rocky  # via tox with specific Ansible version
```

## When Bumping the Default Go Version

Update the hardcoded version in `default/tests/test_role.py` (lines referencing `/opt/go/X.Y.Z`).
