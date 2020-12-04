Ansible Role: Go language SDK
=============================

[![Tests](https://github.com/gantsign/ansible-role-golang/workflows/Tests/badge.svg)](https://github.com/gantsign/ansible-role-golang/actions?query=workflow%3ATests)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-gantsign.golang-blue.svg)](https://galaxy.ansible.com/gantsign/golang)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gantsign/ansible-role-golang/master/LICENSE)

Role to download and install the [Go language SDK](https://golang.org/).

Requirements
------------

* Ansible >= 2.8

* Linux Distribution

    * Debian Family

        * Debian

            * Jessie (8)
            * Stretch (9)

        * Ubuntu

            * Xenial (16.04)
            * Bionic (18.04)

    * RedHat Family

        * CentOS

            * 7
            * 8

        * Fedora

            * 31

    * SUSE Family

        * openSUSE

            * 15.1

    * Note: other versions are likely to work but have not been tested.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# Go language SDK version number
golang_version: '1.15.6'

# Mirror to download the Go language SDK redistributable package from
golang_mirror: 'https://storage.googleapis.com/golang'

# Base installation directory the Go language SDK distribution
golang_install_dir: '/opt/go/{{ golang_version }}'

# Directory to store files downloaded for Go language SDK installation
golang_download_dir: "{{ x_ansible_download_dir | default(ansible_env.HOME + '/.ansible/tmp/downloads') }}"

# Location for GOPATH environment variable
golang_gopath:
```

### Supported Go language SDK Versions

The following versions of Go language SDK are supported without any additional
configuration (for other versions follow the Advanced Configuration
instructions):

* `1.15.6`
* `1.15.5`
* `1.15.4`
* `1.15.3`
* `1.15.2`
* `1.15.1`
* `1.15`
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

The following role variable is dependent on the Go language SDK version; to use
a Go language SDK version **not pre-configured by this role** you must configure
the variable below:

```yaml
# SHA256 sum for the redistributable package (i.e. "go{{ golang_version }}.linux-amd64.tar.gz")
golang_redis_sha256sum: '6e3e9c949ab4695a204f74038717aa7b2689b1be94875899ac1b3fe42800ff82'
```

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
