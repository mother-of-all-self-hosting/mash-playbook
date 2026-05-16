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

## Dependencies

- [Traefik](traefik.md) reverse-proxy server (optional)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# stirling-pdf                                                         #
#                                                                      #
########################################################################

stirling_pdf_enabled: true

stirling_pdf_hostname: mash.example.com
stirling_pdf_path_prefix: /stirling-pdf

########################################################################
#                                                                      #
# /stirling-pdf                                                        #
#                                                                      #
########################################################################
```

### Optional Configuration

You can decide if you want to configure via environment variables. Environment variables outrank the configuration file. Using the configuration file via `stirling_pdf_extra_config` is not encurage, since stirling-pdf override it at application start ([see](https://github.com/Bergruebe/ansible-role-stirling-pdf/issues/7)).

To set addition environment variables use `stirling_pdf_environment_variables_extensions` in your `vars.yml` file.

```yaml
stirling_pdf_environment_variables_extensions: |
  SYSTEM_DEFAULTLOCALE=de-DE
  SYSTEM_DEFAULTLOCALE=de-DE
  SECURITY_ENABLELOGIN=false
```

Find all possible arguments in the [official documentation](https://docs.stirlingpdf.com/Advanced%20Configuration/How%20to%20add%20configurations).

### Extending the configuration

There are some additional things you may wish to configure about the service.

Take a look at:

- [`ansible-role-stirling-pdf` Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-stirling-pdf)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-stirling-pdf/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file.

## Related services

- [BentoPDF](bentopdf.md) — Client-side PDF editor and converter
- [OmniTools](omnitools.md) — Web app offering a variety of online tools to simplify everyday tasks
