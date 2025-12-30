Ansible Role: Go language SDK (minimal)
======================================

Role to download and install the Go language SDK with only the essentials left
in place.

Requirements
------------

* Ansible Core >= 2.17
* Tested platforms: Debian 13 (amd64, arm64) and Ubuntu 24.04 (amd64, arm64)

Role Variables
--------------

```yaml
# Go language SDK version number (pre-configured checksums are kept only for this release)
golang_version: '1.25.5'

# Mirror to download the Go language SDK redistributable package from
golang_mirror: 'https://go.dev/dl'

# Base installation directory the Go language SDK distribution
golang_install_dir: '/opt/go/{{ golang_version }}'

# Directory to store files downloaded for Go language SDK installation
golang_download_dir: "{{ x_ansible_download_dir | default(ansible_facts.env.HOME + '/.ansible/tmp/downloads') }}"

# Location for GOPATH environment variable
golang_gopath:
```

Supported Go Versions
---------------------

Checksums are provided for Go `1.25.5` (amd64 and arm64). For any other
version, set `golang_version` and provide the matching `golang_redis_sha256sum`.

```yaml
# SHA256 sum for the redistributable package (i.e. "go{{ golang_version }}.linux-amd64.tar.gz")
golang_redis_sha256sum: '9e9b755d63b36acf30c12a9a3fc379243714c1c6d3dd72861da637f336ebb35b'
```

Example Playbook
----------------

```yaml
- hosts: servers
  roles:
    - role: ansible-role-golang
      golang_gopath: '$HOME/workspace-go'
```

Testing
-------

A single Molecule scenario (`molecule/default`) runs against Debian 13 and
Ubuntu 24.04 for both amd64 and arm64.

License
-------

MIT

Author Information
------------------

Originally by John Freeman / GantSign Ltd.
