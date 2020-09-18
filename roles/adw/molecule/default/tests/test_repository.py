"""Repo Tests"""
import pytest
from hamcrest import assert_that, contains_string

# pylint: disable=redefined-outer-name
@pytest.fixture()
def AnsibleVars(host):
    """Define AnsibleVars"""
    adw_role = "file=../../vars/main.yml name=adw_role"
    ansible_vars = host.ansible("include_vars", adw_role)["ansible_facts"]["adw_role"]
    return ansible_vars

def test_digital_workspace_context_200(host, AnsibleVars):
    "Check that /digital-workspace context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin http://{}:8080/digital-workspace".format(AnsibleVars["adw_host"]))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))
