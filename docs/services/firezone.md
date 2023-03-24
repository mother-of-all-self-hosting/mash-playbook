# Firezone

[Firezone](https://www.firezone.dev/) is a self-hosted VPN server with Web UI that this playbook can install using the ansible role [moan0s/role-firezone](https://github.com/moan0s/role-firezone).

To enable Firezone add the following to your `vars.yml`:

```yaml
##############
## FIREZONE ##
##############

firezone_enabled: true
firezone_hostname: example.org

firezone_default_admin_email: "user@invalid.org"
firezone_default_admin_password: "<securepassword>"

# Generate this with `openssl rand -base64 32`
firezone_database_encryption_key: "<secret>"
```

Use `just run-tags firezone-create-or-reset-admin` to create the configured
admin account or reset the password to the password set in `vars.yml`.
