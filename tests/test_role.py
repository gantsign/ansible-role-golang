import pytest
import re

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize('name,pattern', [
    ('GOROOT', '^/opt/go/1.10$'),
    ('GOPATH', '^/root/workspace-go$'),
    ('PATH', '^(.+:)?/opt/go/1.10/bin(:.+)?$'),
    ('PATH', '^(.+:)?/root/workspace-go/bin(:.+)?$')
])
def test_go_env(Command, name, pattern):
    cmd = Command('. /etc/profile && printf $' + name)
    assert re.search(pattern, cmd.stdout)


def test_go(Command):
    cmd = Command('. /etc/profile && go version')
    assert cmd.rc == 0


@pytest.mark.parametrize('command', [
    'godoc',
    'gofmt'
])
def test_go_tools(Command, command):
    cmd = Command('. /etc/profile && which ' + command)
    assert cmd.rc == 0
