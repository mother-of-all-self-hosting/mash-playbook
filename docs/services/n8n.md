<!--
SPDX-FileCopyrightText: 2023 kinduff
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# n8n

The playbook can install and configure [n8n](https://n8n.io/) for you.

n8n is a workflow automation tool for technical people.

See the project's [documentation](https://docs.n8n.io/) to learn what n8n does and why it might be useful to you.

>[!WARNING]
> n8n is licensed under [Sustainable Use License](https://github.com/n8n-io/n8n/blob/master/LICENSE.md). Because we had discouraged using [Redis](redis.md) as it was provided under "source available" model (note: Redis has retracted its stance in the end and since version 8.0 it was started to be released under multiple licenses, one of which is AGPL-3.0), we do not encourage using n8n either on the same ground.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# n8n                                                                  #
#                                                                      #
########################################################################

n8n_enabled: true

n8n_hostname: mash.example.com
n8n_path_prefix: /n8n

########################################################################
#                                                                      #
# /n8n                                                                 #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, the Calibre-Web instance becomes available at the URL specified with `n8n_hostname` and `n8n_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/n8n`.

You can create additional users (admin-privileged or not) after logging in.
