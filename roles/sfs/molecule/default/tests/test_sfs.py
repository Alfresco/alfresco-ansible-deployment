"""SFS Tests"""
import os
import pytest
from hamcrest import assert_that, contains_string

# pylint: disable=redefined-outer-name
@pytest.fixture()
def AnsibleVars(host):
    """Define AnsibleVars"""
    java_role = "file=../../../roles/java/vars/main.yml name=java_role"
    common_vars = "../../../common/vars/main.yml name=common_vars"
    common_defaults = "../../../common/defaults/main.yml name=common_defaults"
    common_hosts = "../../../common/vars/hosts.yml name=common_hosts"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_hosts)["ansible_facts"]["common_hosts"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    return ansible_vars

test_host = os.environ.get('TEST_HOST')

def test_sfs_service_is_running_and_enabled(host, AnsibleVars):
    """Check sfs service"""
    sfs = host.service("alfresco-shared-fs")
    assert_that(sfs.is_running)
    assert_that(sfs.is_enabled)

def test_sfs_log_exists(host, AnsibleVars):
    "Check that ats-shared-fs.log exists in /var/log/alfresco"
    assert_that(host.file("/var/log/alfresco/ats-shared-fs.log").exists)

def test_sfs_response(host, AnsibleVars):
    "Check that sfs context is available and returns a HTTP 200 status code"
    ready = host.run("curl -iL http://{}:8099/ready".format(test_host))
    live = host.run("curl -iL http://{}:8099/live".format(test_host))
    assert_that(ready.stdout, contains_string("HTTP/1.1 200"))
    assert_that(live.stdout, contains_string("HTTP/1.1 200"))

def test_environment_jvm_opts(host, get_ansible_vars):
    "Check that overwritten JVM_OPTS are taken into consideration"
    pid = host.run("/opt/openjdk*/bin/jps -lV | grep sfs | awk '{print $1}'")
    process_map = host.run("/opt/openjdk*/bin/jhsdb jmap --heap --pid {}".format(pid.stdout))
    assert_that(process_map.stdout, contains_string("MaxHeapSize              = 943718400 (900.0MB)"))