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
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Authelia

The playbook can install and configure [Authelia](https://www.authelia.com/) for you.

Authelia is an open-source [authentication](https://www.authelia.com/overview/authentication/introduction/) and [authorization](https://www.authelia.com/overview/authorization/access-control/) server and portal fulfilling the identity and access management (IAM) role of information security in providing [multi-factor authentication](https://www.authelia.com/overview/authentication/introduction/) and single sign-on (SSO) for your applications via a web portal.

See the project's [documentation](https://www.authelia.com/integration/prologue/get-started/) to learn what Authelia does and why it might be useful to you.

For details about configuring the [Ansible role for Authelia](https://github.com/mother-of-all-self-hosting/ansible-role-authelia), you can check them via:

- 🌐 [the role's documentation](https://github.com/mother-of-all-self-hosting/ansible-role-authelia/blob/main/docs/configuring-authelia.md) online
- 📁 `roles/galaxy/authelia/docs/configuring-authelia.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Postgres](postgres.md) / MySQL / [MariaDB](mariadb.md) / [SQLite](https://www.sqlite.org/) database
- [Traefik](traefik.md) reverse-proxy server
- (optional; recommended) [Valkey](valkey.md) — if not enabled, restarting Authelia destroys user sessions

## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
########################################################################
#                                                                      #
# authelia                                                             #
#                                                                      #
########################################################################

authelia_enabled: true

authelia_hostname: authelia.example.com

########################################################################
#                                                                      #
# /authelia                                                            #
#                                                                      #
########################################################################
```

**Note**: hosting Authelia under a subpath (by configuring the `authelia_path_prefix` variable) does not seem to be possible due to Authelia's technical limitations.

### Set a random string

You also need to set a random string to the variable as below by adding the following configuration to your `vars.yml` file. The value can be generated with `pwgen -s 64 1` or in another way.

```yaml
authelia_config_storage_encryption_key: YOUR_SECRET_KEY_HERE
```

>[!WARNING]
> Changing `authelia_config_storage_encryption_key` subsequently will cause trouble unless you use the CLI to migrate.

### Set the base domain for session cookies

You also need to specify the base domain that session cookies related to authentication will be set on. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-authelia/blob/main/docs/configuring-authelia.md#set-the-base-domain-for-session-cookies) on the role's documentation for details.

### Select database to use

Authelia can use a MySQL compatible database, Postgres, or SQLite, and you need to choose one. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-authelia/blob/main/docs/configuring-authelia.md#configuring-database) on the role's documentation for details.

>[!NOTE]
> If you have neither enabled MariaDB or disabled Postgres explicitly with this playbook, the database for your existing installation is most likely to be `postgres`.

### Configuring operation modes

Authelia can be used in two different modes, which can be enabled simultaneously. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-authelia/blob/main/docs/configuring-authelia.md#configuring-operation-modes) on the role's documentation for details.

### Configuring authentication storage providers

Authelia supports [file-based](https://www.authelia.com/configuration/first-factor/file/) and [LDAP](https://www.authelia.com/configuration/first-factor/ldap/) storage providers for the user database. Refer to [this section](https://github.com/mother-of-all-self-hosting/ansible-role-authelia/blob/main/docs/configuring-authelia.md#configuring-authentication-storage-providers) on the role's documentation for details.

### Configuring Valkey (optional)

>[!WARNING]
> If Valkey is not enabled, session information is stored in memory, and restarting the process will destroy all user sessions.

Valkey can optionally be enabled for caching data. This playbook supports it, and you can set up a Valkey instance by enabling it on `vars.yml`.

If Authelia is the sole service which requires Valkey on your server, it is fine to set up just a single Valkey instance. However, **it is not recommended if there are other services which require it, because sharing the Valkey instance has security concerns and possibly causes data conflicts**, as described on the [documentation for configuring Valkey](valkey.md). In this case, you should install a dedicated Valkey instance for each of them.

If you are unsure whether you will install other services along with Authelia or you have already set up services which need Valkey (such as [PeerTube](peertube.md), [Funkwhale](funkwhale.md), and [Docmost](docmost.md)), it is recommended to install a Valkey instance dedicated to Authelia.

*See [below](#setting-up-a-shared-valkey-instance) for an instruction to install a shared instance.*

#### Setting up a dedicated Valkey instance

To create a dedicated instance for Authelia, you can follow the steps below:

1. Adjust the `hosts` file
2. Create a new `vars.yml` file for the dedicated instance
3. Edit the existing `vars.yml` file for the main host

*Refer to [this page](../running-multiple-instances.md) for details about configuring multiple instances of Valkey on the same server.*

##### Adjust `hosts`

At first, you need to adjust `inventory/hosts` file to add a supplementary host for Authelia.

The content should be something like below. Make sure to replace `mash.example.com` with your hostname and `YOUR_SERVER_IP_ADDRESS_HERE` with the IP address of the host, respectively. The same IP address should be set to both, unless the Valkey instance will be served from a different machine.

```ini
[mash_servers]
[mash_servers:children]
mash_example_com

[mash_example_com]
mash.example.com ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
mash.example.com-authelia-deps ansible_host=YOUR_SERVER_IP_ADDRESS_HERE
…
```

`mash_example_com` can be any string and does not have to match with the hostname.

You can just add an entry for the supplementary host to `[mash_example_com]` if there are other entries there already.

##### Create `vars.yml` for the dedicated instance

Then, create a new directory where `vars.yml` for the supplementary host is stored. If `mash.example.com` is your main host, name the directory as `mash.example.com-authelia-deps`. Its path therefore will be `inventory/host_vars/mash.example.com-authelia-deps`.

After creating the directory, add a new `vars.yml` file inside it with a content below. It will have running the playbook create a `mash-authelia-valkey` instance on the new host, setting `/mash/authelia-valkey` to the base directory of the dedicated Valkey instance.

```yaml
# This is vars.yml for the supplementary host of Authelia.

---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-authelia-'
mash_playbook_service_base_directory_name_prefix: 'authelia-'

########################################################################
#                                                                      #
# /Playbook                                                            #
#                                                                      #
########################################################################

########################################################################
#                                                                      #
# valkey                                                               #
#                                                                      #
########################################################################

valkey_enabled: true

########################################################################
#                                                                      #
# /valkey                                                              #
#                                                                      #
########################################################################
```

##### Edit the main `vars.yml` file

Having configured `vars.yml` for the dedicated instance, add the following configuration to `vars.yml` for the main host, whose path should be `inventory/host_vars/mash.example.com/vars.yml` (replace `mash.example.com` with yours).

```yaml
########################################################################
#                                                                      #
# authelia                                                             #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Make sure the connection via Unix domain socket is enabled
# Set to `false` to enable TCP connection instead
authelia_redis_socket_enabled: true

# Connect Authelia to its dedicated Valkey instance via the Unix domain socket
#
# Alternatively, if you set `authelia_redis_socket_enabled` to `false`,
# - Add the dedicated Valkey instance (mash-authelia-valkey) to `authelia_redis_hostname`
# - Add its network (mash-authelia-valkey) to `authelia_container_additional_networks_custom`
authelia_redis_socket_path_host: /mash/authelia-valkey/run

# Make sure the Authelia service (mash-authelia.service) starts after its dedicated Valkey service (mash-authelia-valkey.service)
authelia_systemd_required_services_list_custom:
  - "mash-authelia-valkey.service"

########################################################################
#                                                                      #
# /authelia                                                            #
#                                                                      #
########################################################################
```

Running the installation command will create the dedicated Valkey instance named `mash-authelia-valkey`.

#### Setting up a shared Valkey instance

If you host only Authelia on this server, it is fine to set up a single shared Valkey instance.

To install the single instance and hook Authelia to it, add the following configuration to `inventory/host_vars/mash.example.com/vars.yml`:

```yaml
########################################################################
#                                                                      #
# valkey                                                               #
#                                                                      #
########################################################################

valkey_enabled: true

########################################################################
#                                                                      #
# /valkey                                                              #
#                                                                      #
########################################################################

########################################################################
#                                                                      #
# authelia                                                             #
#                                                                      #
########################################################################

# Add the base configuration as specified above

# Make sure the connection via Unix domain socket is enabled
# Set to `false` to enable TCP connection instead
authelia_redis_socket_enabled: true

# Connect Authelia to the shared Valkey instance via the Unix domain socket
#
# Alternatively, if you set `authelia_redis_socket_enabled` to `false`,
# - Add the shared Valkey instance (mash-valkey) to `authelia_redis_hostname`
# - Add its network (mash-valkey) to `authelia_container_additional_networks_custom`
authelia_redis_socket_path_host: "{{ valkey_run_path }}"

# Make sure the Authelia service (mash-authelia.service) starts after the shared Valkey service (mash-valkey.service)
authelia_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

########################################################################
#                                                                      #
# /authelia                                                            #
#                                                                      #
########################################################################
```

Running the installation command will create the shared Valkey instance named `mash-valkey`.

### Integrating with Prometheus (optional)

Authelia can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If Authelia and Prometheus do not share a network (like Traefik), you can connect the Authelia container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ authelia_container_network }}"
```

#### Expose metrics publicly

If Authelia metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-authelia`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
authelia_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
authelia_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Installation

If you have decided to install the dedicated Valkey instance for Authelia, make sure to run the [installing](../installing.md) command for the supplementary host (`mash.example.com-authelia-deps`) first, before running it for the main host (`mash.example.com`).

Note that running the `just` commands for installation (`just install-all` or `just setup-all`) automatically takes care of the order. See [here](../running-multiple-instances.md#1-adjust-hosts) for more details about it.

## Usage

After running the command for installation, the Authelia instance becomes available at the URL specified with `authelia_hostname`. With the configuration above, the service is hosted at `https://authelia.example.com`.

To get started, open the URL with a web browser to log in to the portal website where you can and manage your user account.

## Related services

- [authentik](authentik.md) — Identity Provider focused on flexibility and versatility
- [Keycloak](keycloak.md) — Identity and access management solution
- [OAuth2-Proxy](oauth2-proxy.md) — Reverse proxy and static file server that provides authentication using OpenID Connect providers
- [Pocket ID](pocket-id.md) — OIDC provider for passkey-only authentication
- [Tinyauth](tinyauth.md) — Authentication middleware that adds a login screen or OAuth with providers to Docker services
