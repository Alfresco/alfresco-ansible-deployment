"""Postgresql Tests"""
import pytest
from hamcrest import assert_that, contains_string

@pytest.fixture(scope="module")
def get_ansible_vars(host):
    """Define get_ansible_vars"""
    postgres_role_defaults = "file=../../defaults/main.yml name=postgres_role_defaults"
    ansible_vars = host.ansible("include_vars", postgres_role_defaults)["ansible_facts"]["postgres_role_defaults"]
    ansible_vars.update(host.ansible("include_vars", postgres_role_defaults)["ansible_facts"]["postgres_role_defaults"])
    return ansible_vars

def test_postgresql_service(host, get_ansible_vars):
    """Ensure postgres is up and basic functionality is working"""
    pghost = host.ansible.get_variables()['inventory_hostname']
    if not host.file('/etc/redhat-release').exists:
        service_name = 'postgresql'
    else:
        postgres_version = get_ansible_vars["postgres_major_version"]
        service_name = 'postgresql-{}'.format(postgres_version)

    assert_that(host.service(service_name).is_running)
    assert_that(host.service(service_name).is_enabled)

    with host.sudo('postgres'):
        # databases exists
        host.run_expect([0], "psql alfresco -c 'SELECT 1'")
        host.run_expect([0], "psql alfresco-sync -c 'SELECT 1'")

    host.run_expect([0], "PGPASSWORD=alfresco psql -h {} -U alfresco alfresco -c \"SELECT 1\"".format(pghost))
    host.run_expect([0], "PGPASSWORD=alfresco psql -h {} -U alfresco-sync alfresco-sync -c \"SELECT 1\"".format(pghost))

    # user can't connect to another user db remotely due to pg_hba
    host.run_expect([2], "PGPASSWORD=alfresco psql -h {} -U alfresco alfresco-sync -c \"SELECT 1\"".format(pghost))
    # but can connect to it locally
    host.run_expect([0], "PGPASSWORD=alfresco psql -h 127.0.0.1 -U alfresco alfresco-sync -c \"SELECT 1\"")
    # and it's fine because it cannot create objects inside it
    fail_create_table_output = host.run("PGPASSWORD=alfresco psql -h 127.0.0.1 -U alfresco alfresco-sync -c \"CREATE TABLE public.films (code char(5));\"")
    assert_that(fail_create_table_output.stderr, contains_string('permission denied for schema public'))
