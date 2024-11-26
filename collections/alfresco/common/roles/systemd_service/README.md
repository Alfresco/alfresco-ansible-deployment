# systemd_service

Install and configure systemd services

## Table of content

* [systemd\_service](#systemd_service)
  * [Table of content](#table-of-content)
  * [Requirements](#requirements)
  * [Default Variables](#default-variables)
    * [systemd\_service\_additional\_options](#systemd_service_additional_options)
    * [systemd\_service\_enabled](#systemd_service_enabled)
    * [systemd\_service\_environment](#systemd_service_environment)
    * [systemd\_service\_exec\_start](#systemd_service_exec_start)
    * [systemd\_service\_exec\_stop](#systemd_service_exec_stop)
    * [systemd\_service\_state](#systemd_service_state)
    * [systemd\_service\_type](#systemd_service_type)
    * [systemd\_service\_unit\_after](#systemd_service_unit_after)
    * [systemd\_service\_unit\_description](#systemd_service_unit_description)
    * [systemd\_service\_unit\_name](#systemd_service_unit_name)
    * [systemd\_service\_user](#systemd_service_user)
    * [systemd\_service\_working\_directory](#systemd_service_working_directory)
  * [Dependencies](#dependencies)
  * [License](#license)
  * [Author](#author)

---

## Requirements

* Minimum Ansible version: `2.1`

## Default Variables

### systemd_service_additional_options

```YAML
systemd_service_additional_options: {}
```

### systemd_service_enabled

```YAML
systemd_service_enabled: true
```

### systemd_service_environment

```YAML
systemd_service_environment: {}
```

### systemd_service_exec_start

```YAML
systemd_service_exec_start: ''
```

### systemd_service_exec_stop

```YAML
systemd_service_exec_stop: kill -15 $MAINPID
```

### systemd_service_state

```YAML
systemd_service_state: started
```

### systemd_service_type

```YAML
systemd_service_type: simple
```

### systemd_service_unit_after

```YAML
systemd_service_unit_after: syslog.target network.target local-fs.target remote-fs.target
  nss-lookup.target
```

### systemd_service_unit_description

```YAML
systemd_service_unit_description: ''
```

### systemd_service_unit_name

```YAML
systemd_service_unit_name: ''
```

### systemd_service_user

```YAML
systemd_service_user: ''
```

### systemd_service_working_directory

```YAML
systemd_service_working_directory: /tmp
```

## Dependencies

None.

## License

Apache-2.0

## Author

Alfresco Ops Readiness
