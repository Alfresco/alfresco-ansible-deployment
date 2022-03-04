"""Transform Tests"""
import os
import pytest
from hamcrest import contains_string, assert_that

# pylint: disable=redefined-outer-name
@pytest.fixture(scope="module")
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    java_role = "file=../java/vars/main.yml name=java_role"
    common_vars = "file=../common/vars/main.yml name=common_vars"
    common_defaults = "file=../common/defaults/main.yml name=common_defaults"
    common_hosts = "file=../common/vars/hosts.yml name=common_hosts"
    transform_services = "file=./vars/main.yml name=transform_services"
    ansible_vars = host.ansible("include_vars", java_role)["ansible_facts"]["java_role"]
    ansible_vars.update(host.ansible("include_vars", java_role)["ansible_facts"]["java_role"])
    ansible_vars.update(host.ansible("include_vars", common_vars)["ansible_facts"]["common_vars"])
    ansible_vars.update(host.ansible("include_vars", common_hosts)["ansible_facts"]["common_hosts"])
    ansible_vars.update(host.ansible("include_vars", common_defaults)["ansible_facts"]["common_defaults"])
    ansible_vars.update(host.ansible("include_vars", transform_services)["ansible_facts"]["transform_services"])
    return ansible_vars

test_host = os.environ.get('TEST_HOST')

def test_aio_log_exists(host, get_ansible_vars):
    """Check that Transform AIO log exists"""
    assert_that(host.file("{}/ats-ate-aio.log".format(get_ansible_vars["logs_folder"])).exists, get_ansible_vars["logs_folder"])

def test_aio_service(host, get_ansible_vars):
    """Check that Transform AIO is enabled and running"""
    assert_that(host.service("alfresco-tengine-aio").is_running)
    assert_that(host.service("alfresco-tengine-aio").is_enabled)

def test_aio_config_api(host, get_ansible_vars):
    """Check that Transform AIO transform/config api works"""
    cmd = host.run("curl -iL http://{}:8090/transform/config".format(test_host))
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))
    assert_that(cmd.stdout, contains_string("pdfRendererOptions"))
    assert_that(cmd.stdout, contains_string("archiveOptions"))
    assert_that(cmd.stdout, contains_string("imageMagickOptions"))
    assert_that(cmd.stdout, contains_string("tikaOptions"))
    assert_that(cmd.stdout, contains_string("pdfboxOptions"))
    assert_that(cmd.stdout, contains_string("textToPdfOptions"))
    assert_that(cmd.stdout, contains_string("stringOptions"))

def test_aio_root_api(host, get_ansible_vars):
    """Check that Transform AIO root api works s"""
    cmd = host.run("curl -iL http://{}:8090".format(test_host))
    assert_that(cmd.stdout, contains_string("All in One Transformer Test Transformation"), cmd.stdout)
    assert_that(cmd.stdout, contains_string("HTTP/1.1 200"))

def test_environment_jvm_opts(host, get_ansible_vars):
    "Check that overwritten JVM_OPTS are taken into consideration"
    pid = host.run("/opt/openjdk*/bin/jps -lV | grep transform-core-aio | awk '{print $1}'")
    process_map = host.run("/opt/openjdk*/bin/jhsdb jmap --heap --pid {}".format(pid.stdout))
    assert_that(process_map.stdout, contains_string("MaxHeapSize              = 943718400 (900.0MB)"))
