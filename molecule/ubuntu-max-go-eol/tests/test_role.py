import os
import pytest
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('name,pattern', [
    ('GOROOT', '^/opt/go/1.12.13$'),
    ('GOPATH', '^/root/workspace-go$'),
    ('PATH', '^(.+:)?/opt/go/1.12.13/bin(:.+)?$'),
    ('PATH', '^(.+:)?/root/workspace-go/bin(:.+)?$')
])
def test_go_env(host, name, pattern):
    cmd = host.run('. /etc/profile && printf $' + name)
    assert re.search(pattern, cmd.stdout)


def test_go(host):
    cmd = host.run('. /etc/profile && go version')
    assert cmd.rc == 0


@pytest.mark.parametrize('command', [
    'godoc',
    'gofmt'
])
def test_go_tools(host, command):
    cmd = host.run('. /etc/profile && which ' + command)
    assert cmd.rc == 0
