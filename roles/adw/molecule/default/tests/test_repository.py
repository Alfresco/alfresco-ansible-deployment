"""Repo Tests"""
import pytest
from hamcrest import assert_that, contains_string

# pylint: disable=redefined-outer-name
@pytest.fixture()
def AnsibleVars(host):
    """Define AnsibleVars"""
    adw_role = "file=../../vars/main.yml name=adw_role"
    repository_role = "file=../../../roles/repository/vars/main.yml name=repository_role"
    tomcat_role = "file=../../../roles/tomcat/vars/main.yml name=tomcat_role"
    java_role = "file=../../../roles/java/vars/main.yml name=java_role"
    ansible_vars = host.ansible("include_vars", tomcat_role)["ansible_facts"]["tomcat_role"]
    ansible_vars.update(host.ansible("include_vars", adw_role)["ansible_facts"]["adw_role"])
    ansible_vars.update(host.ansible("include_vars", repository_role)["ansible_facts"]["repository_role"])
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    return ansible_vars

def test_share_context_200(host, AnsibleVars):
    "Check that /share context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin http://{}:8080/workspace".format(AnsibleVars["repository"]["host"]))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))
