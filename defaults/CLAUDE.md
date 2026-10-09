# defaults/

User-facing role variables. All are overridable by playbook consumers.

## Variables

| Variable | Default | Purpose |
|---|---|---|
| `golang_version` | `'latest'` | Go SDK version to install, or `latest` to resolve the newest stable release at run time |
| `golang_use_download_api` | `true` | Resolve version + checksum from the Go download API; set `false` for offline runs |
| `golang_releases_url` | `'https://go.dev/dl/?mode=json&include=all'` | The download API endpoint |
| `golang_mirror` | `'https://dl.google.com/go'` | Download mirror URL |
| `golang_install_dir` | `'/opt/go/{{ golang_version_resolved }}'` | Installation path (version-specific, allows side-by-side installs) |
| `golang_download_dir` | `x_ansible_download_dir` or `~/.ansible/tmp/downloads` | Temp download cache |
| `golang_gopath` | unset | If set, configures GOPATH env var and adds `$GOPATH/bin` to PATH |
| `golang_redis_sha256sum` | unset (`None`) | Resolved automatically per architecture; only set to override both the API and the static table |

## When Updating

The default is `latest`, so there is normally no version to bump. `add_new_versions.py` no longer rewrites `golang_version` here (its regex only matches a numeric version), which is intentional — the default should stay `latest`.

`molecule/default/tests/test_role.py` no longer hardcodes a version either; it reads the installed version back from `/etc/ansible/facts.d/golang.fact` so the default scenario keeps passing as new Go releases land. The `ubuntu-max-go-eol` scenario does pin a version, and `add_new_versions.py` still maintains that one.

## Gotcha

`golang_redis_sha256sum` is architecture-specific. Passing it as a role parameter overrides the detected value for **every** host in the play, which silently breaks any host that is not the architecture the sum came from. Leave it unset.
