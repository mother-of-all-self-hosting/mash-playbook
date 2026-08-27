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

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Stirling PDF v1

>[!NOTE]
> On this playbook, Stirling PDF is implemented with [ansible-role-stirling-pdf](https://github.com/mother-of-all-self-hosting/ansible-role-stirling-pdf). While Stirling PDF itself continues to be actively developed, the role is configured to install version 1 and will not support version 2, because it enforces Open Core license since [v2.0.0](https://github.com/Stirling-Tools/Stirling-PDF/releases/tag/v2.0.0).

The playbook can install and configure [Stirling PDF](https://github.com/Stirling-Tools/Stirling-PDF) version 1 for you.

Stirling PDF is an online PDF converter and editor.

See the project's [documentation](https://github.com/Stirling-Tools/Stirling-PDF/blob/main/README.md) to learn what Stirling PDF does and why it might be useful to you.

For details about configuring the [Ansible role for Stirling PDF](https://github.com/mother-of-all-self-hosting/ansible-role-stirling-pdf), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-stirling-pdf/blob/main/docs/configuring-stirling-pdf.md) online
- 📁 `roles/galaxy/stirling_pdf/docs/configuring-stirling-pdf.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

- [Traefik](traefik.md) reverse-proxy server (optional)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# stirling_pdf                                                         #
#                                                                      #
########################################################################

stirling_pdf_enabled: true

stirling_pdf_hostname: mash.example.com
stirling_pdf_path_prefix: /stirling-pdf

########################################################################
#                                                                      #
# /stirling_pdf                                                        #
#                                                                      #
########################################################################
```

### Configuring HTTP Basic authentication

The HTTP Basic authentication on Traefik is enabled for the web interface by default. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-stirling-pdf/blob/main/docs/configuring-stirling-pdf.md#configuring-http-basic-authentication) on the role's documentation for details about how to set it up or disable it.

## Usage

After running the command for installation, the Lute instance becomes available at the URL specified with `stirling_pdf_hostname`. With the configuration above, the service is hosted at `https://mash.example.com/stirling-pdf`.

## Related services

- [BentoPDF](bentopdf.md) — Client-side PDF editor and converter
- [OmniTools](omnitools.md) — Web app offering a variety of online tools to simplify everyday tasks
