"""Java Tests"""
import pytest
from hamcrest import contains_string, assert_that

# pylint: disable=redefined-outer-name
@pytest.fixture()
def get_ansible_vars(host):
    """Define AnsibleVars"""
    java_role = "file=../../../java/vars/main.yml name=java_role"
    tomcat_role = "file=../../vars/main.yml name=tomcat_role"
    common_vars = "file=../../../common/vars/main.yml name=common_vars"
    common_defaults = "file=../../../common/defaults/main.yml name=common_defaults"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", tomcat_role)["ansible_facts"]["tomcat_role"])
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    return ansible_vars


def test_java_home(host, get_ansible_vars):
    "Check that TOMCAT_HOME is environment variable is set"
    cmd = host.run("source {}/setenv.sh && echo $TOMCAT_HOME".format(get_ansible_vars["config_folder"]))
    assert_that(cmd.stdout, contains_string("apache-tomcat-{}".format(get_ansible_vars["tomcat_version"])))
