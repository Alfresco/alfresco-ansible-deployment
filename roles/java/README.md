# java

This role installs the java JDK (OpenJDK)

[![community roles](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/community.yml/badge.svg)](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/community.yml)

## Requirements

`openssl` is required on the target machine (it should be provided by the
role's dependencies).

As the role has `allow_duplicates` to to`false` you MUST make sure you call the
role with appropriate arguments BEFORE any other role may call it with
different arguments.

## Dependencies

This role relies on the Alfresco `common`role.

## Example Playbook

Installing OpenJDK in a basic maner:

```yaml
    - hosts: all
      roles:
         - java
```

Installing OpenJDK and importing a server certificate in the java keystore:

```yaml
    - hosts: all
    - hosts: all
      roles:
         - role: java
           cert_containers:
              - path: snakeoil.p12
                pass: dummy
                add_to_trusted_ca: false
```

Installing OpenJDK, importing certificates and generating a security key:

```yaml
    - hosts: all
    - hosts: all
      roles:
         - role: java
           cert_containers:
              - path: server-snakeoil.p12
                pass: dummy
                add_to_trusted_ca: false
              - path: client-server-snakeoil.p12
                pass: dummy
                add_to_trusted_ca: true
           seckeys:
             - name: mykey
               algorythm: AES
               length: 256
               pass: dummy
```

> Note: a single client/server cert may also be provided.

## Author Information

[Alfresco java role](https://github.com/Alfresco/alfresco-ansible-deployment/tree/master/roles/java/)
by [Hyland - Alfresco](http://www.alfresco.com)
