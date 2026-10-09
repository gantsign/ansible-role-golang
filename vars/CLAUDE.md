# vars/

Internal role variables (not intended for user override).

## `main.yml`

Defines `golang_redis_filename` — the download filename template: `go{{ golang_version_resolved }}.linux-{{ golang_architecture }}.tar.gz`

Note it uses `golang_version_resolved` (set by `tasks/main.yml`), not `golang_version`, which may be the literal string `latest`.

## `architecture/`

Maps `ansible_facts.architecture` to Go's architecture name. Loaded via `first_found` in tasks.

| File | `ansible_facts.architecture` | `golang_architecture` |
|---|---|---|
| `default.yml` | anything unmapped (fallback) | `amd64` |
| `x86_64.yml` | x86_64 | `amd64` |
| `aarch64.yml` | aarch64 | `arm64` |
| `arm64.yml` | arm64 | `arm64` |
| `armv7l.yml` | armv7l | `armv6l` |
| `armv6l.yml` | armv6l | `armv6l` |
| `aarch64-32.yml` | aarch64 (32-bit userspace) | `armv6l` |
| `i386.yml`, `i686.yml` | i386 / i686 | `386` |
| `ppc64.yml`, `ppc64le.yml`, `s390x.yml`, `riscv64.yml`, `mips.yml`, `mips64.yml`, `mips64le.yml` | same | same |
| `loongarch64.yml` | loongarch64 | `loong64` |
| `mipsel.yml` | mipsel | `mipsle` |

`default.yml` mapping to `amd64` is a footgun for genuinely unmapped
architectures — it would download an amd64 tarball. That is why the explicit
files above exist for every architecture Go publishes a Linux archive for; add
a file rather than relying on the default.

## `versions/`

~543 YAML files containing SHA256 checksums. Each file has a single variable:
```yaml
golang_redis_sha256sum: '<sha256>'
```

**Naming convention:**
- `{version}-{arch}.yml` — architecture-specific checksum (e.g. `1.24.2-amd64.yml`, `1.24.2-arm64.yml`)
- `{version}.yml` — used by older versions that only had amd64 builds

Newer versions (1.24.x) have per-architecture files (`-amd64`, `-arm64`, `-armv6l`). Older versions (pre-1.10) typically have a single file for amd64 only.

**Do not hand-edit** — use `add_new_versions.py` at the repo root to generate these from the go.dev API.

These files are now the **offline fallback only**. By default the role queries
the go.dev API directly at run time (`golang_use_download_api: true`), so a
version missing from this directory still installs fine as long as the API is
reachable. The table matters for `golang_use_download_api: false`.
