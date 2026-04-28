<!--
SPDX-FileCopyrightText: 2025 MASH project contributors
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Stirling PDF

The playbook can install and configure [Stirling PDF](https://github.com/Stirling-Tools/Stirling-PDF) for you.

Stirling PDF is an online PDF converter and editor.

See the project's [documentation](https://github.com/Stirling-Tools/Stirling-PDF/blob/main/README.md) to learn what Stirling PDF does and why it might be useful to you.

>[!WARNING]
> Since [v2.0.0](https://github.com/Stirling-Tools/Stirling-PDF/releases/tag/v2.0.0) Stirling PDF enforces Open Core license.

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

stirling_pdf_hostname: stirling-pdf.example.com

# The path at which stirling_pdf is served.
# This value must either be `/` or not end with a slash (e.g. `/pdf`).
stirling_pdf_path_prefix: /

# Set to true to download calibre onto stirling-pdf enabling pdf to/from book and advanced html conversion | default false
stirling_pdf_install_calibre: false

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

All possible variables to configure the ansible-role can be found in its [defaults/main.yml](https://github.com/Bergruebe/ansible-role-stirling-pdf/blob/main/defaults/main.yml) file.

## Related services

- [BentoPDF](bentopdf.md) — client-side PDF editor and converter
