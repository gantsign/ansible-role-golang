import pytest
import re


@pytest.mark.parametrize('name,pattern', [
    ('GOROOT', '^/opt/go/1.15.6$'),
    ('GOPATH', '^/root/workspace-go$'),
    ('PATH', '^(.+:)?/opt/go/1.15.6/bin(:.+)?$'),
    ('PATH', '^(.+:)?/root/workspace-go/bin(:.+)?$')
])
def test_go_env(host, name, pattern):
    cmd = host.run('. /etc/profile && printf $' + name)
    assert re.search(pattern, cmd.stdout)


def test_go(host):
    cmd = host.run('. /etc/profile && go version')
    assert cmd.rc == 0


@pytest.mark.parametrize('command', [
    'gofmt'
])
def test_go_tools(host, command):
    cmd = host.run('. /etc/profile && which ' + command)
    assert cmd.rc == 0
