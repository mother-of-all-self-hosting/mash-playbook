<!--
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# OxiTraffic

The playbook can install and configure [OxiTraffic](https://codeberg.org/mo8it/oxitraffic) for you.

OxiTraffic is a self-hosted, simple and privacy respecting website traffic tracker. It does not collect IP addresses or browser information. Each visitor is assigned an anonymous ID upon visiting the website, which is used to store information on how long the visitor stays there, without setting cookies.

See the project's [documentation](https://codeberg.org/mo8it/oxitraffic/src/branch/main/README.md) to learn what OxiTraffic does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# oxitraffic                                                           #
#                                                                      #
########################################################################

oxitraffic_enabled: true
oxitraffic_hostname: traffic.example.com

########################################################################
#                                                                      #
# /oxitraffic                                                          #
#                                                                      #
########################################################################
```

### Set the website hostname

You also need to set the hostname of the website, on which the OxiTraffic instance counts visits, as below:

```yaml
oxitraffic_tracked_origin: https://example.com
```

Replace `https://example.com` with the hostname of your website.

## Usage

After running the command for installation, OxiTraffic becomes available at the specified hostname like `https://traffic.example.com`.

To have your OxiTraffic instance count visits at `https://example.com`, you need to add the following script tag to the website:

```html
<script type="module" src="https://traffic.example.com/count.js"></script>
```

## Troubleshooting

Internal OxiTraffic errors will not be logged to `stdout` and will therefore not be part of `journalctl -fu mash-oxitraffic`. Its log can be checked by running `tail -f logs/oxitraffic`.
