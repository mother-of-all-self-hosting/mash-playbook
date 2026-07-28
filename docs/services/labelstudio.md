<!--
SPDX-FileCopyrightText: 2025 Gergely Horváth
SPDX-FileCopyrightText: 2025, 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Label Studio

The playbook can install and configure [Label Studio](https://labelstud.io/) for you.

Label Studio is an open-source data labeling tool that supports multiple projects.

See the project's [documentation](https://labelstud.io/quick-start/) to learn what Label Studio does and why it might be useful to you.

For details about configuring the [Ansible role for Label Studio](https://github.com/mother-of-all-self-hosting/ansible-role-labelstudio), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-labelstudio/blob/main/docs/configuring-labelstudio.md) online
- 📁 `roles/galaxy/labelstudio/docs/configuring-labelstudio.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# Label Studio                                                         #
#                                                                      #
########################################################################

labelstudio_enabled: true

labelstudio_hostname: labelstudio.example.com

########################################################################
#                                                                      #
# /Label Studio                                                        #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Label Studio instance becomes available at the URL specified with `labelstudio_hostname`. With the configuration above, the service is hosted at `https://labelstudio.example.com`.

To get started, open the URL with a web browser to register new accounts, log in with them, and start working.

Keep in mind that every user will see every project. It may be more secure to disable user registration and use an admin user. See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-labelstudio/blob/main/docs/configuring-labelstudio.md#setting-administrators-account-details-optional) on the role's documentation for details.

## Related services

It is possible to attach a pre-labeling backend to Label Studio. One such example project can be found in [this repository](https://github.com/seblful/label-studio-yolo-backend).
