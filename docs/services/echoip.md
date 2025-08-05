<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# echoip

The playbook can install and configure [echoip](https://github.com/mpolden/echoip) for you.

echoip is simple service for looking up your IP address, which powers [ifconfig.co](https://ifconfig.co).

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# echoip                                                               #
#                                                                      #
########################################################################

echoip_enabled: true

echoip_hostname: echoip.example.com

########################################################################
#                                                                      #
# /echoip                                                              #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, echoip becomes available at the specified hostname like `https://echoip.example.com`.

You can use the echoip instance by running a command as below:

```sh
curl https://echoip.example.com
```
