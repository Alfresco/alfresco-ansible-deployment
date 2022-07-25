"""Postgresql Tests"""
import os
from hamcrest import assert_that, contains_string


def test_postgresql_service(host):
    """Ensure postgres is up and basic functionality is working"""
    pghost = host.ansible.get_variables()['inventory_hostname']
    if os.environ['TEST_IMAGE'].startswith('ubuntu'):
        service_name = 'postgresql'
    else:
        postgres_version = host.ansible.get_variables()['dependencies_version']['postgres_major_version']
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
