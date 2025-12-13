<!--
SPDX-FileCopyrightText: 2025 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Apache NiFi

[Apache NiFi](https://nifi.apache.org/) is an open source, easy to use, powerful, and reliable system to process and distribute data.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Prerequisites

To deploy Apache NiFi using this role it is necessary that:

1. The [community.general](https://github.com/ansible-collections/community.general) collection be installed. This is needed to support modifying XML configuration files.
2. The [community.crypto](https://github.com/ansible-collections/community.crypto) collection be installed. This is needed to create the self-signed HTTPS certificate for Apache NiFi.
3. The `keytool` program be available on the target host. This can be installed via `apt install default-jre` on Debian systems.


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

# A passphrase used to generate a self-signed certificate
# which is used to serve Apache NiFi via HTTPS internally
# Generate one using `pwgen -s 64 1`, or some other way
nifi_self_signed_cert_passphrase: ""

# A passphrase used to encrypt sensitive values inputted into NiFi
# Generate one using `pwgen -s 64 1`, or some other way
nifi_sensitive_props_key: ""

# The default login credentials to configure
# The password must be at least 12 characters, generate one using `pwgen -s 32 1`, or some other way
# The salt must be exactly 22 characters, and does not necessarily need to be changed from default value
nifi_login_username: admin
nifi_login_password: my-secure-password

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
      {{ nifi_traefik_serverstransport }}:
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
