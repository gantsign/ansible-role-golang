#!/bin/bash

curl -s 'https://go.dev/dl/?mode=json' | jq -r '
["amd64", "arm64", "armv6l", "ppc64", "ppc64le"] as $supported_arches |
[
  "Version", "Arch", "SHA256"
],
(
  .[] |
  .version as $version |
  .files[] |
  select(.os == "linux" and (.arch as $this_arch | $supported_arches | index($this_arch))) |
  [
    $version,
    .arch,
    .sha256
  ]
) | @tsv' | column -t
