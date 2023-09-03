# Frigate

[Frigate](https://frigate.video/) is an open source NVR built around real-time AI object detection.

## Dependencies

No other services are required to run Frigate in the default configuration,
but it is commonly deployed together with an MQTT broker such as:
* [mosquitto](mosquitto.md)
* [rumqttd](rumqttd.md)

## Configuration

To enable this service, add the following to your `vars.yml` and re-run the [installation](../installing.md).

```yaml
########################################################################
#                                                                      #
# frigate                                                              #
#                                                                      #
########################################################################

frigate_enabled: true

# Required
# See https://docs.frigate.video/configuration/cameras
frigate_cameras:
  # Required: name of the camera
  MY_EXAMPLE_CAMERA_NAME:
    # Optional: Enable/Disable the camera (default: shown below).
    # If disabled: config is used but no live stream and no capture etc.
    # Events/Recordings are still viewable.
    enabled: True
    # Required: ffmpeg settings for the camera
    ffmpeg:
      # Required: A list of input streams for the camera. See documentation for more information.
      inputs:
        # Required: the path to the stream
        # NOTE: path may include environment variables, which must begin with 'FRIGATE_' and be referenced in {}
        - path: rtsp://MY_EXAMPLE_CAMERA_URL
          # Required: list of roles for this stream. valid values are: detect,record,rtmp
          # NOTICE: In addition to assigning the record and rtmp roles,
          # they must also be enabled in the camera config.
          roles:
            - detect
            - record
            - rtmp

########################################################################
#                                                                      #
# /frigate                                                             #
#                                                                      #
########################################################################
```

## Enabling Video Hardware Acceleration

The playbook supports configuring hardware acceleration in Frigate.

For example, to enable Intel hardware acceleration with VA-API, add the
following lines to your `vars.yml`:

```yaml
# Use VA-API to detect and use whatever hw accel is available on the system
frigate_ffmpeg_hwaccel_args: preset-vaapi

# Give the frigate container access to the Intel device
frigate_devices:
  - /dev/dri/renderD128
```

Refer to the [Frigate documentation on hardare acceleration](https://docs.frigate.video/configuration/hardware_acceleration)
for more details and support for other hardware.
