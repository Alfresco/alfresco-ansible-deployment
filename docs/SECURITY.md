# SECURITY

This pages focuses on providing information on making the platform deployed
with alfresco-ansible-deployment secure.
In particular, for Share to work, Follow the
[Share security setup](#Share security setup).

## Specify trustworthy applications

Nowadays several security features rely on the fact the server tells the
browser which are the applications that can be trusted. This is largely due to
the expanding usage of single pages applications and setups where such an
application is hosted on a domain name which do not match the backend server.

In such circumstances, you can tell the playbook which are these applications by
 adding the client application URL as a group variable in the
`group_vars/all.yaml` file:

```yaml
known_urls:
  - http://app.domain.local/legit
  - https://app.domain.local/legit
```

## Configure CSRF

CSRF is enabled by default and its default configuration is to only allow
requests from the same `Origin` & `Referer` headers. Any other `Origin` or
`Referer` will be denied.
If you want a third party application (often SPA) to be able query the alfresco
API you need to add it to the list of `known_urls` as shown above.
In addition you can also control whether you want to enforce presence of either
or both of the `Referer` or `Origin` headers. This is turned off by default as
some browser/clients simply do not provide them. You should not enforce them
unless you have full control on your clients' browser fleet and know they all
provide necessary headers in all circumstances. If so, you can override the
default `csrf` configuration node.

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

The playbook now enables CORS headers to be sent by the server by default. The
default policy basically only allows the Same-Origin policy.
If you want to allow for more origins to query  the Alfresco repository, you
should make sure they are part of the `known_urls` variable. Any location
mentioned in this variable will be automatically to the list of relaxed origins
for CORS queries. By default they will be allowed tu use any following methods:
DELETE, GET, HEAD, OPTIONS, POST, PUT. If you want to restrict methods or
further tweak the CORS configuration, you can do so by overriding the whole
`cors` variable as shown bellow:

```yaml
cors:
  enabled: true
  urls: "{{ trusted_urls }}"
  allowed_methods:
    - GET
    - OPTIONS
    - POST
    - PUT
  allowed_headers:
    - Accept
    - Access-Control-Request-Headers
    - Access-Control-Request-Method
    - Authorization
    - Cache-Control
    - Content-Type
    - Origin
    - X-CSRF-Token
    - X-Requested-With
  exposed_headers:
    - Access-Control-Allow-Origin
    - Access-Control-Allow-Credentials
  support.credentials: true
  preflight_maxage: 10
```

To completely disable CORS simply use:

```yaml
cors:
  enabled: false
```

## Share security setup

Share is **always** deployed together with the repo (it's part of the same
role), and as a consequence will always try to access the repo through the
`localhost` interface. That means from the repo's point of view - unless Share
itself is accessed using [http://localhost/share/](http://localhost/share/) - it
is breaking CORS protection. For that reason in order for Share to work, it is
mandatory to add the URL Share will be accessed from as a `known_urls`. We
recommand doing it via the `all` group variables in `group_vars/all.yml`:

```yaml
known_urls:
  - https://ecm.domain.local/share
```

## Transformations security

Renditions using the LibreOffice transformer to render HTML are subject to the
BSSRF attacks. In order to mitigate this risk, you may decide to disable the
optimal renditions and instead generate lower quality renditions (where
basically images would not be rendered as part of the HTML).
That is achieved by the variable bellow:

```yaml
bssrf_protection_enabled: true
```

> This protection is disabled by default so users benefit from the best quality renditions.

## Hosts certificates & keys

Support for hosts' certificates has been introduced.
Its main purpose is to provide mTLS authentication for components which may
need it. By default the playbook will generate its own PKI and issue dedicated
host certificate and private key pairs. It is also possible to use your own
private PKI. To do so you can either request a CA signing certificate and key,
or you can request individual hosts certificates.

### Providing hosts certificates

In this configuration you will have to provide one certificate per hosts in the
inventory. All certificates MUST conform to the following:

- The certificates must be store in a PKCS12 container
- The corresponding private key must be added to the PKCS12 container
- All the p12 files for individual hosts must share the same passphrase
- The PKCS12 container must contain the CA certificate chain
- The certificates must have the following `extendedKeyUsage`: `serverAuth` &
  `clientAuth` so the same certificate serves for server and client
  authentication (this is a host certificate)

> That approach can be tedious and it's usually easier to either use your own
> CA signing or let the playbook generate its own PKI if that's allowed by your
> security policy.

### Using your own PKI signing CA

This is the preferred approach as it is much easier. And lets you be more
autonomous.  In this configuration, you need to provide the following to the
playbook:

- A CA signing certificate in PEM format
- The encrypted CA signing key in PEM format

Usually, you would request these 2 files to your PKI admin or generate your own
with PKI management software. In that case make sure you would be signing your
certificates with an intermediate CA. That requires you make sure the CA
certificate contains the full chain to the root CA otherwise the playbook will
not be able to update the list of trusted CA where needed and some usage of
these certificates might be broken.
Once you have these two files you need to put the certificate in the `/ca/` with
a `.pem`or `.crt` extension. The private key can be placed in the same directory
with a `.key` extension, but it's recommended to put in the `/private/` folder
as a file named `ca.key`.

> The path above are relative to the PKI directory on the control node which by
> default is `configuration_files/pki/`

With the 2 files in place you now need to provide 2 secrets:

- ca_signing_key_passphrase: the passphrase to decrypt the CA signing key
- certs_p12_passphrase: the passphrase the playbook will use to protect the
  resulting PKCS12 containers.

In order to set secrets in the playbook's vault please refer to
[SECRETS.md](SECRETS.md).

If you want to fully automate this generation just make sure to run the
`secrets-init.yml` playbook as described in the
[Deployment guide](./deployment-guide.md#encrypted-variables).

### CA generation parameters

If you let the playbook generate a small PKI infrastructure for you you can
still have some control on it using the variables below:

- pki_dir: the location to where to find/generate the CA and store generated
  certificates.
- ca_key_size: size of the private key in bits (default to 4kb long keys).
- ca_key_type: type of private key to generate (default to RSA keys).
- ca_cn: Common Name to use to generate the CA signing certificate (defaults
  to Hyland - Alfresco signing CA)
- ca_signing_key_passphrase: passphrase to use to encrypt to CA signing key
- ca_days_valid_for: how many days will the generated certificate will be
  valid for (default 10y)

### Certificates generation parameters

Similar options can be used to control how certificates are generated.

- cert_key_size: size of the private key in bits (default to 4kb long keys).
- cert_key_type: type of private key to generate (default to RSA keys).
- cert_days_valid_for: how many days will the generated certificate will be
  valid for (default 10y)

### Using the PKI playbook independently

One can call the playbook directly without playing the full ACS playbook.
Below is an example of how to do that:

```bash
pipenv run \
  ansible-playbook playbooks/pki.yml
    -e p12_passphrase=$P12_PASSPHRASE
    -e secret_ca_passphrase=$MYPKI_PASSPHRASE
    -i my_inventory_file.yml
```

> Above command expects you have first exported the PKCS12 container and the CA
> signing key passphrases as environment variables.
