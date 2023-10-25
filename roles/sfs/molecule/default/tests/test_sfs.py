"""SFS Tests"""
import os
import pytest
from hamcrest import assert_that, contains_string

test_host = os.environ.get('TEST_HOST')


# pylint: disable=redefined-outer-name
@pytest.fixture(scope="module")
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    java_role = "file=../roles/java/vars/main.yml name=java_role"
    common_vars = "file=../../../common/vars/main.yml name=common_vars"
    common_defaults = "file=../../../common/defaults/main.yml name=common_defaults"
    common_hosts = "file=../../../common/vars/hosts.yml name=common_hosts"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_hosts)["ansible_facts"]["common_hosts"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    return ansible_vars

def test_sfs_service_is_running_and_enabled(host):
    """Check sfs service"""
    sfs = host.service("alfresco-shared-fs")
    assert_that(sfs.is_running)
    assert_that(sfs.is_enabled)

def test_sfs_log_exists(host, get_ansible_vars):
    "Check that ats-shared-fs.log exists in /var/log/alfresco"
    with host.sudo(get_ansible_vars['username']):
        assert_that(host.file("/var/log/alfresco/ats-shared-fs.log").exists)

def test_sfs_response(host):
    "Check that sfs context is available and returns a HTTP 200 status code"
    ready = host.run("curl -iL http://{}:8099/ready".format(test_host))
    live = host.run("curl -iL http://{}:8099/live".format(test_host))
    assert_that(ready.stdout, contains_string("HTTP/1.1 200"))
    assert_that(live.stdout, contains_string("HTTP/1.1 200"))

def test_environment_jvm_opts(host):
    "Check that overwritten JVM_OPTS are taken into consideration"
    java_process = host.process.get(user="alfresco", comm="java")
    assert_that(java_process.args, contains_string('-Xmx900m'))
    assert_that(java_process.args, contains_string('-Xms128m'))
