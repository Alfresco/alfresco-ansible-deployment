# SECURITY

This pages focuses on providing information on making the platform deployed with alfresco-ansible-deployment secure.

## Specify trustworthy applications

Nowadays several security features rely on the fact the server tells the browser which are the applications that can be trusted.
This is largely due to the expanding usage of single pages applications and setups where such an application is hosted on a domain name which do not match the backend server.

In such circumstances, you can tell the playbook which are these applications by using adding the client application to your inventory file as shown below:

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

Note the `known_urls` variable. It needs to be defined as a list of URLs where the client application is hosted

## Configure CSRF

CSRF is enabled by default and its default configuration is to only allow requests from the same `Origin` & `Referer` headers. Any other `Origin` or `Referer` will be denied.
If you want a third party application (often SPA) to be able query the alfresco API you need to add it to the list of `known_urls` as shown above.
In addition you can also control whether you want to enforce presence of either or both of the `Referer` or `Origin` headers. This is turned off by default as some
browser/clients simply do not provide them. You should not enforce them unless you have full control on your clients' browser fleet and know they all provide necessary
headers in all circumstances. If so you can override the default `csrf` configuration node.

```yaml
csrf:
  enabled: true
  force_headers:
    - referer
    - origin
  urls: "{{ trusted_urls }}"
```

Similarly in order to disable CSRF completely use:

```yaml
csrf:
  enabled: false
```

## Configure CORS

TODO as part of OPSEXP-1309

## Transformations security

Renditions using the LibreOffice transformer to render HTML are subject to the BSSRF attacks. In order to mitigate this risk, you may decide to disable the optimal renditions
and instead generate lower quality renditions (where basically images would not be rendered as part of the HTML.
That is achieved by the variable bellow:

```yaml
bssrf_protection_enabled: true
```

> This protection is disabled by default so users benefit from the best quality renditions.
