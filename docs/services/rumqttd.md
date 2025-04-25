<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# rumqttd

[rumqttd](https://github.com/bytebeamio/rumqtt) is a high performance, embeddable [MQTT](https://en.wikipedia.org/wiki/MQTT) broker installed via [mother-of-all-self-hosting/ansible-role-rumqttd](https://github.com/mother-of-all-self-hosting/ansible-role-rumqttd).


# Configuring this role for your playbook

## Dependencies

This service does not require any dependecies.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# rumqttd                                                              #
#                                                                      #
########################################################################


rumqttd_enabled: true


########################################################################
#                                                                      #
# /rumqttd                                                             #
#                                                                      #
########################################################################
```


## Usage

You can then start to send and subscribe to MQTT topics. Use port 1883 and the servers IP or any domain you configured to point at this server.

## Alternatives

* [Mosquitto](mosquitto.md) is another, more feature-complete MQTT broker
