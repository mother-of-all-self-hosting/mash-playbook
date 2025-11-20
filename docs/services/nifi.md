<!--
SPDX-FileCopyrightText: 2025 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Apache NiFi

[Apache NiFi](https://nifi.apache.org/) is an open source, easy to use, powerful, and reliable system to process and distribute data.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# nifi                                                                 #
#                                                                      #
########################################################################

nifi_enabled: true

nifi_hostname: nifi.example.com

nifi_environment_variables_single_user_credentials_username: "admin"

# Put a strong password below, generated with `pwgen -s 64 1` or in another way
nifi_environment_variables_single_user_credentials_password: ""

# Put a strong password in the value field, generated with `pwgen -s 64 1` or in another way
# For more information see:
#   - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html#security_properties
nifi_conf_nifi_properties:
  - key: nifi.sensitive.props.key
    value: ''

########################################################################
#                                                                      #
# /nifi                                                                #
#                                                                      #
########################################################################

########################################################################
#                                                                      #
# traefik                                                              #
#                                                                      #
########################################################################

traefik_provider_configuration_extension_yaml: |
  http:
    serversTransports:
      insecure-nifi-transport:
        insecureSkipVerify: true
      
########################################################################
#                                                                      #
# /traefik                                                             #
#                                                                      #
########################################################################
```

The custom Traefik `serversTransports` definition is required since Apache NiFi only supports listening via HTTPS. Since this "backend" certificate is self-signed, Traefik must be configured to skip verifying it.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- The [Apache NiFi role](https://github.com/spatterIight/ansible-role-nifi/)'s [`defaults/main.yml`](https://github.com/spatterIight/ansible-role-nifi/blob/main/defaults/main.yml) for additional variables that you can customize via your `vars.yml` file.
- The [Apache NiFi role documentation](https://github.com/spatterIight/ansible-role-nifi/blob/main/docs/configuring-nifi.md#adjusting-the-apache-nifi-configuration).

## Usage

After running the command for installation, Apache NiFi becomes available at the specified hostname like `https://nifi.example.com`.

To get started, open the URL with a web browser to log in to the instance using your configured credentials.

