# SECURITY

This pages focuses on providing information on making the platform deployed with alfresco-ansible-deployment secure.

## Specify trustworthy applications

Nowadays several security features rely on the fact the server tells the browser which are the applications that can be trusted.
This is largely due to the expanding usage of single pages applications and setups where such an application is hosted on a domain name which do not match the backend server.

In such circumstances, you can tell the playbook which are these application by using adding the client application to your inventory file as shown below:

```yaml
all:
  chidren:
    3rd_party_repo_client:
      hosts:
        my_custom_app:
          known_urls:
            - http://app.domain.local/legit
            - https://app.domain.local/legit
```

Note the `known_urls` variable. It needs to be defined as a list of URLs where the client applicaiton is hosted

## Configure CSRF

TODO as part of OPSEXP-1308

## Configure CORS

TODO as part of OPSEXP-1309
