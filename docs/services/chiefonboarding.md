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
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# ChiefOnboarding

The playbook can install and configure [ChiefOnboarding](https://docs.chiefonboarding.com) for you.

ChiefOnboarding is a remote-first employee onboarding platform to streamline the employee experience for both employees and employers.

See the project's [documentation](https://docs.chiefonboarding.com) to learn what ChiefOnboarding does and why it might be useful to you.

For details about configuring the [Ansible role for ChiefOnboarding](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3HYheWh86U9ErEL18tK2gBkq7g2A), you can check them via:

- 🌐 [the role's documentation](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3HYheWh86U9ErEL18tK2gBkq7g2A/tree/docs/configuring-chiefonboarding.md) online
- 📁 `roles/galaxy/chiefonboarding/docs/configuring-chiefonboarding.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) database
- [Traefik](traefik.md) reverse-proxy server
- (optional) [exim-relay](exim-relay.md) mailer — ChiefOnboarding is compatible with other email delivery services

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# chiefonboarding                                                      #
#                                                                      #
########################################################################

chiefonboarding_enabled: true

chiefonboarding_hostname: chiefonboarding.example.com

########################################################################
#                                                                      #
# /chiefonboarding                                                     #
#                                                                      #
########################################################################
```

**Note**: hosting ChiefOnboarding under a subpath (by configuring the `chiefonboarding_path_prefix` variable) does not seem to be possible due to ChiefOnboarding's technical limitations.

### Set a random string

You also need to set a random string to the variable as below by adding the following configuration to your `vars.yml` file. The value can be generated with `pwgen -s 64 1` or in another way.

```yaml
chiefonboarding_environment_variables_secret_key: YOUR_SECRET_KEY_HERE
```

### Configuring the mailer (optional)

On ChiefOnboarding you can set up a mailer for functions such as password recovery. If you enable the [exim-relay](exim-relay.md) service in your inventory configuration, the playbook will automatically configure it as a mailer for the service.

>[!WARNING]
> Without setting an authentication method such as DKIM, SPF, and DMARC for your hostname, emails are most likely to be quarantined as spam at recipient's mail servers. The worst scenario is that your server's IP address or hostname will be included in the spam list such as the one managed by [Spamhaus](https://www.spamhaus.org/), depending on the reputation. As the exim-relay service supports DKIM signing, refer to [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) for details about how to set it up.

Refer to [this section](https://radicle.network/nodes/seed.radicle.garden/rad:z3HYheWh86U9ErEL18tK2gBkq7g2A/tree/docs/configuring-chiefonboarding.md#configure-the-mailer) on the role's documentation for the details about how to configure the mailer.

## Usage

After installation, the ChiefOnboarding instance becomes available at the URL specified with `chiefonboarding_hostname`. With the configuration above, the service is hosted at `https://chiefonboarding.example.com`.

To get started, open the URL with a web browser to create an account.

## Troubleshooting

See [this section](https://radicle.network/nodes/seed.radicle.garden/rad%3Az3HYheWh86U9ErEL18tK2gBkq7g2A/tree/docs/configuring-chiefonboarding.md#troubleshooting) on the role's documentation for details.
