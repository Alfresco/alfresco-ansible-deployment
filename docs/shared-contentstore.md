# Setting up an Enterprise grade contentstore

In enterprise environment, it's a common requirement to setup a platform so that data is stored on trusted device.

## Use cases

The contentstore is the location where you want Alfresco Content Service to write the data you store in its repository. Implementation may vary but by default files are stored there in a structured folder hierarchy as shown bellow:

```shell
contentstore.deleted
contentstore
└── 2022
    └── 2
        ├── 17
        │   └── 18
        │       ├── 54
        │       └── 55
        └── 18
            └── 2
                ├── 22
                ├── 23
                ├── 24
                └── 25
```

The most common use cases which involve setting up a dedicated, enterprise grade contentstore are listed bellow (non exhaustive list):

- You bought expensive storage hardware and want to leverage all the goodness that comes with it. For example, your NetApp NAS offers snapshots capabilities which will help you a lot improving your backup procedure.
- Your data is really critical and you want to leverage the storage architecture which offers cross-site replication.
- Your network topology involves a clear seperation between data and applications.
- Your workload cannot be handled by a single server and you need to setup a cluster.

## The approach to storage integration

While ACS only need to be given a filesystem, the underlying implementation and deployment methodology can vary a lot depending on technology, vendors and models. For this reason it is not possible for the playbook to handle the low-level part of the configuration.
As a consequence the playbook will not try setup your storage system for you ([Ansible provide great modules](https://docs.ansible.com/ansible/2.9/modules/list_of_storage_modules.html) for some vendors), but expect that it's been done in advance. What the playbook will do instead is configure the OS so that the storage is mounted on the OS at boot time and ACS has appropriate permissions to write to it (see notes about permissions below).
In order for the playbook to you need to give it the details about the storage location in a way it can understand.

### Configuration format

Instead of re-inventing the wheel and trying to come up with a sensible configuration syntax or format, we've chosen to rely on the widely used mount format (see [mount(8)](https://linux.die.net/man/8/mount) for details). There are 3 things one needs to provide to the playbook:

- A device: same as what would be the first argument of the mount command if you were to manually mount the filesystem.
- A type: the filesystem type as recognized by the mount programm (e.g. cifs for windows share or nfs for NFS exports).
- A set of options: an optional list of comma separated options. Such options can be generic to the mount programm, or dedicated to the type of filesystem.

### Providing configuration details

The Ansible playbook expect to find the configuration details in a strucutured variable named `cs_storage`. It's structure is as bellow:

```yaml
cs_storage:
  device:
  type:
  options:
```

Given this variable defines a chunk of the deployment architecture we recommend you set it in the ansible inventory file. The file `inventory_ha.yml` gives an example of how to use that feature.

#### Typical clusters

For most clusters setting the `cs_storage` variable under the `repository` group is sensible as it makes that config available to all cluster nodes without repeating the config in different places. This is what is done in the example file `inventory_ha.yml` and match most case such as those shown below:

![ACS basic cluster storage](resources/acs-ha-contentstore.png)

#### Advanced use cases

There may be cases where the configuration required to mount the filesystem on each host might differ. In this case the configuration can be repeated for each repository node, as shown below:

```yaml
---
all:
  children:
    repository:
      hosts:
        ecm1:
          cs_storage:
              device: storage.site1.infra.local:/nfs/contentstore
              type: nfs
              options: _netdev,noatime,nodiratime,tcp,soft,intr
        ecm2:
          cs_storage:
              device: backup.site2.infra.local:/replica/content_store
              options: _netdev,noatime,nodiratime,tcp,soft,intr
```

> The example above could be used in case of sites replicated real-time through low latency links between sites. That's a feature high storage vendors can offer.
