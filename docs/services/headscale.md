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

### URL

In the example configuration above, we configure the service to be hosted at `https://headscale.example.com`.

The `headscale_path_prefix` variable can be adjusted to host Headscale under a subpath (e.g. `headscale_path_prefix: /headscale`) on the given hostname.


## Usage

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
