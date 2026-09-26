<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Nginx

The playbook can install and configure [Nginx](https://nginx.org/) for you.

Nginx is a web server, which can also be used as a reverse proxy, load balancer and HTTP cache. By default, the playbook configures it to serve static files (e.g. a website).

See the project's [documentation](https://nginx.org/en/docs/) to learn what Nginx does and why it might be useful to you.

For details about configuring the [Ansible role for Nginx](https://github.com/spatterIight/ansible-role-nginx), you can check them via:

- 🌐 [the role's documentation](https://github.com/spatterIight/ansible-role-nginx/blob/main/docs/configuring-nginx.md) online
- 📁 `roles/galaxy/nginx/docs/configuring-nginx.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# nginx                                                                #
#                                                                      #
########################################################################

nginx_enabled: true

nginx_hostname: nginx.example.com

########################################################################
#                                                                      #
# /nginx                                                               #
#                                                                      #
########################################################################
```

### Serving static files

By default, Nginx serves the files found in the `data` directory under the service's base path (`/mash/nginx/data` on the server by default). Put your website's files (e.g. `index.html`) there.

To have Nginx do something else (e.g. reverse-proxy to another container), see [this section](https://github.com/spatterIight/ansible-role-nginx/blob/main/docs/configuring-nginx.md#changing-what-nginx-serves-optional) on the role's documentation for details.

## Usage

After running the command for installation, Nginx becomes available at the URL specified with `nginx_hostname`. With the configuration above, the service is hosted at `https://nginx.example.com`.

## Troubleshooting

See [this section](https://github.com/spatterIight/ansible-role-nginx/blob/main/docs/configuring-nginx.md#troubleshooting) on the role's documentation for details.
