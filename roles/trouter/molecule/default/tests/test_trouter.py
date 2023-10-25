"""TRouter Tests"""
import os
import pytest
from hamcrest import assert_that, contains_string, has_length

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

def test_trouter_service_is_running_and_enabled(host):
    """Check trouter service"""
    trouter = host.service("alfresco-transform-router")
    assert_that(trouter.is_running)
    assert_that(trouter.is_enabled)

def test_trouter_log_exists(host, get_ansible_vars):
    "Check that ats-atr.log exists in /var/log/alfresco"
    with host.sudo(get_ansible_vars['username']):
        assert_that(host.file("/var/log/alfresco/ats-atr.log").exists)

def test_trouter_response(host):
    "Check that trouter context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL http://{}:8095/transform/config".format(test_host))
    http_response = host.run("curl -sL -w '%{http_code}' http://" + test_host + ":8095/transform/config -o /dev/null")
    assert_that(http_response.stdout, contains_string("200"))
    assert_that(cmd.stdout, contains_string("pdfRendererOptions"))
    assert_that(cmd.stdout, contains_string("archiveOptions"))
    assert_that(cmd.stdout, contains_string("imageMagickOptions"))
    assert_that(cmd.stdout, contains_string("tikaOptions"))
    assert_that(cmd.stdout, contains_string("pdfboxOptions"))
    assert_that(cmd.stdout, contains_string("textToPdfOptions"))
    assert_that(cmd.stdout, contains_string("stringOptions"))

def test_environment_jvm_opts(host):
    "Check that overwritten JVM_OPTS are taken into consideration"
    java_processes = host.process.filter(user="alfresco", comm="java")
    assert_that(java_processes, has_length(3))
    for java_process in java_processes:
        if 'alfresco-transform-router' in java_process.args:
            assert_that(java_process.args, contains_string('-Xmx900m'))
            assert_that(java_process.args, contains_string('-Xms800m'))

def test_no_ghostscript(host):
    host.run_expect([127], "gs")
    host.run_expect([127], "ghostscript")
