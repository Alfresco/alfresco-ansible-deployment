"""Postgresql Tests"""
import os
from hamcrest import assert_that


def test_postgresql_service(host):
    """Ensure postgres is up and basic functionality is working"""
    pghost = host.ansible.get_variables()['inventory_hostname']
    if os.environ['TEST_IMAGE'].startswith('ubuntu'):
        service_name = 'postgresql'
    else:
        service_name = 'postgresql-13'

    assert_that(host.service(service_name).is_running)
    assert_that(host.service(service_name).is_enabled)

    with host.sudo('postgres'):
        # databases exists
        host.run_expect([0], "psql alfresco -c 'SELECT 1'")
        host.run_expect([0], "psql alfresco-sync -c 'SELECT 1'")

    host.run_expect([0], "PGPASSWORD=alfresco psql -h {} -U alfresco alfresco -c \"SELECT 1\"".format(pghost))
    host.run_expect([0], "PGPASSWORD=alfresco psql -h {} -U alfresco-sync alfresco-sync -c \"SELECT 1\"".format(pghost))

    # user can't connect to another user db remotely
    host.run_expect([2], "PGPASSWORD=alfresco psql -h {} -U alfresco alfresco-sync -c \"SELECT 1\"".format(pghost))
    # but can connect to it locally
    host.run_expect([0], "PGPASSWORD=alfresco psql -h 127.0.0.1 -U alfresco alfresco-sync -c \"SELECT 1\"")
    # and cannot create object inside it
    fail_create_table_output = host.run("PGPASSWORD=alfresco psql -h 127.0.0.1 -U alfresco alfresco-sync -c \"CREATE TABLE public.films (code char(5));\"")
    assert 'permission denied for schema public' in fail_create_table_output.stderr
