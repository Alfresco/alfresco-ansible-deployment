# manual-activemq

This is a scenario to test the playbook with a manually provisioned activemq service.

Activemq connections details must be manually provided in the [hosts.yml](hosts.yml) file.

For example ActiveMQ can run on [Amazon MQ](https://eu-west-1.console.aws.amazon.com/amazon-mq/home?region=eu-west-1#/brokers).
Make sure to configure Security Group to enable access to the openwire port.

Then launch the scenario with:

```bash
molecule -e molecule/manual-activemq/vars.yml converge -s manual-activemq
```
