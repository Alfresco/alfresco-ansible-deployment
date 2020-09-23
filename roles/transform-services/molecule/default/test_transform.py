"""Transform Tests"""
import time
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
    transform_services = "file=../../vars/main.yml name=transform_services"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_hosts)["ansible_facts"]["common_hosts"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    ansible_vars.update(host.ansible("include_vars", transform_services)["ansible_facts"]["transform_services"])
    return ansible_vars

def test_solr_log_exists(host, get_ansible_vars):
    "Check that solr log"
    assert_that(host.file("{}/solr.log".format(get_ansible_vars["logs_folder"])).exists, get_ansible_vars["logs_folder"])

@pytest.mark.parametrize("svc", ["solr"])
def test_solr_service_running_and_enabled(host, svc):
    """Check solr service"""
    solr = host.service(svc)
    assert_that(solr.is_running)
    assert_that(solr.is_enabled)

def test_solr_stats_is_accesible(host, get_ansible_vars):
    """Check solrstats service"""
    timeout = time.time() + 360
    output = None
    command = False
    while not command or time.time() < timeout:
        run_command = host.run("curl -v -k --connect-timeout 5 --user admin:admin http://{}:8080/alfresco/s/api/solrstats".format(get_ansible_vars["repo_host"]))
        command = run_command.succeeded
        output = run_command.stdout
    assert_that(output,contains_string("queryInfo"))
