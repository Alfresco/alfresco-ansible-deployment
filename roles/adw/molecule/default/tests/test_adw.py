"""Repo Tests"""
import pytest
from hamcrest import assert_that, contains_string

# pylint: disable=redefined-outer-name
@pytest.fixture()
def AnsibleVars(host):
    """Define AnsibleVars"""
    common_vars = "../../../common/vars/main.yml name=common_vars"
    ansible_vars = host.ansible("include_vars", adw_role)["ansible_facts"]["common_vars"]
    return ansible_vars

def test_digital_workspace_200(host, AnsibleVars):
    "Check that /digital-workspace context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin http://{}:8880/".format(AnsibleVars["adw_host"]))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))
