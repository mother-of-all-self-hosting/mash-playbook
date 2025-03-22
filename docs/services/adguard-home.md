# AdGuard Home

[AdGuard Home](https://adguard.com/en/adguard-home/overview.html/) is a network-wide DNS software for blocking ads & tracking.

> [!WARNING]
> Running a public DNS server is not advisable. You'd better install AdGuard Home in a trusted local network, or adjust its network interfaces and port exposure (via the variables in the [Networking](#networking) configuration section below) so that you don't expose your DNS server publicly to the whole world. If you're exposing your DNS server publicly, consider restricting who can use it by adjusting the **Allowed clients** setting in the **Access settings** section of **Settings** -> **DNS settings**.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# adguard-home                                                         #
#                                                                      #
########################################################################

adguard_home_enabled: true

adguard_home_hostname: mash.example.com

# Hosting under a subpath sort of works, but is not ideal
# (see the URL section below for details).
# Consider using a dedicated hostname and removing the line below.
adguard_home_path_prefix: /adguard-home

########################################################################
#                                                                      #
# /adguard-home                                                        #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/adguard-home`.

You can remove the `adguard_home_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

When **hosting under a subpath**, you may hit [this bug](https://github.com/AdguardTeam/AdGuardHome/issues/5478), which causes these **annoyances**:

- upon initial usage, you will be redirected to `/install.html` and would need to manually adjust this URL to something like `/adguard-home/install.html` (depending on your `adguard_home_path_prefix`). After the installation wizard completes, you'd be redirected to `/index.html` incorrectly as well.

- every time you hit the homepage and you're not logged in, you will be redirected to `/login.html` and would need to manually adjust this URL to something like `/adguard-home/login.html` (depending on your `adguard_home_path_prefix`)


### Networking

By default, the following ports will be exposed by the container on **all network interfaces**:

- `53` over **TCP**, controlled by `adguard_home_container_dns_tcp_bind_port` — used for DNS over TCP
- `53` over **UDP**, controlled by `adguard_home_container_dns_udp_bind_port` — used for DNS over UDP

Docker automatically opens these ports in the server's firewall, so you **likely don't need to do anything**. If you use another firewall in front of the server, you may need to adjust it.

To expose these ports only on **some** network interfaces, you can use additional configuration like this:

```yaml
# Expose only on 192.168.1.15
adguard_home_container_dns_tcp_bind_port: '192.168.1.15:53'
adguard_home_container_dns_udp_bind_port: '192.168.1.15:53'
```

## Usage

After installation, you can go to the AdGuard Home URL, as defined in `adguard_home_hostname` and `adguard_home_path_prefix`.

As mentioned in the [URL](#url) section above, you may hit some annoyances when hosting under a subpath.

The first time you visit the AdGuard Home pages, you'll go through a setup wizard **make sure to set the HTTP port under "Admin Web Interface" to `3000`**. This is the in-container port that our Traefik setup expects and uses for serving the install wizard to begin with. If you go with the default (`80`), the web UI will stop working after the installation wizard completes.

Things you should consider doing later:

- increasing the per-client Rate Limit (from the default of `20`) in the **DNS server configuration** section in **Settings** -> **DNS Settings**
- enabling caching in the **DNS cache configuration** section in **Settings** -> **DNS Settings**
- adding additional blocklists by discovering them on [Firebog](https://firebog.net/) or other sources and importing them from **Filters** -> **DNS blocklists**
- reading the AdGuard Home [README](https://github.com/AdguardTeam/AdGuardHome/blob/master/README.md) and [Wiki](https://github.com/AdguardTeam/AdGuardHome/wiki)


## Troubleshooting and workaround

Adguard Home does not currently support being setup with a non-`root` account (see [issue](https://github.com/AdguardTeam/AdGuardHome/issues/4714)). As the playbook uses the user `mash` when starting services, you will likely encounter the following error when `adguard-home.service` tries to start for the first time:

```
mar 02 19:11:59 $hostname mash-adguard-home[872496]: 2024/03/02 18:11:59.706251 [info] Checking if AdGuard Home has necessary permissions
mar 02 19:11:59 $hostname mash-adguard-home[872496]: 2024/03/02 18:11:59.706257 [fatal] This is the first launch of AdGuard Home. You must run it as Administrator.
```

You can workaround this issue by editing `mash-adguard-home.service` and temporarily make it start Adguard Home as the `root` user for the first time, and then revert it back to using a regular user afterwards. Follow the steps below, which require you to be `root` to execute the commands:

1. Run `systemctl edit --full mash-adguard-home.service` to edit Adguard Home's service file and remove or comment out the line starting with `--user` (e.g. `--user=996:3992 \` — the numbers represent the uid/gid of the `mash` user, so your values may be different):

	```
	ExecStartPre=/usr/bin/env docker create \
	                        --rm \
	                        --name=mash-adguard-home \
	                        --log-driver=none \
	                        --user=996:3992 \  <--- remove temporarily
	```

2. Run `systemctl restart mash-adguard-home.service` to restart the service.
3. Perform the first time setup as documented under [usage](#usage).
4. Run `systemctl stop mash-adguard-home.service` to stop the service.
5. Run `chown -R mash:mash /mash/adguard-home/workdir` to change ownership of the files created during the first-time setup from `root` to `mash`. Optionally, use `ls -ll /mash/adguard-home/workdir` to check the file ownership before and after running `chown`.
6. Run the playbook again to rebuild `/etc/systemd/system/mash-adguard-home.service` and start AdGuard Home again: `just install-service adguard-home.service`.
7. If you didn't get any errors, Adguard Home should be running correctly. You can also check on the service with: `journalctl -fu mash-adguard-home.service`.
