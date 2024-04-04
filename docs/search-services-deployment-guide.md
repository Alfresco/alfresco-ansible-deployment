---
title: Deploying Alfresco Search services
---

# Deploying Alfresco Search services

Deploying Alfresco Search service or Insight Engine can be challenging at
times. There are situations where you might want to deploy this service on its
own, without deploying the full ACS platform. That may happen if your ACS
workload runs on kubernetes or if you want to prepare a new Search service
installation to run a big re-indexation while running normal operations on the
ACS platform.

In order to allow for such scenario, the `search` role within this playbook has
been made a bit more independent. The document below presents an example
playbook which tackles this use case and sets up Alfresco Search services in a
replication manner.

## License consideration

Remember that in order to install Search service on dedicated hosts, you need
to purchase a Search service license. If you're running community or do not have
a license, Search service must always be installed alongside ACS repository.

## Required inventory

While the `search` role do not have any **strong** requirement at the inventory
level, the playbook `playbooks/search_replication.yml` leverage the same
inventory structure the `playbooks/acs.yml`.
So if you use the playbook as-is, you'll need to give a list of hosts which
belong to the `search` group. Of course you can reuse the inventory of the main
playbook and simply add the search hosts you want to provision.

```yaml
all:
  children:
    search:
      search0.infra.local:
      search1.infra.local:
      search2.infra.local:
```

## Role parameters

Role's parameters are defined within the `roles/search/meta/argument_specs.yml`
file. Bellow we'll just expose the most common ones that may be useful for the
type of use-cases mentioned earlier.

- `search_shared_secret`: This parameter is the only one that's required and
  defines the shared secret used for repo<-->search authenticated communication.
  The `playbooks/search_replication.yml` playbook leverage the secrets
  configured as part of the main playbook. Refer to [secrets documentation](SECRETS.md)
  in order to know more.

- `search_topology`: defines the type of setup to deploy. Can be either
  `standalone` or `replication`. The playbook uses `replication`.

- `search_master_hostname`: gives the playbook the hostname or IP address of
  the master host, that read-replicas will poll for index updates.
  This parameter is only useful if the inventory hostname is not reachable by
  its name from other hosts.

- `alfresco.host`: defines the hostname or IP address of the repository to
  track.

- `alfresco.port`: defines the plain TCP port of the repository to track.

- `alfresco.port_ssl`: defines the encrypted TCP port of the repository to track.

In the playbook, role's parameters above are mapped within the playbook
variables:

- `search_shared_secret` <= `reposearch_shared_secret`

- `search_master_hostname` <= `solr_master_host`

- `alfresco.host` <= `ecmhost`

When running the example playbook you need to use the playbook variables.

## Using the Search replication playbook

Assuming the example playbook above, the command bellow will deploy replicated
Search service platform on 3 hosts, the first of which will be used as the
master (and is reachable by other hosts on the IP 192.168.0.56), and this
same host will be tracking the repo located at 192.168.0.138.

```sh
ansible-playbook -i inventory_ssh.yml playbooks/search_replication.yml \
    -K \
    -e ecm_host=192.168.0.138 \
    -e solr_master_host=192.168.0.56
```

## Further notes about setup

There are more actions required at that point to complete the installation:

- Configure ACS repo to use Solr6 index if not done already.

- Configure a load-balancer to route search requests to read-replicas

- Configure ACS to use the load-balancer as the search host.

> These actions bellow can be added to the playbook to match your own setup.
