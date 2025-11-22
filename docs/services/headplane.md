<!--
SPDX-FileCopyrightText: 2025 spatterlight

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Headplane

[Headplane](https://headplane.net/) is an open source, self-hosted implementation of the [Tailscale Web UI](https://tailscale.com/) for [Headscale](headscale.md).

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- a [Headscale](headscale.md) server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# headplane                                                            #
#                                                                      #
########################################################################

headplane_enabled: true

headplane_hostname: headplane.example.com
headplane_cookie_secret: "{{ vault_headplane_cookie_secret }}"

########################################################################
#                                                                      #
# /headplane                                                           #
#                                                                      #
########################################################################
```

`headplane_cookie_secret` is required and must be a 32-character secret used to encrypt Headplane session cookies. Generate one (for example `pwgen -s 32 1`) and store it in your vault (`inventory/host_vars/<your-domain>/vault.yml`) as `vault_headplane_cookie_secret`.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- The [Headplane role](https://github.com/spatterIight/ansible-role-headplane/)'s [`defaults/main.yml`](https://github.com/spatterIight/ansible-role-headplane/blob/main/defaults/main.yml) for additional variables that you can customize via your `vars.yml` file.
- The [Headplane example configuration](https://github.com/tale/headplane/blob/main/config.example.yaml) for all the possible configuration options (like OIDC).

## Usage

After running the command for installation, the Headplane instance becomes available at the URL specified with `headplane_hostname`. With the configuration above, the service is hosted at `https://headplane.example.com/admin`.

The application being hosted at `/admin` is [not easily configurable](https://github.com/tale/headplane/blob/main/docs/install/native-mode.md#custom-path-prefix). The default configuration is to automatically redirect `/` requests to `/admin`.

> [!NOTE]
> The `headplane_path_prefix` variable can be adjusted to host under a subpath (e.g. `headplane_path_prefix: /headplane`), but this hasn't been tested yet.

### Logging in

To [login to headplane](https://headplane.net/install/docker#accessing-headplane), run a command using the [Headscale convenience script](headscale.md#convenience-script-to-call-the-binary) like this:

```sh
/mash/headscale/bin/headscale apikeys create
```

Then login to `https://headplane.example.com/admin` by entering the generated API key.

### Modifying DNS

To modify Headscale DNS in Headplane some variables should be adjusted:

```yaml
headscale_extra_records_path_enabled: true
headplane_headscale_config_path_mount_options: readwrite
```

Otherwise you'll see an error like: "The Headscale configuration is read-only. You cannot make changes to the configuration"

Be careful making changes outside of the `DNS Records` section, since many of other configuration options will directly modify the Headscale configuration file managed by Ansible -- this is likely to lead to conflicts. The `DNS Records` section does not have this issue since it uses a separate file (`extra_records.json`).

### Modifying Access Control Lists

To modify Headscale ACL's you'll need to adjust the Headscale configuration:

```yaml
headscale_config_policy_mode: database
```

Otherwise you'll see an error like: "The ACL policy mode is set to `file` in your Headscale configuration. This means that the ACL file cannot be edited through the web interface."
