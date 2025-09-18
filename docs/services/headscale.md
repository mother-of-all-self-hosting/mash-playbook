<!--
SPDX-FileCopyrightText: 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Headscale

[Headscale](https://headscale.net/) is an open source, self-hosted implementation of the [Tailscale](https://tailscale.com/) control server.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# headscale                                                            #
#                                                                      #
########################################################################

headscale_enabled: true

headscale_hostname: headscale.example.com

########################################################################
#                                                                      #
# /headscale                                                           #
#                                                                      #
########################################################################
```

### Single-Sign-On (SSO) integration

Headscale supports Single-Sign-On (SSO) via OIDC. To make use of it, an Identity Provider (IdP) like [authentik](authentik.md), [Authelia](authelia.md) or [Tinyauth](tinyauth.md) needs to be set up.

As Headscale's built-in authentication is somewhat manual, setting up OIDC can provide a smoother user experience.

For example, you can enable SSO with authentik via OIDC by following the steps below.

Here, we are using Ansible Vault to supply both our `domain` as well as `client_id` and `client_secret`. Add the following configuration to your `vars.yml` file. This assumes that you picked the slug `headscale` in authentik when adding Headscale as an application. If not, replace `headscale` in `issuer: "https://authentik.{{ domain }}/application/o/headscale/"`.

```yaml
headscale_configuration_extension:
  oidc:
    only_start_if_oidc_is_available: true
    issuer: "https://authentik.{{ domain }}/application/o/headscale/"
    client_id: "{{ vault_headscale_client_id }}"
    client_secret: "{{ vault_headscale_client_secret }}"
    scope: ["openid", "profile", "email"]
    pkce:
      enabled: true
      method: S256
```

You can find more details about configuring OIDC by referring to the documentation at both [Headscale](https://headscale.net/stable/ref/oidc/?h=oidc) and [authentik](https://integrations.goauthentik.io/networking/headscale/). Note that Headscale's documentation doesn't explicitly cover authentik.

## Role

Take a look at:

- The [Headscale role](https://github.com/mother-of-all-self-hosting/ansible-role-headscale/)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-headscale/blob/main/defaults/main.yml) for additional variables that you can customize via your `vars.yml` file.

## Usage

After running the command for installation, the Headscale instance becomes available at the URL specified with `headscale_hostname` and `headscale_path_prefix`. With the configuration above, the service is hosted at `https://headscale.example.com`.

After installation, you would normally:

- first, [create some users](#creating-users)
- then, [connect some devices](#connecting-devices) by the official Tailscale applications, configured to talk to your own Headscale server

### Convenience script to call the binary

We provide a `/mash/headscale/bin/headscale` script on the server, which forwards commands to the `headscale` binary inside the container (`mash-headscale`).

Example usage: `/mash/headscale/bin/headscale version`

> [!WARNING]
> Command arguments which contain spaces may not be forwarded correctly.

### Creating users

To [create a user](https://headscale.net/stable/usage/getting-started/#create-a-user), run a command like this:

```sh
/usr/bin/env docker exec -it mash-headscale \
headscale users create \
john.doe \
--display-name "John Doe" \
--email "john.doe@example.com"
```

> [!WARNING]
> We use `docker exec` here because the [convenience script](#convenience-script-to-call-the-binary) does not handle forwarding arguments with spaces (like `--display-name`) correctly.

💡 You can [list the existing users](https://headscale.net/stable/usage/getting-started/#list-existing-users) with a command like this: `/mash/headscale/bin/headscale users list`

### Connecting devices

Here are some quick guides for the various platforms:

- [Android devices](https://headscale.net/stable/usage/connect/android/)
- [Apple devices](https://headscale.net/stable/usage/connect/apple/)
- [Windows devices](https://headscale.net/stable/usage/connect/windows/)
- Linux: install the `tailscale` CLI. See the official [Setting up Tailscale on Linux](https://tailscale.com/kb/1031/install-linux) documentation, or the [Archlinux Tailscale Wiki page](https://wiki.archlinux.org/title/Tailscale) (and specifically its [Third-party clients](https://wiki.archlinux.org/title/Tailscale#Third-party_clients) section for GUI clients).

All of these platforms would require confirmation after initial login, so consult the [Connecting Linux devices with manual confirmation](#connecting-linux-devices-with-manual-confirmation) section below for details on how to do it.

#### Connecting Linux devices with manual confirmation

To connect a Linux device, you can use a `tailscale up` command like this:

```sh
tailscale up --login-server=https://headscale.example.com
```

💡 You may wish to add additional arguments to this command, such as `--hostname`, `--advertise-exit-node`, `--advertise-routes`, etc. These settings can also be configured later using `tailscale set` (e.g. `tailscale set --hostname=custom-hostname-for-my-device`).

Running the `tailscale up` command will print a URL you need to open in your browser to complete the setup.

The URL would contain a `headscale` command you need to run. It looks something like this:

```sh
headscale nodes register --user USERNAME --key mkey:....
```

Take this command and:

- replace the `headscale` prefix with `/mash/headscale/bin/headscale`
- replace `USERNAME` with the username of a valid [user you created](#creating-users) earlier
- run it on the Headscale server

#### Connecting Linux devices with a preshared key

Instead of following the manual back-and-forth flow as specified in [Connecting Linux devices with manual confirmation](#connecting-linux-devices-with-manual-confirmation), you can also use a preshared key to connect your device.

First, generate a preshared key:

```sh
/mash/headscale/bin/headscale preauthkeys create --user=john.doe
```

You can then connect your device with the preshared key:

```sh
tailscale up --login-server=https://headscale.example.com --auth-key=...
```

The device will be automatically connected to the Headscale server, without any additional approval steps.
