# templates/

Two Jinja2 templates, both using `{{ ansible_managed | comment('plain') }}` for the managed-by header.

## `golang.sh.j2`

Deployed to `/etc/profile.d/golang.sh`. Sets:
- `GOROOT` → `golang_install_dir`
- `PATH` → prepends `$GOROOT/bin`
- `GOPATH` + `$GOPATH/bin` on PATH (only if `golang_gopath` is set)

Sourced automatically by login shells.

## `facts.j2`

Deployed to `/etc/ansible/facts.d/golang.fact`. INI format exposing:
- `ansible_local.golang.general.version`
- `ansible_local.golang.general.home`

Used by downstream roles/playbooks to query the installed Go version.
