Role Name
=========

This role installs the java JDK (OpenJDK)

[![community roles](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/community.yml/badge.svg)](https://github.com/Alfresco/alfresco-ansible-deployment/actions/workflows/community.yml)

Requirements
------------

`openssl` is required on the target machine (it should be provided by the role's dependencies).

Dependencies
------------

This role relies on the Alfresco `common`role.

Example Playbook
----------------

Installing OpenJDK in a basic maner:

    - hosts: all
      roles:
         - java

Installing OpenJDK and importing a server certificate in the java keystore:

    - hosts: all
      roles:
         - role: java
           cert_containers:
              - path: snakeoil.p12
                pass: dummy
                trustcachain: false

Installing OpenJDK, importing certificates and generating a security key:

    - hosts: all
      roles:
         - role: java
           cert_containers:
              - path: server-snakeoil.p12
                pass: dummy
                trustcachain: false
              - path: client-server-snakeoil.p12
                pass: dummy
                trustcachain: true
           seckeys:
             - name: mykey
               algorythm: AES
               length: 256
               pass: dummy

> Note: a single client/server cert may also be provided.

Author Information
------------------

[Alfresco java role](https://github.com/Alfresco/alfresco-ansible-deployment/tree/master/roles/java/)
by [Hyland - Alfresco](http://www.alfresco.com)
