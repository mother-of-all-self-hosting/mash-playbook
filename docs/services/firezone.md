# Firezone

[Firezone](https://www.firezone.dev/) is a self-hosted VPN server with Web UI that this playbook can install using the ansible role [moan0s/role-firezone](https://github.com/moan0s/role-firezone).

To enable Firezone add the following to your `vars.yml`:

```yaml
##############
## FIREZONE ##
##############

firezone_enabled: true
firezone_hostname: vpn.example.org

firezone_default_admin_email: "user@invalid.org"
firezone_default_admin_password: "<securepassword>"

# Generate this with `openssl rand -base64 32`
firezone_database_encryption_key: "<secret>"
```

Use `just run-tags firezone-create-or-reset-admin` to create the configured
admin account or reset the password to the password set in `vars.yml`.

### Networking

By default, the following ports will be exposed by the container on **all network interfaces**:

- `51820` over **UDP**, controlled by `firezone_wireguard_bind_port` - used for your wireguard connections

Docker automatically opens these ports in the server's firewall, so you **likely don't need to do anything**. If you use another firewall in front of the server, you may need to adjust it.

### Usage

After you started the service you can login at vpn.example.org with the credentials set in `firezone_default_admin_email/password`.
After that refer to the [official documentation](https://www.firezone.dev/docs/user-guides/add-devices/) to add devices and more.
