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

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Euro-Office

The playbook can install and configure [Euro-Office](https://github.com/Euro-Office/DocumentServer) for you.

Euro-Office is an online office suite comprising viewers and editors for texts, spreadsheets and presentations, compatible with Office Open XML formats: .docx, .xlsx, .pptx and enabling collaborative editing in real time.

See the project's [documentation](https://github.com/Euro-Office/DocumentServer/blob/main/README.md) to learn what Euro-Office does and why it might be useful to you.

For details about configuring the [Ansible role for Euro-Office](https://radicle.network/nodes/seed.radicle.garden/rad%3Az4SSf2SU2YwBaMmCFBJnM5KqorU9T), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/seed.radicle.garden/rad%3Az4SSf2SU2YwBaMmCFBJnM5KqorU9T/tree/docs/configuring-eurooffice-docs.md) online
- 📁 `roles/galaxy/eurooffice/docs/configuring-eurooffice-docs.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

>[!NOTE]
> To use an Euro-Office instance to edit office documents, it is necessary to integrate it with another software which functions as a data storage and manages access control for users. **You cannot edit the documents without such integrations.**

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# eurooffice                                                           #
#                                                                      #
########################################################################

eurooffice_enabled: true

eurooffice_hostname: eurooffice.example.com

########################################################################
#                                                                      #
# /eurooffice                                                          #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Euro-Office instance becomes available at the URL specified with `eurooffice_hostname`. With the configuration above, the service is hosted at `https://eurooffice.example.com`.

### Integrating Euro-Office with FileBrowser Quantum (optional)

You can integrate Euro-Office with [FileBrowser Quantum](https://filebrowserquantum.com/) to edit office documents on the service. See [this page](filebrowser-quantum.md) for details about how to install FileBrowser Quantum.

To enable the integration, add the following configuration to your `vars.yml` file:

```yaml
filebrowser_quantum_config_integrations_office_url: "{{ eurooffice_scheme }}://{{ eurooffice_hostname }}"
filebrowser_quantum_config_integrations_office_secret: "{{ eurooffice_environment_variables_jwt_secret }}"
```

## Troubleshooting

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Az4SSf2SU2YwBaMmCFBJnM5KqorU9T/tree/docs/configuring-eurooffice-docs.md#troubleshooting) on the role's documentation for details.

## Related services

- [Collabora Online Development Edition (CODE)](code.md) — Development version of Collabora Online, which enables you to edit office documents with integrations
- [ONLYOFFICE Docs](onlyoffice-docs.md) — Online office suite comprising viewers and editors
