"""Repo Tests"""
import pytest
from hamcrest import assert_that, contains_string

# pylint: disable=redefined-outer-name
@pytest.fixture()
def AnsibleVars(host):
    """Define AnsibleVars"""
    repository_role = "file=../../vars/main.yml name=repository_role"
    tomcat_role = "file=../../../roles/tomcat/vars/main.yml name=tomcat_role"
    java_role = "file=../../../roles/java/vars/main.yml name=java_role"
    common_vars = "../../../common/vars/main.yml name=common_vars"
    common_defaults = "../../../common/defaults/main.yml name=common_defaults"
    common_hosts = "../../../common/vars/hosts.yml name=common_hosts"
    ansible_vars = host.ansible("include_vars", tomcat_role)["ansible_facts"]["tomcat_role"]
    ansible_vars.update(host.ansible("include_vars", repository_role)["ansible_facts"]["repository_role"])
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_hosts)["ansible_facts"]["common_hosts"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    return ansible_vars

def test_repo_service_is_running_and_enabled(host, AnsibleVars):
    """Check repository service"""
    repository = host.service("alfresco-content.service")
    assert_that(repository.is_running)
    assert_that(repository.is_enabled)

def test_alfresco_log_exists(host, AnsibleVars):
    "Check that alfresco.log exists in /var/log/alfresco"
    assert_that(host.file("/var/log/alfresco/alfresco.log").exists)

def test_alfresco_context_200(host, AnsibleVars):
    "Check that /alfresco context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin http://{}:8080/alfresco".format(AnsibleVars["repo_host"]))
    assert_that(cmd.stdout, contains_string("Welcome to Alfresco"), AnsibleVars["repo_host"])
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))

def test_alfresco_api(host, AnsibleVars):
    "Check the repository is installed correctly by calling the discovery API (/alfresco/api/discovery)"
    cmd = host.run("curl -iL --user admin:admin http://{}:8080/alfresco/api/discovery".format(AnsibleVars["repo_host"]))
    assert_that(cmd.stdout, contains_string(AnsibleVars["alfresco"]["version"]))

def test_share_log_exists(host, AnsibleVars):
    "Check that share.log exists in /var/log/alfresco"
    assert_that(host.file("/var/log/alfresco/share.log").exists)

def test_share_context_200(host, AnsibleVars):
    "Check that /share context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin http://{}:8080/share".format(AnsibleVars["repo_host"]))
    assert_that(cmd.stdout, contains_string("Alfresco Share"))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))

def test_api_explorer_context_200(host, AnsibleVars):
    "Check that /api-explorer context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL --user admin:admin http://{}:8080/api-explorer".format(AnsibleVars["repo_host"]))
    assert_that(cmd.stdout, contains_string("Alfresco Content Services REST API Explorer"))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))