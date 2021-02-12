"""Nginx Tests"""
import os
import pytest
from hamcrest import contains_string, assert_that

# pylint: disable=redefined-outer-name
@pytest.fixture()
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    common_vars = "file=../../../common/vars/main.yml name=common_vars"
    common_defaults = "file=../../../common/defaults/main.yml name=common_defaults"
    nginx_vars = "file=../../vars/main.yml name=nginx_vars"
    ansible_vars = host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"]
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    ansible_vars.update(host.ansible("include_vars", nginx_vars)["ansible_facts"]["nginx_vars"])
    return ansible_vars

test_host = os.environ.get('TEST_HOST')

def test_selinux(host, get_ansible_vars):
    "Check that the selinux config is valid"
    virt_system = host.ansible("setup")["ansible_facts"]['ansible_virtualization_type']
    if virt_system != 'docker':
        cmd = host.run("sudo getsebool httpd_can_network_connect")
        assert_that(cmd, contains_string("{} syntax is ok".format(get_ansible_vars["nginx_conf_file_path"])))

def test_nginx_files_exist(host, get_ansible_vars):
    "Check that nginx file exist"
    assert_that(host.file("/usr/sbin/nginx").exists)
    assert_that(host.file(get_ansible_vars["nginx_conf_file_path"]).exists)

def test_nginx_version(host, get_ansible_vars):
    "Check that the version is valid"
    cmd = host.run("nginx -v")
    assert_that(cmd.stderr, contains_string("{}".format(get_ansible_vars["nginx_version"])))

def test_configuration_syntax(host, get_ansible_vars):
    "Check that the configuration is valid"
    cmd = host.run("nginx -t")
    assert_that(cmd.stderr, contains_string("{} syntax is ok".format(get_ansible_vars["nginx_conf_file_path"])))
    assert_that(cmd.stderr, contains_string("{} test is successful".format(get_ansible_vars["nginx_conf_file_path"])))

def test_nginx_secure_solr_path_1(host, get_ansible_vars):
    "Check that /.*/service/api/solr/.* is blocked and returns a HTTP 403 status code"
    cmd = host.run("curl -iL --connect-timeout 5 http://{}/alfresco/service/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

def test_nginx_secure_solr_path_2(host, get_ansible_vars):
    "Check that /.*/s/api/solr/.* is blocked and returns a HTTP 403 status code"
    cmd = host.run("curl -iL --connect-timeout 5 http://{}/alfresco/s/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

def test_nginx_secure_solr_path_3(host, get_ansible_vars):
    "Check that /.*/wcservice/api/solr/.* is blocked and returns a HTTP 403 status code"
    cmd = host.run("curl -iL --connect-timeout 5 http://{}/alfresco/wcservice/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

def test_nginx_secure_solr_path_4(host, get_ansible_vars):
    "Check that /.*/wcs/api/solr/.* is blocked and returns a HTTP 403 status code"
    cmd = host.run("curl -iL --connect-timeout 5 http://{}/alfresco/wcs/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

def test_nginx_secure_solr_path_5(host, get_ansible_vars):
    "Check that /.*/proxy/alfresco/api/solr/.* is blocked and returns a HTTP 403 status code"
    cmd = host.run("curl -iL --connect-timeout 5 http://{}/share/proxy/alfresco/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

def test_nginx_secure_solr_path_6(host, get_ansible_vars):
    "Check that /.*/proxy/alfresco/api/solr/.* is blocked and returns a HTTP 403 status code"
    cmd = host.run("curl -iL --connect-timeout 5 http://{}/share/proxy/alfresco-noauth/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

def test_nginx_secure_solr_path_7(host, get_ansible_vars):
    "Check that /.*/proxy/alfresco/api/solr/.* is blocked and returns a HTTP 403 status code"
    cmd = host.run("curl -iL --connect-timeout 5 http://{}/share/proxy/alfresco-feed/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

def test_nginx_secure_solr_path_8(host, get_ansible_vars):
    "Check that /.*/-default-/proxy/alfresco/api/.* is blocked and returns a HTTP 403 status code"
    cmd = host.run("curl -iL --connect-timeout 5 http://{}/alfresco/-default-/proxy/alfresco/api/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

def test_nginx_secure_prometheus_path(host, get_ansible_vars):
    "Check that /.*/s/prometheus is blocked and returns a HTTP 403 status code"
    cmd = host.run("curl -iL --connect-timeout 5 http://{}/alfresco/s/prometheus".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))
