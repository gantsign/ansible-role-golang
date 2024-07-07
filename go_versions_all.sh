#!/bin/bash

curl -s 'https://go.dev/dl/?mode=json&include=all' | jq -r '
[
  "Version", "Arch", "SHA256"
],
(
  .[] |
  .version as $version |
  .files[] |
  select(.os == "linux" and (.arch == "amd64" or .arch == "arm64" or .arch == "armv6l")) |
  [
    $version,
    .arch,
    .sha256
  ]
) | @tsv' | column -t
