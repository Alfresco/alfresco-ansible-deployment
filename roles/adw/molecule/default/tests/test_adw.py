"""ADW Tests"""
import os
import pytest
from hamcrest import assert_that, contains_string

# pylint: disable=redefined-outer-name
@pytest.fixture(scope="module")
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    common_vars = "file=../common/vars/main.yml name=common_vars"
    common_hosts = "file=../common/defaults/main.yml name=common_hosts"
    ansible_vars = host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"]
    ansible_vars.update(host.ansible("include_vars", common_hosts)["ansible_facts"]["common_hosts"])
    return ansible_vars

test_host = os.environ.get('TEST_HOST')

def test_digital_workspace_200(host, get_ansible_vars):
    "Check that ADW is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin http://{}:8880/".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))
