---
title: Deploying Alfresco Connector for Content Intelligence
---

# Deploying Alfresco Connector for Content Intelligence

The *Alfresco Connector for Content Intelligence* (CIC) provides knowledge
retrieval capabilities by connecting your content repository, Alfresco Content
Services (ACS), to *Knowledge Discovery*. Knowledge Discovery allows you to
apply machine learning to your content repository.

The connector consists of three services:

* **Live Ingester** — ingests repository events in real time.
* **Bulk Ingester** — batch-ingests existing content from the repository
  database. It is installed as a `oneshot` service and is **not** started
  automatically; run it on demand for the initial load or to recover after
  downtime. It is only installed when the repository database is reachable.
* **Nucleus Sync** — synchronises Alfresco users and groups into Nucleus.
  Upstream marks this component as *not yet production-ready*; it is deployed
  and started by this role, but treat it as preview.

CIC requires **no ACS repository extension**: repository events are consumed
directly from the `alfresco.repo.event2` ActiveMQ topic.

You can get the most up-to-date product documentation for the `Alfresco
Connector` in the [Alfresco Connector for Content Intelligence
documentation](https://support.hyland.com/r/Alfresco/Alfresco-Connector-for-Content-Intelligence).

## Prerequisites

* Alfresco Content Services **Enterprise Edition** 7.4 or later (Community
  Edition is not supported)
* Active subscription and credentials for the Content Intelligence service

## Deployment Steps

1. Configure at least one host inside the `inventory` file for the `cic` group.
2. Provide your Content Intelligence credentials and related configuration
   parameters/URLs in the `vars/cic.yml` file.
3. Provide `cic_remote_client_secret` in the `vars/secrets.yml` file. Make sure
   to learn about [Ansible Vault
   integration](https://alfresco.github.io/alfresco-ansible-deployment/deployment-guide.html#secrets-management)
   if you are doing a production deployment.
4. Run the Ansible playbook as for a standard deployment. Please follow the
   [deployment
   guide](https://alfresco.github.io/alfresco-ansible-deployment/deployment-guide.html)
   for more details.

Any Alfresco Digital Workspace (ADW) UI configuration required to surface
Knowledge Discovery features is product- and version-specific — refer to the
[Content Intelligence documentation](https://support.hyland.com/r/Alfresco/Alfresco-Connector-for-Content-Intelligence).

## Verifying the Deployment

After the deployment is complete:

1. Check that the connector services are running:

   ```bash
   systemctl status alfresco-cic-connector-live-ingester
   systemctl status alfresco-cic-connector-nucleus-sync
   ```

   The bulk ingester is installed but not started; run it on demand:

   ```bash
   systemctl start alfresco-cic-connector-bulk-ingester
   ```

2. Create or update a document in the repository and check the ingestion logs:

   ```bash
   journalctl -u alfresco-cic-connector-live-ingester -f
   ```

## Source Code

The `cic_connector` Ansible role is available as part of the [Alfresco Platform
Collection](https://github.com/Alfresco/alfresco-ansible-collection).
