"""TRouter Tests"""
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

def test_trouter_service_is_running_and_enabled(host, AnsibleVars):
    """Check sfs service"""
    trouter = host.service("alfresco-transform-router")
    assert_that(trouter.is_running)
    assert_that(trouter.is_enabled)

def test_trouter_log_exists(host, AnsibleVars):
    "Check that ats-atr.log exists in /var/log/alfresco"
    assert_that(host.file("/var/log/alfresco/ats-atr.log").exists)

def test_trouter_response(host, AnsibleVars):
    "Check that sfs context is available and returns a HTTP 200 status code"
    cmd = host.run("curl -iL http://{}:8095/transform/config".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))
    assert_that(cmd.stdout, contains_string("pdfRendererOptions"))
    assert_that(cmd.stdout, contains_string("archiveOptions"))
    assert_that(cmd.stdout, contains_string("imageMagickOptions"))
    assert_that(cmd.stdout, contains_string("tikaOptions"))
    assert_that(cmd.stdout, contains_string("pdfboxOptions"))
    assert_that(cmd.stdout, contains_string("textToPdfOptions"))
    assert_that(cmd.stdout, contains_string("stringOptions"))
