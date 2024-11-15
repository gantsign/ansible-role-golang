#!/usr/bin/env python3
import logging
import re
from pathlib import Path
from textwrap import dedent
from typing import Dict, List

import requests
from packaging.version import Version

# Constants
# https://pkg.go.dev/golang.org/x/website/internal/dl
GO_DOWNLOAD_URL = 'https://go.dev/dl/?mode=json&include=all'


def fetch_go_releases() -> List[Dict]:
    """Fetches all Go releases from the official Go API."""
    try:
        response = requests.get(GO_DOWNLOAD_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(
            f"Failed to fetch Go releases from {GO_DOWNLOAD_URL}: {e}")
        raise RuntimeError(f"Failed to fetch Go releases: {e}")

    releases = response.json()
    if not releases:
        raise ValueError("No releases found in the Go downloads API response.")

    return releases


def versions_from_releases(releases: List[Dict]) -> List[str]:
    """Extracts all stable Go versions from the releases data."""
    versions = [
        re.sub(r"^go", "", item['version'])
        for item in releases
        if item.get("stable", False)
    ]
    return sorted(set(versions), key=Version)


def query_local_versions() -> List[str]:
    """Gets local Go versions from checksum files."""

    versions_path = Path('vars/versions')
    if not versions_path.is_dir():
        raise FileNotFoundError(f"Directory {versions_path} does not exist.")

    version_pattern = re.compile(r'^(\d+\.\d+(?:\.\d+)?)')
    version_set = set()
    for filepath in versions_path.iterdir():
        filename = filepath.name
        if match := version_pattern.match(filename):
            version_set.add(match.group(1))

    return sorted(version_set, key=Version)


def get_minor_versions(versions: List[str]) -> List[str]:
    """Extracts minor versions (major.minor) from a list of versions."""
    minor_versions = {
        '.'.join(version.split('.')[:2]) for version in versions
    }
    return sorted(minor_versions, key=Version)


def filter_by_minor_version(
        target_minor_version: str,
        versions: List[str]) -> List[str]:
    """Filters versions by a specific minor version (major.minor)."""
    filter_version = Version(target_minor_version)
    return sorted(
        [
            version for version in versions
            if (parsed := Version(version)).major == filter_version.major and
            parsed.minor == filter_version.minor
        ],
        key=Version
    )


def write_checksum(version: str, arch: str, checksum: str) -> None:
    """Writes a checksum to a YAML file."""
    file_path = Path(f'vars/versions/{version}-{arch}.yml')
    logging.info(f'Writing: {file_path}')
    try:
        contents = dedent(f"""\
            ---
            # SHA256 sum for the redistributable package
            golang_redis_sha256sum: '{checksum}'
        """)
        file_path.write_text(contents)
    except IOError as e:
        logging.error(f"Error writing checksum file {file_path}: {e}")
        raise RuntimeError(f"Error writing checksum file {file_path}: {e}")


def write_checksums(version: str, release: Dict) -> None:
    """Writes checksums for a specific Go version release."""
    for file_info in release.get('files', []):
        os_name = file_info.get('os')
        kind = file_info.get('kind')
        arch = file_info.get('arch')
        if os_name == 'linux' and kind == 'archive' and arch in [
                'amd64', 'armv6l', 'arm64']:
            write_checksum(version, arch, file_info.get('sha256'))


def get_missing_versions(go_versions: List[str]) -> List[str]:
    """Identify missing Go versions compared to the local versions."""
    recent_go_minor_versions = get_minor_versions(go_versions)[-2:]

    # Query and process local versions
    local_versions = query_local_versions()
    recent_local_minor_versions = get_minor_versions(local_versions)[-2:]

    # Merge and sort unique minor versions
    merged_minor_versions = sorted(
        set(recent_go_minor_versions + recent_local_minor_versions),
        key=Version
    )

    # Function to identify missing versions for a given minor version
    def find_missing_versions(minor_version: str) -> List[str]:
        go_versions_for_minor = filter_by_minor_version(
            minor_version, go_versions)
        local_versions_for_minor = filter_by_minor_version(
            minor_version, local_versions)
        return list(set(go_versions_for_minor) - set(local_versions_for_minor))

    # Collect missing versions for all merged minor versions
    missing_versions = sorted(
        [
            version
            for minor_version in merged_minor_versions
            for version in find_missing_versions(minor_version)
        ],
        key=Version
    )
    return missing_versions


def add_missing_checksums() -> None:
    """Adds missing Go versions by downloading their checksums."""
    releases = fetch_go_releases()
    go_versions = versions_from_releases(releases)
    missing_versions = get_missing_versions(go_versions)
    if len(missing_versions) == 0:
        logging.info('No new versions found.')

    for version in missing_versions:
        for release in releases:
            if release['version'] == f'go{version}':
                write_checksums(version, release)
                break


def update_readme() -> None:
    """Updates the README file with the latest Go versions."""
    file_path = Path('README.md')

    try:
        content = file_path.read_text()
    except IOError as e:
        logging.error(f"Error reading {file_path}: {e}")
        raise

    local_versions = sorted(query_local_versions(), key=Version, reverse=True)
    if not local_versions:
        logging.error("No local versions found.")
        raise ValueError("No local versions found.")

    new_version = local_versions[0]

    version_pattern = re.compile(
        r"(?m)(?<=^golang_version:\s')\d+\.\d+(?:\.\d+)?(?=')")
    new_content = version_pattern.sub(new_version, content)
    formatted_versions = ''.join(
        f'* `{version}`\n' for version in local_versions)

    bullet_list_pattern = re.compile(
        r"(?m)^(\* `\d+\.\d+(?:\.\d+)?`(?:\n|$))+")
    new_content = bullet_list_pattern.sub(formatted_versions, new_content)

    if new_content != content:
        logging.info(f'Writing: {file_path}')
        file_path.write_text(new_content)


def update_vars() -> None:
    """Updates the Go version in the specified YAML file."""
    file_path = Path('defaults/main.yml')

    try:
        content = file_path.read_text()
    except IOError as e:
        logging.error(f"Error reading {file_path}: {e}")
        raise

    local_versions = query_local_versions()
    if not local_versions:
        logging.error("No local versions found.")
        raise ValueError("No local versions found.")

    new_version = local_versions[-1]

    version_var_pattern = re.compile(
        r"(?m)(?<=^golang_version:\s')\d+\.\d+(?:\.\d+)?(?=')")
    new_content = version_var_pattern.sub(new_version, content)

    if new_content != content:
        logging.info(f"Writing: {file_path}")
        file_path.write_text(new_content)


def update_tests() -> None:
    """Updates latest version number in the tests."""
    local_versions = query_local_versions()
    if not local_versions:
        logging.error("No local versions found.")
        raise ValueError("No local versions found.")

    new_version = local_versions[-1]

    file_path = Path('molecule/default/tests/test_role.py')
    try:
        content = file_path.read_text()
    except IOError as e:
        logging.error(f"Error reading {file_path}: {e}")
        raise

    # Regular expression to match version numbers like 1.0, 1.0.0, 10.2.3, etc.
    version_pattern = re.compile(r"\b\d+\.\d+(?:\.\d+)?\b")

    # Replace old version numbers with the new version
    new_content = version_pattern.sub(new_version, content)

    if new_content != content:
        logging.info(f'Writing: {file_path}')
        file_path.write_text(new_content)


def update_eol_tests() -> None:
    """Updates EOL tests and configurations with the latest EOL version."""
    local_versions = query_local_versions()
    if len(local_versions) < 2:
        logging.error("Not enough local versions to update EOL tests.")
        raise ValueError("Not enough local versions to update EOL tests.")

    local_minor_versions = get_minor_versions(local_versions)
    if len(local_minor_versions) < 2:
        logging.error("Not enough minor versions to determine EOL version.")
        raise ValueError("Not enough minor versions to determine EOL version.")

    eol_minor_version = local_minor_versions[-2]
    local_versions_for_minor = filter_by_minor_version(
        eol_minor_version, local_versions)
    eol_version = local_versions_for_minor[-1]

    test_file_path = Path('molecule/ubuntu-max-go-eol/tests/test_role.py')
    try:
        content = test_file_path.read_text()
    except IOError as e:
        logging.error(f"Error reading {test_file_path}: {e}")
        raise

    # Regular expression to match version numbers like 1.0, 1.0.0, 10.2.3, etc.
    version_pattern = re.compile(r"\b\d+\.\d+(?:\.\d+)?\b")

    # Replace old version numbers with the new version
    new_content = version_pattern.sub(eol_version, content)

    if new_content != content:
        logging.info(f'Writing: {test_file_path}')
        test_file_path.write_text(new_content)

    converge_file_path = Path('molecule/ubuntu-max-go-eol/converge.yml')

    try:
        content = converge_file_path.read_text()
    except IOError as e:
        logging.error(f"Error reading {converge_file_path}: {e}")
        raise

    # Regular expression to match version numbers like: golang_version: '1.0'
    version_property_pattern = re.compile(
        r"(?<=golang_version:\s')\d+\.\d+(?:\.\d+)?(?=')")

    # Replace old version numbers with the new version
    new_content = version_property_pattern.sub(eol_version, content)

    if new_content != content:
        logging.info(f'Writing: {converge_file_path}')
        converge_file_path.write_text(new_content)


def main() -> None:
    """Main function to fetch, update, and write Go versions."""
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    try:
        add_missing_checksums()
        update_readme()
        update_vars()
        update_tests()
        update_eol_tests()
        logging.info('Completed successfully.')
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise


if __name__ == '__main__':
    main()
