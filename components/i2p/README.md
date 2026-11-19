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
SPDX-FileCopyrightText: 2023 Alejandro AR
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# I2P

The playbook can install and configure [the reference Java implementation](https://github.com/i2p/i2p.i2p) of [I2P](https://i2p.net/) (Invisible Internet Project) for you.

I2P is a decentralized, privacy-focused network that allows people to communicate and share information anonymously.

See the project's [documentation](https://i2p.net/en/docs/) to learn what the service does and why it might be useful to you.

For details about configuring the [Ansible role for I2P](https://radicle.network/nodes/progressiv.radicle.garden/rad%3AzHnhpZXGPKyDQUC8Ub9LfkW2S8KD), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/progressiv.radicle.garden/rad%3AzHnhpZXGPKyDQUC8Ub9LfkW2S8KD/tree/docs/configuring-i2p.md) online
- 📁 `roles/galaxy/i2p/docs/configuring-i2p.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                      #
# i2p                                                                  #
#                                                                      #
########################################################################

i2p_enabled: true

########################################################################
#                                                                      #
# /i2p                                                                 #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the I2P instance becomes available. Refer to [this section](https://radicle.network/nodes/progressiv.radicle.garden/rad%3AzHnhpZXGPKyDQUC8Ub9LfkW2S8KD/tree/docs/configuring-i2p.md#usage) on the role's documentation for details about the usage.

### Provide services via the I2P router

It is possible to have the I2P router provide services of the playbook.

First, you need to create a server "tunnel" on Hidden Services Manager on the router console. Then, bind the published port of the service to loopback as below:

```yaml
YOUR-SERVICE_container_http_host_bind_port: "127.0.0.1:YOUR_SERVER_TUNNEL_PORT_HERE"

# Disable clearnet connection via Traefik (optional)
YOUR-SERVICE_container_labels_traefik_enabled: false
```

After restarting the service, it becomes possible to access to the service with a Base 32 (“b32”) address or with `http://127.0.0.1:YOUR_SERVER_TUNNEL_PORT_HERE` if a SSH tunnel is established. The b32 address can be checked on the console.

Refer to [this section](https://i2p.net/en/docs/guides/gettingstarted/#configuring-your-browser-for-i2p) on the official documentation about how to configure your web browser for I2P.

## Troubleshooting

Refer to [this section](https://radicle.network/nodes/progressiv.radicle.garden/rad%3AzHnhpZXGPKyDQUC8Ub9LfkW2S8KD/tree/docs/configuring-i2p.md#troubleshooting) on the role's documentation for details.

## Related services

- [Onion Service with C Tor](../onion_service_tor/README.md) — Run Onion Service with C Tor
