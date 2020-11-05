"""SyncService Tests"""
import pytest
from hamcrest import contains_string, assert_that

# pylint: disable=redefined-outer-name
@pytest.fixture()
def get_ansible_vars(host):
    """Define AnsibleVars"""
    java_role = "file=../../../java/vars/main.yml name=java_role"
    common_vars = "file=../../../common/vars/main.yml name=common_vars"
    common_defaults = "file=../../../common/defaults/main.yml name=common_defaults"
    common_hosts = "file=../../../common/vars/hosts.yml name=common_hosts"
    syncservices = "file=../../vars/main.yml name=syncservices"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_hosts)["ansible_facts"]["common_hosts"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    ansible_vars.update(host.ansible("include_vars", syncservices)["ansible_facts"]["syncservices"])
    return ansible_vars

def test_sync_log_exists(host, get_ansible_vars):
    """Check that Sync Service log exists"""
    assert_that(host.file("{}/sync-service.log".format(get_ansible_vars["logs_folder"])).exists, get_ansible_vars["logs_folder"])

def test_sync_service(host, get_ansible_vars):
    "Check that Sync Service is enabled and running"
    assert_that(host.service("alfresco-sync").is_running)
    assert_that(host.service("alfresco-sync").is_enabled)

def test_sync_health(host, get_ansible_vars):
    """Check Sync Service health"""
    cmd = host.run("curl -iL http://{}:9090/alfresco/healthcheck".format(get_ansible_vars["sync_host"]))
    assert_that(cmd.stdout, contains_string("ActiveMQ connection Ok"))
    assert_that(cmd.stdout, contains_string("Database connection Ok"))
    assert_that(cmd.stdout, contains_string("Repository connection Ok"))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))
