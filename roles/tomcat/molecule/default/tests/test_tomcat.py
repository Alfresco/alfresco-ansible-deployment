"""Java Tests"""
import pytest
from hamcrest import contains_string, assert_that

# pylint: disable=redefined-outer-name
@pytest.fixture()
def get_ansible_vars(host):
    """Define AnsibleVars"""
    java_role = "file=../../vars/main.yml name=java_role"
    tomcat_role = "file=../../vars/main.yml name=tomcat_role"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", tomcat_role)["ansible_facts"]["tomcat_role"])
    return ansible_vars

def test_java_exists(host, get_ansible_vars):
    "Check that java executable exists"
    assert_that(host.file("/opt/openjdk-{}/bin/java".format(get_ansible_vars["jdk_version"])).exists, get_ansible_vars["jdk_version"])

def test_java_version(host, get_ansible_vars):
    "Check that java version is correct"
    cmd = host.run("/opt/openjdk-{}/bin/java -version".format(get_ansible_vars["jdk_version"]))
    assert_that(cmd.stderr, contains_string(get_ansible_vars["jdk_version"]))

def test_java_home(host, get_ansible_vars):
    "Check that TOMCAT_HOME is environment variable is set"
    cmd = host.run("source {}/setenv.sh && echo $TOMCAT_HOME".format(get_ansible_vars["config_dir"]))
    assert_that(cmd.stdout, contains_string("/apache-tomcat-{}".format(get_ansible_vars["tomcat_version"])))
