Ansible Role: Go language SDK
=============================

[![Tests](https://github.com/gantsign/ansible-role-golang/workflows/Tests/badge.svg)](https://github.com/gantsign/ansible-role-golang/actions?query=workflow%3ATests)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-gantsign.golang-blue.svg)](https://galaxy.ansible.com/gantsign/golang)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gantsign/ansible-role-golang/master/LICENSE)

Role to download and install the [Go language SDK](https://golang.org/).

Requirements
------------

* Ansible Core >= 2.17

* Linux Distribution

    * Debian Family

        * Debian

            * Bullseye (11)
            * Bookworm (12)

        * Ubuntu

            * Jammy (22.04)
            * Noble (24.04)

    * RedHat Family

        * Rocky Linux

            * 9

        * Fedora

            * 41

    * SUSE Family

        * openSUSE

            * Tumbleweed

    * Note: other versions are likely to work but have not been tested.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# Go language SDK version number ('latest' resolves the newest stable release
# at run time, or pin an explicit version such as '1.26.6')
golang_version: 'latest'

# Resolve the version and SHA256 checksum from the Go download API instead of
# the checked-in vars/versions/ table. Set to false for offline runs.
golang_use_download_api: true

# Go download API used to resolve versions and checksums
golang_releases_url: 'https://go.dev/dl/?mode=json&include=all'

# Mirror to download the Go language SDK redistributable package from
golang_mirror: 'https://dl.google.com/go'

# Base installation directory the Go language SDK distribution
golang_install_dir: '/opt/go/{{ golang_version_resolved }}'

# Directory to store files downloaded for Go language SDK installation
golang_download_dir: "{{ x_ansible_download_dir | default(ansible_facts.env.HOME + '/.ansible/tmp/downloads') }}"

# Location for GOPATH environment variable
golang_gopath:

# SHA256 sum of the redistributable package. Resolved automatically; only set
# this to override both the download API and the vars/versions/ table.
golang_redis_sha256sum:
```

`golang_version_resolved` is set by the role once `golang_version` has been
resolved to a concrete version; use it instead of `golang_version` when
referencing the installed version from your own templates.

### Architecture and checksum detection

The role detects the target's CPU architecture from `ansible_facts.architecture`
and maps it to the matching Go redistributable (`vars/architecture/`), then
resolves the SHA256 checksum **for that architecture**:

| Ansible architecture | Go redistributable |
|----------------------|--------------------|
| `x86_64`             | `amd64`            |
| `aarch64` / `arm64`  | `arm64`            |
| `armv6l` / `armv7l`  | `armv6l`           |
| `i386` / `i686`      | `386`              |
| `ppc64le`, `ppc64`, `s390x`, `riscv64`, `mips`, `mips64`, `mips64le` | same name |
| `loongarch64`        | `loong64`          |
| `mipsel`             | `mipsle`           |

Because both the version and the checksum are resolved at run time, **callers do
not need to specify `golang_version` or `golang_redis_sha256sum` at all** — the
same playbook installs the correct build on amd64, arm64 and everything else.
Hardcoding `golang_redis_sha256sum` in a playbook is in fact harmful: a role
parameter outranks the detected value, so an amd64 checksum passed that way
makes the download fail its integrity check on an arm64 host.

Resolution order for the checksum, highest priority first:

1. `golang_redis_sha256sum` passed explicitly by the caller.
2. The Go download API, for the resolved version and detected architecture.
3. `vars/versions/<version>-<arch>.yml` — the checked-in offline table.

If none apply, the role fails with a message naming the version and architecture
it could not resolve, rather than downloading the wrong artifact.

### Offline / air-gapped use

Set `golang_use_download_api: false` and pin `golang_version` to a version that
exists in `vars/versions/`. The static table is still maintained by
`add_new_versions.py` and covers amd64, arm64 and armv6l.

### Supported Go language SDK Versions

Any version published by the Go download API works out of the box. The versions
below additionally have checked-in checksums, so they also work with
`golang_use_download_api: false` (for other versions follow the Advanced
Configuration instructions):

* `1.27.1`
* `1.27.0`
* `1.26.8`
* `1.26.7`
* `1.26.6`
* `1.26.5`
* `1.26.4`
* `1.26.3`
* `1.26.2`
* `1.26.1`
* `1.26.0`
* `1.25.14`
* `1.25.13`
* `1.25.12`
* `1.25.11`
* `1.25.10`
* `1.25.9`
* `1.25.8`
* `1.25.7`
* `1.25.6`
* `1.25.5`
* `1.25.4`
* `1.25.3`
* `1.25.2`
* `1.25.1`
* `1.25.0`
* `1.24.13`
* `1.24.12`
* `1.24.11`
* `1.24.10`
* `1.24.9`
* `1.24.8`
* `1.24.7`
* `1.24.6`
* `1.24.5`
* `1.24.4`
* `1.24.3`
* `1.24.2`
* `1.24.1`
* `1.24.0`
* `1.23.12`
* `1.23.11`
* `1.23.10`
* `1.23.9`
* `1.23.8`
* `1.23.7`
* `1.23.6`
* `1.23.5`
* `1.23.4`
* `1.23.3`
* `1.23.2`
* `1.23.1`
* `1.23.0`
* `1.22.11`
* `1.22.10`
* `1.22.9`
* `1.22.8`
* `1.22.7`
* `1.22.6`
* `1.22.5`
* `1.22.4`
* `1.22.3`
* `1.22.2`
* `1.22.1`
* `1.22.0`
* `1.21.13`
* `1.21.12`
* `1.21.11`
* `1.21.10`
* `1.21.9`
* `1.21.8`
* `1.21.7`
* `1.21.6`
* `1.21.5`
* `1.21.4`
* `1.21.3`
* `1.21.2`
* `1.21.1`
* `1.21.0`
* `1.20.13`
* `1.20.12`
* `1.20.11`
* `1.20.10`
* `1.20.9`
* `1.20.8`
* `1.20.7`
* `1.20.6`
* `1.20.5`
* `1.20.4`
* `1.20.3`
* `1.20.2`
* `1.20.1`
* `1.20`
* `1.19.12`
* `1.19.11`
* `1.19.10`
* `1.19.9`
* `1.19.8`
* `1.19.7`
* `1.19.6`
* `1.19.5`
* `1.19.4`
* `1.19.3`
* `1.19.2`
* `1.19.1`
* `1.19`
* `1.18.10`
* `1.18.9`
* `1.18.8`
* `1.18.7`
* `1.18.6`
* `1.18.5`
* `1.18.4`
* `1.18.3`
* `1.18.2`
* `1.18.1`
* `1.18`
* `1.17.13`
* `1.17.12`
* `1.17.11`
* `1.17.10`
* `1.17.9`
* `1.17.8`
* `1.17.7`
* `1.17.6`
* `1.17.5`
* `1.17.4`
* `1.17.3`
* `1.17.2`
* `1.17.1`
* `1.17`
* `1.16.15`
* `1.16.14`
* `1.16.13`
* `1.16.12`
* `1.16.11`
* `1.16.10`
* `1.16.9`
* `1.16.8`
* `1.16.7`
* `1.16.6`
* `1.16.5`
* `1.16.4`
* `1.16.3`
* `1.16.2`
* `1.16.1`
* `1.16`
* `1.15.15`
* `1.15.14`
* `1.15.13`
* `1.15.12`
* `1.15.11`
* `1.15.10`
* `1.15.9`
* `1.15.8`
* `1.15.7`
* `1.15.6`
* `1.15.5`
* `1.15.4`
* `1.15.3`
* `1.15.2`
* `1.15.1`
* `1.15`
* `1.14.15`
* `1.14.14`
* `1.14.13`
* `1.14.12`
* `1.14.11`
* `1.14.10`
* `1.14.9`
* `1.14.8`
* `1.14.7`
* `1.14.6`
* `1.14.5`
* `1.14.4`
* `1.14.3`
* `1.14.2`
* `1.14.1`
* `1.14`
* `1.13.15`
* `1.13.14`
* `1.13.13`
* `1.13.12`
* `1.13.11`
* `1.13.10`
* `1.13.9`
* `1.13.8`
* `1.13.7`
* `1.13.6`
* `1.13.5`
* `1.13.4`
* `1.13.3`
* `1.13.2`
* `1.13.1`
* `1.13`
* `1.12.17`
* `1.12.16`
* `1.12.15`
* `1.12.14`
* `1.12.13`
* `1.12.12`
* `1.12.11`
* `1.12.10`
* `1.12.9`
* `1.12.8`
* `1.12.7`
* `1.12.6`
* `1.12.5`
* `1.12.4`
* `1.12.3`
* `1.12.2`
* `1.12.1`
* `1.12`
* `1.11.13`
* `1.11.12`
* `1.11.11`
* `1.11.10`
* `1.11.9`
* `1.11.8`
* `1.11.7`
* `1.11.6`
* `1.11.5`
* `1.11.4`
* `1.11.3`
* `1.11.2`
* `1.11.1`
* `1.11`
* `1.10.8`
* `1.10.7`
* `1.10.6`
* `1.10.5`
* `1.10.4`
* `1.10.3`
* `1.10.2`
* `1.10.1`
* `1.10`
* `1.9.7`
* `1.9.6`
* `1.9.5`
* `1.9.4`
* `1.9.3`
* `1.9.2`
* `1.9.1`
* `1.9`
* `1.8.7`
* `1.8.6`
* `1.8.5`
* `1.8.4`
* `1.8.3`
* `1.8.2`
* `1.8.1`
* `1.8`
* `1.7.4`
* `1.7.3`

Advanced Configuration
----------------------

You normally do not need anything here: the download API supplies the checksum
for any published version on the detected architecture.

Only when the API is unreachable **and** the version is missing from
`vars/versions/` do you need to supply the checksum yourself — and it must be
the checksum for the architecture you are targeting, i.e. for
`go{{ golang_version_resolved }}.linux-{{ golang_architecture }}.tar.gz`:

```yaml
# SHA256 sum for the redistributable package on THIS target's architecture
golang_redis_sha256sum: '6e3e9c949ab4695a204f74038717aa7b2689b1be94875899ac1b3fe42800ff82'
```

Do not set this in a playbook that runs against hosts of mixed architectures —
one hardcoded sum cannot be right for all of them.

Example Playbook
----------------

```yaml
- hosts: servers
  roles:
     - role: gantsign.golang
       golang_gopath: '$HOME/workspace-go'
```

Role Facts
----------

This role exports the following Ansible facts for use by other roles:

* `ansible_local.golang.general.version`

    * e.g. `1.7.3`

* `ansible_local.golang.general.home`

    * e.g. `/opt/golang/1.7.3`

More Roles From GantSign
------------------------

You can find more roles from GantSign on
[Ansible Galaxy](https://galaxy.ansible.com/ui/standalone/namespaces/2463/).

Development & Testing
---------------------

This project uses the following tooling:
* [Molecule](http://molecule.readthedocs.io/) for orchestrating test scenarios
* [Testinfra](http://testinfra.readthedocs.io/) for testing the changes on the
  remote
* [pytest](http://docs.pytest.org/) the testing framework
* [Tox](https://tox.wiki/en/latest/) manages Python virtual
  environments for linting and testing
* [pip-tools](https://github.com/jazzband/pip-tools) for managing dependencies

A Visual Studio Code
[Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) is
provided for developing and testing this role.

License
-------

MIT

Author Information
------------------

John Freeman

GantSign Ltd.
Company No. 06109112 (registered in England)
