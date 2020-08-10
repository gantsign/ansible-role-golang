Ansible Role: Go language SDK
=============================

Original role by John Freeman/gantsign - https://github.com/gantsign

This role has been updated with new features:
- only run the setup tasks when go is not installed or at a different version
- use tmp dir for download
- update molecule converge playbook to converge.yml
- use ansible to verify infrastructure
- added validation against directories that should not be cleaned up
- included testing for centos 8, debian buster, ubuntu focal fossa, fedora and suse.

<!-- [![Build Status](https://travis-ci.org/gantsign/ansible-role-golang.svg?branch=master)](https://travis-ci.org/gantsign/ansible-role-golang)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-gantsign.golang-blue.svg)](https://galaxy.ansible.com/gantsign/golang)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gantsign/ansible-role-golang/master/LICENSE) -->

Role to download and install the [Go language SDK](https://golang.org/).

Requirements
------------

* Ansible >= 2.9 (Might work on early versions)

* Linux Distribution

    * Debian Family

        * Debian

            * Jessie (8)
            * Stretch (9)
            * Buster (10)

        * Ubuntu

            * Xenial (16.04)
            * Bionic (18.04)
            * Focal Fossa (20.04)

    * RedHat Family

        * CentOS

            * 6
            * 7
            * 8

        * Fedora

            * 31
            * 32

    * SUSE Family

        * openSUSE

            * 15.1
            * 15.2

    * Note: other versions are likely to work but have not been tested.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
---
# Go language SDK version number
golang_version: '1.14.7'

# Mirror to download the Go language SDK redistributable package from
golang_mirror: 'https://storage.googleapis.com/golang'

# GOROOT / installation directory for the Go SDK
golang_install_dir: '/usr/local/go'

# Environment variable for GOPATH environment
golang_gopath:
```

The below variables are use when re-installing golang at the same version.
```yaml
---
# Cleanup golang GOROOT installation eg. '/usr/local/go'
golang_install_clean: false

# Cleanup golang GOPATH installation eg. '/home/user/go'
golang_install_clean_all: false
```

### Supported Go language SDK Versions

The following versions of Go language SDK are supported without any additional
configuration (for other versions follow the Advanced Configuration
instructions):

* `1.14.7`
* `1.13.15`


Advanced Configuration
----------------------

The following role variable is dependent on the Go language SDK version; to use
a Go language SDK version **not pre-configured by this role** you must configure
the variable below:

```yaml
# SHA256 sum for the redistributable package (i.e. "go{{ golang_version }}.linux-amd64.tar.gz")
golang_archive_sha256sum: '6e3e9c949ab4695a204f74038717aa7b2689b1be94875899ac1b3fe42800ff82'
```

Example Playbook
----------------

```yaml
- hosts: servers
  roles:
     - golang
```

Role Facts
----------

This role exports the following Ansible facts for use by other roles:

* `ansible_local.golang.general.version`

    * e.g. `1.14.7`

* `ansible_local.golang.general.home`

    * e.g. `/usr/local/go`

More Roles From GantSign
------------------------

You can find more roles from GantSign on
[Ansible Galaxy](https://galaxy.ansible.com/gantsign).

Development & Testing
---------------------

This project uses [Molecule](http://molecule.readthedocs.io/) to aid in the
development and testing; the role is unit tested using
[Testinfra](http://testinfra.readthedocs.io/) and
[pytest](http://docs.pytest.org/).

To develop or test you'll need to have installed the following:

* Linux (e.g. [Ubuntu](http://www.ubuntu.com/))
* [Docker](https://www.docker.com/)
* [Python](https://www.python.org/) (including python-pip)
* [Ansible](https://www.ansible.com/)
* [Molecule](http://molecule.readthedocs.io/)

Because the above can be tricky to install, this project includes
[Molecule Wrapper](https://github.com/gantsign/molecule-wrapper). Molecule
Wrapper is a shell script that installs Molecule and it's dependencies (apart
from Linux) and then executes Molecule with the command you pass it.

To test this role using Molecule Wrapper run the following command from the
project root:

```bash
./moleculew test
```

Note: some of the dependencies need `sudo` permission to install.

License
-------

MIT

Author Information
------------------

John Freeman

GantSign Ltd.
Company No. 06109112 (registered in England)
