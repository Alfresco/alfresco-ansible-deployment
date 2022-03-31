# Secrets

This page describe which secrets and how they can be managed in our playbook.

Links to the official documentation relevant for this subject:

* [Alfresco Authorization](https://docs.alfresco.com/content-services/latest/admin/security/)

## Secrets defined as variables

### activemq_password

The password used to access the activemq instance.

### repo_db_password

The password used to access the postgres database of Repository

### sync_db_password

The password used to access the postgres database of Sync

### reposearch_shared_secret

The secret used between Solr and Repository for communicating.

## Secrets not yet properly handled

The `acs_environment` ansible variable holds environment variables for the JVM
that must be handled as secrets:

```yml
acs_environment:
  JAVA_TOOL_OPTIONS: 
    - -Dmetadata-keystore.password=<your-keystore-password>
    - -Dmetadata-keystore.metadata.password=<your-keystore-password>
```

`metadata-keystore.password` is the same variable handled in `keystore_password`.

`metadata-keystore.metadata.password` is the password of the keystore dedicated to repository metadata.
