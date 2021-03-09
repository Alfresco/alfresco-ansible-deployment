"""Java Tests"""
import pytest
from hamcrest import contains_string, assert_that

# pylint: disable=redefined-outer-name
@pytest.fixture()
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    java_role = "file=../../../java/vars/main.yml name=java_role"
    tomcat_role = "file=../../vars/main.yml name=tomcat_role"
    common_vars = "file=../../../common/vars/main.yml name=common_vars"
    common_defaults = "file=../../../common/defaults/main.yml name=common_defaults"
    group_vars = "../../../../group_vars/all.yml name=group_vars"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", tomcat_role)["ansible_facts"]["tomcat_role"])
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    ansible_vars.update(host.ansible("include_vars", group_vars)["ansible_facts"]["group_vars"])
    return ansible_vars

def test_tomcat_exe_exists(host, get_ansible_vars):
    "Check that Tomcat executable exists"
    assert_that(host.file("/opt/apache-tomcat-{}/bin/catalina.sh".format(get_ansible_vars["dependencies_version"]["tomcat"])).exists)

def test_tomcat_version(host, get_ansible_vars):
    "Check that Tomcat version is correct"
    cmd = host.run("source {}/setenv.sh && $TOMCAT_HOME/bin/catalina.sh version".format(get_ansible_vars["config_folder"]))
    assert_that(cmd.stdout, contains_string("Server version: Apache Tomcat/{}".format(get_ansible_vars["dependencies_version"]["tomcat"])))

def test_tomcat_home(host, get_ansible_vars):
    "Check that TOMCAT_HOME variable is set"
    cmd = host.run("source {}/setenv.sh && echo $TOMCAT_HOME".format(get_ansible_vars["config_folder"]))
    assert_that(cmd.stdout, contains_string("/opt/apache-tomcat-{}".format(get_ansible_vars["dependencies_version"]["tomcat"])))

def test_catalina_home(host, get_ansible_vars):
    "Check that CATALINA_HOME variable is set"
    cmd = host.run("sudo -u alfresco {}/tomcat.sh configtest".format(get_ansible_vars["binaries_folder"]))
    assert_that(cmd.stderr, contains_string("/opt/apache-tomcat-{}".format(get_ansible_vars["dependencies_version"]["tomcat"])))

def test_catalina_base(host, get_ansible_vars):
    "Check that CATALINA_BASE variable is set"
    cmd = host.run("sudo -u alfresco {}/tomcat.sh configtest".format(get_ansible_vars["binaries_folder"]))
    assert_that(cmd.stderr, contains_string("{}/tomcat".format(get_ansible_vars["config_folder"])))

def test_tomcat_service(host, get_ansible_vars):
    "Check that Tomcat is enabled and running"
    assert_that(host.service("alfresco-content").is_running)
    assert_that(host.service("alfresco-content").is_enabled)
