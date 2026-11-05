<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2026 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Recyclarr

The playbook can install and configure [Recyclarr](https://recyclarr.dev/) for you.

Recyclarr syncs the recommended settings of the [TRaSH Guides](https://trash-guides.info/) — custom formats, quality profiles, quality sizes and media naming — to [Sonarr](../sonarr/README.md) and [Radarr](../radarr/README.md), on a schedule.

See the project's [documentation](https://recyclarr.dev/) to learn what Recyclarr does and why it might be useful to you.

For details about configuring the [Ansible role for Recyclarr](https://github.com/mother-of-all-self-hosting/ansible-role-recyclarr), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-recyclarr/blob/main/docs/configuring-recyclarr.md) online
- 📁 `roles/galaxy/recyclarr/docs/configuring-recyclarr.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# recyclarr                                                            #
#                                                                      #
########################################################################

recyclarr_enabled: true

# The Sonarr and Radarr instances to sync, with their URLs and API keys
recyclarr_config_sonarr:
  sonarr:
    base_url: "http://{{ sonarr_identifier }}:{{ sonarr_container_http_port }}"
    api_key: YOUR_SONARR_API_KEY_HERE
    quality_definition:
      type: series

recyclarr_config_radarr:
  radarr:
    base_url: "http://{{ radarr_identifier }}:{{ radarr_container_http_port }}"
    api_key: YOUR_RADARR_API_KEY_HERE
    quality_definition:
      type: movie

########################################################################
#                                                                      #
# /recyclarr                                                           #
#                                                                      #
########################################################################
```

Keep at least one of `recyclarr_config_sonarr` and `recyclarr_config_radarr`. The example only syncs the quality sizes of the TRaSH Guides. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-recyclarr/blob/main/docs/configuring-recyclarr.md#configuring-sonarr-and-radarr-instances) on the role's documentation for where to find the API keys and what else an instance can sync.

### Connecting to Sonarr and Radarr

If [Sonarr](../sonarr/README.md) or [Radarr](../radarr/README.md) is enabled as well, the playbook wires Recyclarr to it automatically: Recyclarr joins its container network, and starting Recyclarr starts it too.

The `base_url` values above reach them by their container names. If a path prefix is set for Sonarr or Radarr, append it to that URL. For an instance on another server, use its URL instead.

## Usage

Recyclarr works in the background. It syncs the configured instances once a day by default, and not when it starts. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-recyclarr/blob/main/docs/configuring-recyclarr.md#setting-the-schedule-optional) on the role's documentation for how to change the schedule.

To sync right away, for example after changing the configuration, run `docker exec mash-recyclarr recyclarr sync` on the server. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-recyclarr/blob/main/docs/configuring-recyclarr.md#usage) on the role's documentation for details about the usage.

## Troubleshooting

Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-recyclarr/blob/main/docs/configuring-recyclarr.md#troubleshooting) on the role's documentation for details.

## Related services

- [Radarr](../radarr/README.md) — Movie organizer/manager for Usenet and BitTorrent users
- [Sonarr](../sonarr/README.md) — PVR for newsgroup and BitTorrent users
