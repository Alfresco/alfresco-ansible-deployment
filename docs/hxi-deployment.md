---
title: Deploying Alfresco Connector for Content Intelligence
---

The Alfresco Connector for Content Intelligence (also referred to as the
HxInsight Connector inside the provided Ansible playbooks) provides knowledge
retrieval capabilities by connecting your content repository, Alfresco Content
Services (ACS), to Knowledge Discovery. Knowledge Discovery allows you to apply
machine learning to your content repository.

You can get the most up-to-date product documentation for the `Alfresco
Connector` in the [Content Intelligence
Documentation](https://support.hyland.com/p/contentintel).

## Prerequisites

* Alfresco Content Services Enterprise (ACS) 23 or later
* Active subscription and credentials for Content Intelligence service

## Deployment Steps

1. Configure at least one host inside the `inventory` file for the `hxi` group.
2. Provide your Content Intelligence credentials and related configuration
   parameters/URLs in the `vars/hxi.yml` file.
3. Provide `hxi_remote_client_secret` in the `vars/secrets.yml` file. Make sure
   to learn about [Ansible Vault
   integration](https://alfresco.github.io/alfresco-ansible-deployment/deployment-guide.html#secrets-management)
   if you are doing a production deployment.
4. Enable knowledge discovery plugin in ADW by setting in `playbooks/group_vars/adw.yml`:

   ```yaml
   adw_app_configuration:
     plugins:
       knowledgeRetrievalEnabled: true
   ```

5. Run the Ansible playbook as for a standard deployment. Please follow the
   [deployment
   guide](https://alfresco.github.io/alfresco-ansible-deployment/deployment-guide.html)
   for more details.

## Verifying the Deployment

After the deployment is complete:

1. Log into ADW and verify that the `Ask Discovery` button is available in the main view
2. Check that both connector services are running:

   ```bash
   systemctl status alfresco-hxinsight-connector-live-ingester
   ```

3. Upload a document with ADW and check the ingestion logs:

   ```bash
   journalctl -u alfresco-hxinsight-connector-live-ingester -f
   ```
