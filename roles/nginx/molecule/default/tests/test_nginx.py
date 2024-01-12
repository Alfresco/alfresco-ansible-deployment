"""Nginx Tests"""
import os
import pytest
from hamcrest import contains_string, assert_that

test_host = os.environ.get('TEST_HOST')


# pylint: disable=redefined-outer-name
@pytest.fixture(scope="module")
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    common_vars = "file=../../../common/vars/main.yml name=common_vars"
    common_defaults = "file=../../../common/defaults/main.yml name=common_defaults"
    nginx_vars = "file=../../vars/main.yml name=nginx_vars"
    distribution_name = host.ansible("setup")["ansible_facts"]["ansible_distribution"]
    distribution_version = host.ansible("setup")["ansible_facts"]["ansible_distribution_version"]
    nginx_dist_version_vars = "file=../../vars/{}{}.yml name=nginx_dist_version_vars".format(distribution_name, distribution_version)
    nginx_osfam_vars = "file=../../vars/" + host.ansible("setup")["ansible_facts"]["ansible_os_family"] + ".yml name=nginx_osfam_vars"
    ansible_vars = host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"]
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    ansible_vars.update(host.ansible("include_vars", nginx_vars)["ansible_facts"]["nginx_vars"])
    ansible_vars.update(host.ansible("include_vars", nginx_osfam_vars)["ansible_facts"]["nginx_osfam_vars"])
    ansible_vars.update(host.ansible("include_vars", nginx_dist_version_vars)["ansible_facts"]["nginx_dist_version_vars"])
    return ansible_vars

def test_selinux(host):
    """Check that the selinux config is valid"""
    selinux_status = host.ansible("setup")["ansible_facts"]["ansible_selinux"]["status"]
    if selinux_status != 'disabled':
        cmd = host.run("getsebool httpd_can_network_connect")
        assert_that(cmd, contains_string("--> off"))

def test_nginx_configuration(host, get_ansible_vars):
    """Check that nginx configuration exists and that is valid"""
    assert_that(host.file("/usr/sbin/nginx").exists)
    assert_that(host.file(get_ansible_vars["nginx_conf_file_path"]).exists)

    with host.sudo():
        cmd = host.run("nginx -t")
    assert_that(cmd.stderr, contains_string("{} syntax is ok".format(get_ansible_vars["nginx_conf_file_path"])))
    assert_that(cmd.stderr, contains_string("{} test is successful".format(get_ansible_vars["nginx_conf_file_path"])))

def test_nginx_secure_solr_paths(host):
    """Check that different solr http endpoints are blocked and returns 403"""
    cmd = host.run("curl -iL --connect-timeout 5 http://{}/alfresco/service/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

    cmd = host.run("curl -iL --connect-timeout 5 http://{}/alfresco/s/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

    cmd = host.run("curl -iL --connect-timeout 5 http://{}/alfresco/wcservice/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

    cmd = host.run("curl -iL --connect-timeout 5 http://{}/alfresco/wcs/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

    cmd = host.run("curl -iL --connect-timeout 5 http://{}/share/proxy/alfresco/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

    cmd = host.run("curl -iL --connect-timeout 5 http://{}/share/proxy/alfresco-noauth/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

    cmd = host.run("curl -iL --connect-timeout 5 http://{}/share/proxy/alfresco-feed/api/solr/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

    cmd = host.run("curl -iL --connect-timeout 5 http://{}/alfresco/-default-/proxy/alfresco/api/test".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))

def test_nginx_secure_prometheus_path(host):
    """Check that /.*/s/prometheus is blocked and returns a HTTP 403 status code"""
    cmd = host.run("curl -iL --connect-timeout 5 http://{}/alfresco/s/prometheus".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 403"))
