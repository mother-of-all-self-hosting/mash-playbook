<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2025 Sudo-Tiz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Bazarr

The playbook can install and configure [Bazarr](https://www.bazarr.media/) for you.

Bazarr is a companion application to [Sonarr](https://sonarr.tv/) and [Radarr](https://radarr.video/) that manages and downloads subtitles based on your requirements.

See the project's [documentation](https://wiki.bazarr.media/) to learn what Bazarr does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# bazarr                                                               #
#                                                                      #
########################################################################

bazarr_enabled: true

bazarr_hostname: bazarr.example.com

# To mount additional data directories, use `bazarr_container_additional_volumes_custom`
#
# Example:
# bazarr_container_additional_volumes_custom:
#   - type: bind
#     src: /path/on/the/host
#     dst: /data
#   - type: bind
#     src: /another-path/on/the/host
#     dst: /read-only
#     options: readonly

########################################################################
#                                                                      #
# /bazarr                                                              #
#                                                                      #
########################################################################
```

### Configuring HTTP Basic authentication (optional)

Since there does not exist an authentication system on the web interface, the HTTP Basic authentication on Traefik can be enabled for it. Refer to [ansible-role-bazarr](https://github.com/mother-of-all-self-hosting/ansible-role-bazarr)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-bazarr/blob/main/defaults/main.yml) file for details about how to set it up.

## Usage

After running the command for installation, the Bazarr instance becomes available at the URL specified with `bazarr_hostname`. With the configuration above, the service is hosted at `https://bazarr.example.com`.

>[!NOTE]
> The `bazarr_path_prefix` variable can be adjusted to host under a subpath (e.g. `bazarr_path_prefix: /bazarr`), but this hasn't been tested yet.

To get started, open the URL with a web browser to configure Bazarr.

Refer to `defaults/main.yml` file for additional configuration options.

## Integration with Sonarr/Radarr

To integrate Bazarr with [Sonarr](sonarr.md) and/or [Radarr](radarr.md), you need to ensure that:

1. All services can access the same media directories via `bazarr_container_additional_volumes_custom`, `sonarr_container_additional_volumes`, and/or `radarr_container_additional_volumes`
2. The services are connected to each other's networks:

    ```yaml
    # Connect Bazarr to Radarr and/or Sonarr's network
    bazarr_container_additional_networks_custom:
      - "{{ radarr_container_network }}"
      - "{{ sonarr_container_network }}"
    ```

After setup, configure the integrations in Bazarr's web interface under Settings → Sonarr/Radarr.

## Related services

- [Radarr](radarr.md)
- [Sonarr](sonarr.md)
