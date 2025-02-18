<!--
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Jitsi

The playbook can install and configure the [Jitsi](https://jitsi.org/) video-conferencing platform for you.

The Ansible role for Jitsi is developed and maintained by [MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi). For details about configuring Jitsi, you can check them via:
- [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/docs/configuring-jitsi.md)
- `roles/galaxy/jitsi/docs/configuring-jitsi.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# jitsi                                                                #
#                                                                      #
########################################################################

jitsi_enabled: true

jitsi_hostname: mash.example.com
jitsi_path_prefix: /jitsi

########################################################################
#                                                                      #
# /jitsi                                                               #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/jitsi`.

You can remove the `jitsi_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

**Note**: there are minor quirks when hosting under a subpath, such as:

- [When hosting under a subpath, pwa-worker.js is attempted to be loaded from the base domain without a subpath](https://github.com/jitsi/docker-jitsi-meet/issues/1515)
- [When hosting under a subpath, ending the meeting redirects to the base domain without subpath](https://github.com/jitsi/docker-jitsi-meet/issues/1514)


### Authentication

By default the Jitsi Meet instance **does not require any kind of login and is open to use for anyone without registration**.

If you're fine with such an open Jitsi instance, please skip ahead.

If you would like to control who is allowed to open meetings on your new Jitsi instance, then please follow the following steps to enable Jitsi's authentication and optionally guests mode.
Currently, there are three supported authentication modes: `internal` (default), `matrix` and `ldap`.

**Note:** Authentication is not tested via the playbook's self-checks.
We therefore recommend that you manually verify if authentication is required by Jitsi.
For this, try to manually create a conference in your browser.


#### Authenticate using Jitsi accounts (Auth-Type 'internal')

The default authentication mechanism is `internal` auth, which requires Jitsi accounts to be setup and is the recommended setup.

With authentication enabled, all meeting rooms have to be opened by a registered user, after which guests are free to join.
If a registered host is not yet present, guests are put on hold in individual waiting rooms.

Use the following **additional** configuration:

```yaml
jitsi_enable_auth: true
jitsi_enable_guests: true
jitsi_prosody_auth_internal_accounts:
  - username: "jitsi-moderator"
    password: "secret-password"
  - username: "another-user"
    password: "another-password"
```

**Caution:** Accounts added here and subsequently removed will not be automatically removed from the Prosody server until user account cleaning is integrated into the [ansible-role-jitsi](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi) Ansible role.

**If you get an error** like this: "Error: Account creation/modification not supported.", it's likely that you had previously installed Jitsi without auth/guest support. In such a case, you should look into [Rebuilding your Jitsi installation](#rebuilding-your-jitsi-installation).


#### Authenticate using Matrix OpenID (Auth-Type 'matrix')

Using this authentication type require a [Matrix User Verification Service](https://github.com/matrix-org/matrix-user-verification-service).

This playbook does **not** support installing the Matrix User Verification Service. You can install this service with the [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy) playbook. See the [Setting up Matrix User Verification Service](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/configuring-playbook-user-verification-service.md) documentation for `matrix-docker-ansible-deploy`.

To enable Matrix auth for a Jitsi installation managed by this playbook, use this **additional** configuration:

```yaml
jitsi_enable_auth: true
jitsi_auth_type: matrix

# Auth token for Matrix User Verification Service
jitsi_prosody_auth_matrix_uvs_auth_token: ''
# URL where Matrix User Verification Service is hosted
jitsi_prosody_auth_matrix_uvs_location: ''
```

You may also wish to see the [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy) playbook's [Authenticate using Matrix OpenID (Auth-Type 'matrix')](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/configuring-playbook-jitsi.md#authenticate-using-matrix-openid-auth-type-matrix) documentation section.


### Authenticate using LDAP (Auth-Type 'ldap')

An example LDAP configuration could be:

```yaml
jitsi_enable_auth: true
jitsi_auth_type: ldap
jitsi_ldap_url: "ldap://ldap.DOMAIN"
jitsi_ldap_base: "OU=People,DC=DOMAIN"
#jitsi_ldap_binddn: ""
#jitsi_ldap_bindpw: ""
jitsi_ldap_filter: "uid=%u"
jitsi_ldap_auth_method: "bind"
jitsi_ldap_version: "3"
jitsi_ldap_use_tls: true
jitsi_ldap_tls_ciphers: ""
jitsi_ldap_tls_check_peer: true
jitsi_ldap_tls_cacert_file: "/etc/ssl/certs/ca-certificates.crt"
jitsi_ldap_tls_cacert_dir: "/etc/ssl/certs"
jitsi_ldap_start_tls: false
```

For more information refer to the [docker-jitsi-meet](https://github.com/jitsi/docker-jitsi-meet#authentication-using-ldap) and the [saslauthd `LDAP_SASLAUTHD`](https://github.com/winlibs/cyrus-sasl/blob/master/saslauthd/LDAP_SASLAUTHD) documentation.


### Networking

**In addition** to ports `80` and `443` exposed by the [Traefik](traefik.md) reverse-proxy, the following ports will be exposed by the Jitsi containers on **all network interfaces**:

- `4443` over **TCP**, controlled by `jitsi_jvb_rtp_tcp_port` - RTP media fallback over TCP
- `10000` over **UDP**, controlled by `jitsi_jvb_rtp_udp_port` - RTP media over UDP. Depending on your firewall/NAT setup, incoming RTP packets on port `10000` may have the external IP of your firewall as destination address, due to the usage of STUN in JVB (see [`jitsi_jvb_stun_servers`](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi/blob/main/defaults/main.yml)).

Docker automatically opens these ports in the server's firewall, so you **likely don't need to do anything**. If you use another firewall in front of the server, you may need to adjust it.

To learn more, see the upstream [Firewall documentation](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-docker/#external-ports).


### (Optional) Making your Jitsi server work on a LAN

By default the Jitsi Meet instance does not work with a client in LAN (Local Area Network), even if others are connected from WAN. There are no video and audio. In the case of WAN to WAN everything is ok.

The reason is the Jitsi VideoBridge git to LAN client the IP address of the docker image instead of the host. The [documentation](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-docker/#running-behind-nat-or-on-a-lan-environment) of Jitsi in docker suggest to add `JVB_ADVERTISE_IPS` in enviornment variable to make it work.

Here is how to do it in the playbook.

Use the following **additional** configuration:

```yaml
jitsi_jvb_container_extra_arguments:
  - '--env "JVB_ADVERTISE_IPS=<Local IP address of the host>"'
```

### Additional configuration

#### (Optional) Fine tune Jitsi

Sample **additional** configuration to save up resources (explained below):

```yaml
jitsi_web_custom_config_extension: |
  config.enableLayerSuspension = true;

  config.disableAudioLevels = true;

  // Limit the number of video feeds forwarded to each client
  config.channelLastN = 4;

jitsi_web_config_resolution_width_ideal_and_max: 480
jitsi_web_config_resolution_height_ideal_and_max: 240
```

You may want to **suspend unused video layers** until they are requested again, to save up resources on both server and clients.
Read more on this feature [here](https://jitsi.org/blog/new-off-stage-layer-suppression-feature/)

You may wish to **disable audio levels** to avoid excessive refresh of the client-side page and decrease the CPU consumption involved.

You may want to **limit the number of video feeds forwarded to each client**, to save up resources on both server and clients. As clients' bandwidth and CPU may not bear the load, use this setting to avoid lag and crashes.
This feature is found by default in other webconference applications such as Office 365 Teams (limit is set to 4).
Read how it works [here](https://github.com/jitsi/jitsi-videobridge/blob/master/doc/last-n.md) and performance evaluation on this [study](https://jitsi.org/wp-content/uploads/2016/12/nossdav2015lastn.pdf).

You may want to **limit the maximum video resolution**, to save up resources on both server and clients.

#### (Optional) Specify a Max number of participants on a Jitsi conference

The playbook allows a user to set a max number of participants allowed to join a Jitsi conference. By default there is no limit.

In order to set the max number of participants use the following **additional** configuration:

```yaml
jitsi_prosody_max_participants: 4 # example value
```


#### (Optional) Disable Gravatar

In the default upstream Jisti Meet configuration, [gravatar.com](https://gravatar.com/) is enabled as an avatar service. This results in third party request leaking data to Gravatar.

To disable Gravatar integration, use the following **additional** configuration:

```yaml
jitsi_disable_gravatar: false
```

## Usage

After installation, you can go to the [Jitsi URL](#url) and start an audio/video conference.


## Troubleshooting

### Rebuilding your Jitsi installation

**If you ever run into any trouble** or **if you change configuration (`jitsi_*` variables) too much**, we urge you to rebuild your Jitsi setup.

We normally don't require such manual intervention for other services, but Jitsi services generate a lot of configuration files on their own.

These files are not all managed by Ansible (at least not yet), so you may sometimes need to delete them all and start fresh.

To rebuild your Jitsi configuration:

- ask Ansible to stop all Jitsi services: `just run-tags stop-group --extra-vars=group=jitsi`
- SSH into the server and do this and remove all Jitsi configuration & data (`rm -rf /mash/jitsi`)
- ask Ansible to set up Jitsi anew and restart services (`just install-service jitsi`)
