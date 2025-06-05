# Telegraf

[Telegraf](https://www.influxdata.com/) is an open source server agent to help you collect metrics from your stacks, sensors, and systems.

This playbook can install Telegraf, powered by the [mother-of-all-self-hosting/ansible-role-telegraf](https://github.com/mother-of-all-self-hosting/ansible-role-telegraf) Ansible role. It heavily depends on [InfluxDB](influxdb.md)

## Prerequisites

* A functioning [InfluxDB](influxdb.md) instance.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

This role depends on InfluxDB. You need to obtain the influx token and config link in from InfluxDB.
In your browser, visit the InfluxDB instance and go to **Load Data** -> **Telegraf**.
There you need to add a Telegraf configuration. You can now obtain these values from the setup instructions and paste them here.

```yaml
telegraf_enabled: true
telegraf_influx_token: SUPERSECRETTOKEN
telegraf_config_link: https://influxdb.example.org/api/v2/telegrafs/0123456789
```

## Usage

In your InfluxDB instance, configure the Telegraf plugins as you like.
