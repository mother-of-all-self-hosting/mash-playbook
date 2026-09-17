<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Radarr

The playbook can install and configure [Radarr](https://radarr.video/) for you.

Radarr is a movie organizer/manager for Usenet and BitTorrent users.

See the project's [documentation](https://wiki.servarr.com/radarr) to learn what Radarr does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# radarr                                                               #
#                                                                      #
########################################################################

radarr_enabled: true

radarr_hostname: radarr.example.com

# To mount additional data directories, use `radarr_container_additional_volumes`
#
# Example:
# radarr_container_additional_volumes:
#   - type: bind
#     src: /path/on/the/host
#     dst: /data
#   - type: bind
#     src: /another-path/on/the/host
#     dst: /read-only
#     options: readonly

########################################################################
#                                                                      #
# /radarr                                                              #
#                                                                      #
########################################################################
```

### Trusting reverse-proxy headers

Radarr only trusts forwarded headers from loopback addresses by default. For Traefik to pass the original client address and HTTPS scheme to Radarr, configure **Trusted Networks** with the proxy's address or network. Otherwise Radarr sees the proxy's address and the internal HTTP connection, which can affect authentication and generated URLs. See [Radarr's security settings](https://wiki.servarr.com/radarr/settings#security).

On the server, inspect the Docker network shared by Traefik and Radarr. Its name is the value of `mash_playbook_reverse_proxyable_services_additional_network`:

```sh
docker network inspect NETWORK_NAME --format '{{range .IPAM.Config}}{{println .Subnet}}{{end}}'
```

Replace `NETWORK_NAME` with that network's actual name. Trust only the proxy's address or the specific subnet it connects from; trusting a subnet also trusts other containers attached to it. Do not restore trust for all private networks. For an external proxy, use its source address or subnet as seen by Radarr.

You can configure **Settings → General → Security → Trusted Networks** in Radarr and restart it, or manage the setting through `vars.yml`:

```yaml
# Example only: replace this subnet with the actual proxy subnet.
radarr_environment_variables_additional_variables: |
  RADARR__SERVER__TRUSTEDNETWORKS=172.20.0.0/24
```

If you already define `radarr_environment_variables_additional_variables`, add the line to the existing block and preserve its other entries. Multiple addresses or subnets are comma-separated. This environment setting takes precedence over the value saved in Radarr's configuration. Re-run `just install-service radarr` to apply it, and revisit the setting if the proxy network changes.

Keep authentication required for all addresses, especially when using a reverse proxy. If you configure **Allowed Hosts**, include `radarr_hostname` and any additional names used by API clients; an empty list currently accepts all hostnames. After upgrading, verify login and API access through the public HTTPS URL, and check Radarr's logs for the configured trusted network and any rejected hosts.

## Usage

After running the command for installation, the Autobrr instance becomes available at the URL specified with `radarr_hostname`. With the configuration above, the service is hosted at `https://radarr.example.com`.

>[!NOTE]
> The `radarr_path_prefix` variable can be adjusted to host under a subpath (e.g. `radarr_path_prefix: /radarr`), but this hasn't been tested yet.

To get started, open the URL with a web browser to create an account. The recommended authentication method is `Forms (Login Page)`.

For additional configuration options, refer to [ansible-role-radarr](https://github.com/spatterIight/ansible-role-radarr)'s `defaults/main.yml` file.

## Related services

- "* Arr" applications — [Autobrr](autobrr.md) / [Homarr](homarr.md) / [Sonarr](sonarr.md)
- [Jackett](jackett.md)
  - For Jackett integration instructions, see the [setup guide](jackett.md#intergration-with-sonarrradarr)
- [Jellyfin](jellyfin.md)
- [Seerr](seerr.md)
- [Plex](plex.md)
- [qBittorrent](qbittorrent.md)
  - For qBittorrent integration instructions, see the [setup guide](qbittorrent.md#intergration-with-sonarrradarr)
