# APISIX Dashboard

[APISIX Dashboard](https://apisix.apache.org/docs/dashboard/USER_GUIDE/) is a web UI for [APISIX Gateway](./apisix-gateway.md).

It works by directly editing the [etcd](./etcd.md) database that APISIX Gateway stores its data in.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- an [etcd](etcd.md) key-value store
- (optional) [APISIX Gateway](./apisix-gateway.md) — there's no point in administrating APISIX Gateway configuration stored in etcd without having an APISIX Gateway instance to initialize and consume it


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# apisix_dashboard                                                     #
#                                                                      #
########################################################################

apisix_dashboard_enabled: true

apisix_dashboard_hostname: dashboard.api.example.com

# A strong secret for JWT authentication
apisix_dashboard_config_authentication_secret: ''

apisix_dashboard_config_authentication_users:
  - username: admin
    password: password-here

########################################################################
#                                                                      #
# /apisix_dashboard                                                    #
#                                                                      #
########################################################################
```

If you'd like to do something more advanced, the [`ansible-role-apisix-dashboard` Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-apisix-dashboard) is very configurable and should not get in your way of exposing ports or configuring arbitrary settings.

Take a look at [its `default/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-apisix-dashboard/blob/main/defaults/main.yml) for available Ansible variables you can use in your own `vars.yml` configuration file.

### URL

In the example configuration above, we configure APISIX Dashboard to expose itself at: `https://dashboard.api.example.com`

### Authentication

The example above uses the built-in login page of APISIX Dashboard with a list of users is defined via `apisix_dashboard_config_authentication_users`.

APISIX Dashboard also supports OpenID Connect providers. It can be enabled and configured via various `apisix_dashboard_config_oidc_*` Ansible variables.


## Usage

After installation, you can visit the APISIX Dashboard URL and authenticate with a credential as specified in `apisix_dashboard_config_authentication_users`. If you've enabled OpenID Connect, you may also be able to authenticate with that.
