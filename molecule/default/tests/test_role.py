import pytest
import re


def installed_version(host):
    """Version the role actually installed, per the facts file it writes.

    The default scenario uses golang_version: latest, so the expected version
    is not knowable ahead of time and is read back from the role's own output.
    """
    facts = host.file('/etc/ansible/facts.d/golang.fact').content_string
    match = re.search(r'^version=(\S+)$', facts, re.MULTILINE)
    assert match, 'no version recorded in /etc/ansible/facts.d/golang.fact'
    return match.group(1)


@pytest.mark.parametrize('name,template', [
    ('GOROOT', '^/opt/go/{version}$'),
    ('GOPATH', '^/root/workspace-go$'),
    ('PATH', '^(.+:)?/opt/go/{version}/bin(:.+)?$'),
    ('PATH', '^(.+:)?/root/workspace-go/bin(:.+)?$')
])
def test_go_env(host, name, template):
    pattern = template.format(version=re.escape(installed_version(host)))
    cmd = host.run('. /etc/profile && printf $' + name)
    assert re.search(pattern, cmd.stdout)


def test_go(host):
    cmd = host.run('. /etc/profile && go version')
    assert cmd.rc == 0


def test_go_version_matches_facts(host):
    """The binary runs on this architecture and is the version we resolved."""
    cmd = host.run('. /etc/profile && go version')
    assert cmd.rc == 0
    assert 'go' + installed_version(host) in cmd.stdout


@pytest.mark.parametrize('command', [
    'gofmt'
])
def test_go_tools(host, command):
    cmd = host.run('. /etc/profile && which ' + command)
    assert cmd.rc == 0
