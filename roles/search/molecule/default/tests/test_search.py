"""Solr Tests"""
import os
import pytest
from hamcrest import contains_string, assert_that
from packaging import version

test_host = os.environ.get('TEST_HOST')


# pylint: disable=redefined-outer-name
@pytest.fixture(scope="module")
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    java_role = "file=../java/vars/main.yml name=java_role"
    common_vars = "file=../../../common/vars/main.yml name=common_vars"
    common_defaults = "file=../../../common/defaults/main.yml name=common_defaults"
    common_hosts = "file=../../../common/defaults/main.yml name=common_hosts"
    search_services = "file=../../vars/main.yml name=search_services"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_hosts)["ansible_facts"]["common_hosts"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    ansible_vars.update(host.ansible("include_vars", search_services)["ansible_facts"]["search_services"])
    return ansible_vars

def test_solr_log_exists(host, get_ansible_vars):
    """Check that solr log"""
    with host.sudo():
        assert_that(host.file("{}/solr.log".format(get_ansible_vars["logs_folder"])).exists, get_ansible_vars["logs_folder"])

@pytest.mark.parametrize("svc", ["alfresco-search"])
def test_search_service_running_and_enabled(host, svc):
    """Check alfresco-search service"""
    alfresco_search = host.service(svc)
    assert_that(alfresco_search.is_running)
    assert_that(alfresco_search.is_enabled)

def test_solr_stats_is_accessible(host):
    """Check that SOLR creates the alfresco and archive cores"""
    curl_opts = '-iL'
    search_env = host.ansible.get_variables()
    if version.parse(search_env['search']['version']) >= version.parse('2.0.3'):
        curl_opts += ' -H "X-Alfresco-Search-Secret: alfresco with space"'
    print("curl {} http://{}:8983/solr/#/~cores/alfresco".format(curl_opts, test_host))
    alfresco_core_command = host.run("curl {} http://{}:8983/solr/#/~cores/alfresco".format(curl_opts, test_host))
    archive_core_command = host.run("curl {} http://{}:8983/solr/#/~cores/archive".format(curl_opts, test_host))
    assert_that(alfresco_core_command.stdout, contains_string("HTTP/1.1 200"))
    assert_that(archive_core_command.stdout, contains_string("HTTP/1.1 200"))

def test_environment_jvm_opts(host):
    "Check that overwritten JVM_OPTS are taken into consideration"
    java_process = host.process.get(user="alfresco", comm="java")
    assert_that(java_process.args, contains_string('-Xmx900m'))
    assert_that(java_process.args, contains_string('-Xms700m'))
