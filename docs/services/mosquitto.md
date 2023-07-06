# Mosquitto Ansible Role


[Mosquitto](https://mosquitto.org/) is an open source [MQTT](https://en.wikipedia.org/wiki/MQTT) broker.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
mosquitto_enabled: true

# If you need to change the MQTT port you can uncomment and adjust
# mosquitto_container_mqtt_host_bind_port: "1884"
```

## Usage

After installation, you can use `just run-tags mosquitto-add-user --extra-vars=username=<username> --extra-vars=password=<password>` to create a user. For the setting to take effect, you must restart the container. To do that you can use `just start-group mosquitto`.

You can then start to send and subscribe to MQTT topics. Use port 1883 and the servers IP or any domain you configured to point at this server.

## Alternatives

* [rumqttd](rumqttd.md) is another MQTT broker
