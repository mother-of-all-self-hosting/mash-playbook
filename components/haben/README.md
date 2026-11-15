<!--
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 Bergruebe

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Haben

The playbook can install and configure [Haben](https://haben.app) for you.

Haben is a self-hosted bookkeeping application for German freelancers and small businesses, with e-invoicing and VAT returns via ELSTER.

See the project's [documentation](https://haben.app/) (in German) to learn what Haben does and why it might be useful to you.

For details about configuring the [Ansible role for Haben](https://github.com/bergruebe/ansible-role-haben), you can check them via:

- 🌐 [the role's documentation](https://github.com/bergruebe/ansible-role-haben/blob/main/docs/configuring-haben.md) online
- 📁 `roles/galaxy/haben/docs/configuring-haben.md` locally, if you have [fetched the Ansible roles](../../docs/installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](../postgres/README.md) database
- [Traefik](../traefik/README.md) reverse-proxy server
- (optional) [TSDProxy](../tsdproxy/README.md) — for reaching Haben over Tailscale

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../../docs/installing.md) process:

```yaml
########################################################################
#                                                                                                                                            #
# haben                                                                                                                                 #
#                                                                                                                                            #
########################################################################

haben_enabled: true

haben_hostname: haben.example.com

# Generate it with: openssl rand -base64 32
haben_environment_variables_haben_encryption_key: YOUR_ENCRYPTION_KEY_HERE

########################################################################
#                                                                                                                                            #
# /haben                                                                                                                                #
#                                                                                                                                            #
########################################################################
```

>[!WARNING]
> The encryption key protects the ELSTER certificate and stored API keys. Keep a copy in a safe place and do not change it later.

See the role's documentation for details about configuring Haben per your preference (such as [Single Sign-On](https://github.com/bergruebe/ansible-role-haben/blob/main/docs/configuring-haben.md#configure-single-sign-on-optional) and [ELSTER](https://github.com/bergruebe/ansible-role-haben/blob/main/docs/configuring-haben.md#configure-elster-optional)).

### Exposing Haben via TSDProxy (optional)

If [TSDProxy](../tsdproxy/README.md) is enabled, it can serve Haben in your Tailscale network instead of Traefik. Refer to [this section](https://github.com/bergruebe/ansible-role-haben/blob/main/docs/configuring-haben.md#expose-haben-via-tsdproxy-optional) on the role's documentation for details.

## Usage

After running the command for installation, Haben becomes available at the URL specified with `haben_hostname`. With the configuration above, the service is hosted at `https://haben.example.com`.

To create the first account, enter the setup code which Haben prints to its logs: `journalctl -u mash-haben | grep -i einrichtungscode`

## Backup

The database is managed by the playbook's [Postgres](../postgres/README.md) and can be backed up with [Postgres Backup](../postgres_backup/README.md) or [BorgBackup](../backup_borg/README.md). The receipts are stored in `/mash/haben/data/belege`, which BorgBackup includes by default.

## Troubleshooting

Refer to [this section](https://github.com/bergruebe/ansible-role-haben/blob/main/docs/configuring-haben.md#troubleshooting) on the role's documentation for details.
