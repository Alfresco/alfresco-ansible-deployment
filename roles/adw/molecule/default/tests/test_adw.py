"""Repo Tests"""
import pytest
from hamcrest import assert_that, contains_string

# pylint: disable=redefined-outer-name
@pytest.fixture()
def AnsibleVars(host):
    """Define AnsibleVars"""
    common_vars = "../../../common/vars/main.yml name=common_vars"
    common_hosts = "../../../common/vars/hosts.yml name=common_hosts"
    ansible_vars = host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"]
    ansible_vars.update(host.ansible("include_vars", common_hosts)["ansible_facts"]["common_hosts"])
    return ansible_vars

def test_digital_workspace_200(host, AnsibleVars):
    "Check that /digital-workspace context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin http://{}:8880/digital-workspace/".format(AnsibleVars["adw_host"]))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))
