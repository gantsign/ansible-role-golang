# tasks/

Single file: `main.yml` — the full role execution in order.

## Task Flow

1. **Load architecture vars** — `include_vars` with `first_found` from `vars/architecture/`, maps `ansible_facts.architecture` to Go's arch naming (e.g. `aarch64` → `arm64`)
2. **Query the download API** — `uri` GET of `golang_releases_url`; `ignore_errors: true` so an unreachable API degrades to the static table instead of failing the run
3. **Resolve version + checksum** — `set_fact` picks the newest stable release when `golang_version: latest`, then selects the `linux`/`archive` file matching `golang_architecture` and takes its `sha256`
4. **Fall back to the pinned version** — sets `golang_version_resolved` from `golang_version` when the API was skipped or did not resolve
5. **Assert a concrete version** — fails with a targeted message if `latest` could not be resolved
6. **Load version vars** — `include_vars` with `first_found` from `vars/versions/`, **only when no checksum is set yet**; the offline fallback
7. **Assert checksum** — fails the role if `golang_redis_sha256sum` is empty/undefined
8. **Create download dir** — `golang_download_dir`
9. **Download Go SDK** — `get_url` from mirror with `sha256:` checksum verification, `force: false` (skip if cached)
10. **Create install dir** — `/opt/go/{version}` as root
11. **Install unarchive deps** — `gzip` + `tar` on zypper-only systems
12. **Extract** — `unarchive` with `--strip-components=1` and `creates:` guard on `{install_dir}/bin`
13. **Template env vars** — `/etc/profile.d/golang.sh` (GOROOT, PATH, optional GOPATH)
14. **Template facts** — `/etc/ansible/facts.d/golang.fact` (exposes `ansible_local.golang.general.version` and `.home`)
15. **Re-read facts** — `setup` filter to refresh `ansible_local`

## Key Patterns

- **`golang_version_resolved`, not `golang_version`.** Everything downstream (filename, install dir, facts template) references the resolved fact, because `golang_version` may literally be the string `latest`. A separate name is also required for precedence reasons: a caller passing `golang_version` as a role parameter outranks any `set_fact`, so the role cannot overwrite it in place.
- **The static table is a fallback, not the primary source.** Step 6 is guarded by `when: golang_redis_sha256sum | default('', true) | length == 0`. Do not rely on documented variable precedence to order it against step 3 — `include_vars` and `set_fact` both write to the same non-persistent fact namespace, so between those two it is last-write-wins, not precedence.
- Use `default('', true)` rather than `default('')` when testing that checksum: `defaults/main.yml` defines it as an explicit `None`, which `default('')` does not catch.
- `first_found` cascades: specific arch → general → default. This means version files can be per-architecture (`1.24.2-arm64.yml`) or shared (`1.10.3.yml` for amd64-only older versions).
- `creates:` on the unarchive step makes re-runs idempotent without re-extracting.
- `when: not ansible_check_mode` guards download and extract steps since they need actual files.
