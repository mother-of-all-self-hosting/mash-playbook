# Telegraf

[Telegraf](https://www.influxdata.com/) is a plugin-driven server agent for collecting & reporting metric, that this playbook can install, powered by the [mother-of-all-self-hosting/ansible-role-influxdb](https://github.com/mother-of-all-self-hosting/ansible-role-influxdb) Ansible role. It heavily depends on [InfluxDB](influxdb.md)

## Prerequisits

* A installed and running [infuxdb](influxdb.md).

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

This role depends on a influxdb configuring telegraf. You need to obtain the influx token and config link in the influxdb.
In your browser, visit the influxdb and go to Load Data -> Telegraf.
There you need to add a telegraf configuraion. You can now obtain these values from the setup instructions and oaste them here.

```yaml
telegraf_enabled: true
telegraf_influx_token: SUPERSECRETTOKEN
telegraf_config_link: https://influxdb.example.org/api/v2/telegrafs/0123456789
```

## Usage

In your influxdb configure the telegraf plugins as you like.

