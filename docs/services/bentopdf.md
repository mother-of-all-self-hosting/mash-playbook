<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# BentoPDF

The playbook can install and configure [BentoPDF](https://github.com/alam00000/bentopdf) for you.

BentoPDF is a client-side PDF editor to manipulate PDF files (merge, cut, split …), convert files into the PDF format, etc.

See the project's [documentation](https://github.com/alam00000/bentopdf/blob/main/README.md) to learn what BentoPDF does and why it might be useful to you.

For details about configuring the [Ansible role for BentoPDF](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2bgVhWju6shYSwtdKb7v3eoSL1Pt), you can check them via:
- 🌐 [the role's documentation](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2bgVhWju6shYSwtdKb7v3eoSL1Pt/tree/docs/configuring-bentopdf.md) online
- 📁 `roles/galaxy/bentopdf/docs/configuring-bentopdf.md` locally, if you have [fetched the Ansible roles](../installing.md)

>[!NOTE]
> [This commit](https://github.com/alam00000/bentopdf/commit/2c85ca74e9476d2a2e1eb54e6f470d4a1312fd7a) on the upstream project has removed AGPL libraries due to "ensure clear legal boundaries". Note that BentoPDF itself is released under AGPL 3.0 (as of [2.0.0](https://github.com/alam00000/bentopdf/releases/tag/v2.0.0)).

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# bentopdf                                                             #
#                                                                      #
########################################################################

bentopdf_enabled: true

bentopdf_hostname: bentopdf.example.com

########################################################################
#                                                                      #
# /bentopdf                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting BentoPDF under a subpath (by configuring the `bentopdf_path_prefix` variable) does not seem to be possible due to BentoPDF's technical limitations.

### Using the default Docker image (optional)

To have the service run as the playbook's default user instead of root user, this service is by default configured to use the Docker image locally built on [this own Dockerfile](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2bgVhWju6shYSwtdKb7v3eoSL1Pt/tree/templates/Dockerfile.j2).

If you prefer simply pulling and using [the official Docker image](https://github.com/alam00000/bentopdf/pkgs/container/bentopdf) instead, add the following configuration to your `vars.yml` file:

```yaml
bentopdf_container_image_self_build: false
```

>[!NOTE]
> Adding the variable configures the playbook to run the service as a root user.

## Usage

After running the command for installation, the BentoPDF instance becomes available at the URL specified with `bentopdf_hostname`. With the configuration above, the service is hosted at `https://bentopdf.example.com`.

## Troubleshooting

See [this section](https://app.radicle.xyz/nodes/seed.radicle.garden/rad%3Az2bgVhWju6shYSwtdKb7v3eoSL1Pt/tree/docs/configuring-bentopdf.md#troubleshooting) on the role's documentation for details.

## Related services

- [Stirling PDF](stirling-pdf.md) — self-hosted PDF converter
