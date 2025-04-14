# Authelia

[Authelia](https://www.authelia.com/) is an open-source [authentication](https://www.authelia.com/overview/authentication/introduction/) and [authorization](https://www.authelia.com/overview/authorization/access-control/) server and portal fulfilling the identity and access management (IAM) role of information security in providing [multi-factor authentication](https://www.authelia.com/overview/authentication/introduction/) and single sign-on (SSO) for your applications via a web portal.

Authelia has 2 [modes of operation](#modes-of-operation) (Forward-Auth and OpenID Connect). Read below for more information.

> [!WARNING]
> This service is a new addition to the playbook. It may not fully work or be configured in a suboptimal manner.


## Dependencies

This service requires the following other services:

- a database
  - (optional) a [Postgres](postgres.md) database — if enabled for your Ansible inventory host, Authelia will be connected to the Postgres server automatically
  - (optional) a MySQL / [MariaDB](mariadb.md) database — if enabled for your Ansible inventory host (and you don't also enable Postgres), Authelia will be connected to the MariaDB server automatically
  - or SQLite, used by default when none of the above database choices is enabled for your Ansible inventory host

- (optional, but recommended) [Valkey](valkey.md)
  - for storing session information in a persistent manner
  - if Valkey is not enabled, session information is stored in-memory and restarting Authelia destroys user sessions

- a [Traefik](traefik.md) reverse-proxy server
  - for serving the Authelia portal website
  - for protecting other Traefik-based services by adding the Authelia forward-auth middleware to them when [Protecting services with Authelia's forward-auth](#protecting-a-service-with-authelias-forward-auth)


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# authelia                                                             #
#                                                                      #
########################################################################

authelia_enabled: true

authelia_hostname: authelia.example.com

# The base domain that session cookies related to authentication will be set on.
#
# Forward-auth services that you will protect need to be hosted on subdomains under this base domain.
# (e.g. service1.example.com, service2.example.com)
#
# For OpenID Connect-protected services, this value does not matter.
#
# In any case, `authelia_config_session_domain` needs to be a subdomain of `authelia_hostname`.
authelia_config_session_domain: example.com

# The database encryption password.
# Changing this subsequently will cause trouble unless you use the CLI to migrate.
# Generating a strong password (e.g. `pwgen -s 64 1`) is recommended.
authelia_config_storage_encryption_key: ''

# Authelia supports either LDAP or a file-based authentication (user) database.
#
# Using the file-based database is easiest and it's what we do by default here
# by defining `authelia_config_authentication_backend_file_content`.
#
# To use LDAP, remove `authelia_config_authentication_backend_file_content` and define various
# `authelia_config_authentication_backend_ldap_*` variables.
authelia_config_authentication_backend_file_content: |
  ---
  users:
    john:
      disabled: false
      displayname: John Doe
      password: PASSWORD_HASH_HERE
      email: john@example.com
      groups:
        - admins
        - dev
    peter:
      disabled: false
      displayname: Peter Johnson
      password: PASSWORD_HASH_HERE
      email: peter@example.com
      groups:
        - dev
  ...

# You can define various authentication rules for each protected service here.
authelia_config_access_control_rules:
 - domain: 'service1.example.com'
   policy: one_factor

# The configuration below connects Authelia to the Valkey instance, for session storage purposes.
# You may wish to run a separate Valkey instance for Authelia, because Valkey is not multi-tenant.
# Read more in docs/services/redis.md.
# If Valkey is not available, session data will be stored in memory and will be lost on container restart.
authelia_config_session_redis_host: "{{ valkey_identifier if valkey_enabled else '' }}"

########################################################################
#                                                                      #
# /authelia                                                            #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://authelia.example.com`.

While the Authelia Ansible role provides an `authelia_path_prefix` variable, Authelia does not support being hosted at a subpath right now.

On the Authelia base URL, there's a portal website where you can log in and manage your user account.


### Session storage

As mentioned in the default configuration above (see `authelia_config_session_redis_host`), you may wish to run [Valkey](valkey.md) for storing session data.

You may wish to run a separate Valkey instance for Authelia, because Valkey is not multi-tenant. See [our Valkey documentation page](valkey.md) for additional details. When running a separate instance of Valkey, you may need to connect Authelia to the Valkey instance's container network via the `authelia_container_additional_networks_custom` variable.


### Authentication storage providers

Authelia supports [LDAP](https://www.authelia.com/configuration/first-factor/ldap/) and [file-based](https://www.authelia.com/configuration/first-factor/file/) storage providers for the user database.

The default configuration above enables the file-based provider with the `authelia_config_authentication_backend_file_content` variable.

To use LDAP, remove the `authelia_config_authentication_backend_file_content` variable and define a bunch of `authelia_config_authentication_backend_ldap_*` variables.


### Modes of operation

Authelia has 2 [modes of operation](#modes-of-operation) which can be enabled simultaneously:

- **Forward-Auth**: [Forward-Auth](https://doc.traefik.io/traefik/middlewares/http/forwardauth/) is useful for protecting services which are not aware of authentication at all or which can receive authentication/authorization data via [HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers). Forward-Auth can act as a replacement for [HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication). It does this by acting as a companion to [common reverse proxies](https://www.authelia.com/overview/prologue/supported-proxies/), like [Traefik](traefik.md) which is frequently used by this playbook. To learn more, see [Protecting a service with Authelia's forward-auth](#protecting-a-service-with-authelias-forward-auth)

- **OpenID Connect**: experimental OpenID Connect support support, so that services which are OpenID Connect-compatible can use Authelia as an identity provider. To learn more, see [Protecting a service with OpenID Connect](#protecting-a-service-with-openid-connect)


#### Protecting a service with Authelia's forward-auth

If you're using [Traefik](traefik.md), you can easily protect services running on the same host by adding additional Traefik labels to them.

[Forward-Auth](https://doc.traefik.io/traefik/middlewares/http/forwardauth/) is useful for protecting services which are not aware of authentication at all or which can receive authentication/authorization data via [HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers).

Here's an example configuration for [Hubsite](hubsite.md) (a service which does not support authentication at all):

```yaml
hubsite_container_labels_additional_labels: |
  traefik.http.routers.{{ hubsite_identifier }}.middlewares={{ authelia_identifier }}@docker
```

The Hubsite component does not use any Traefik middlewares, so defining a `.middlewares` configuration key and pointing it to the Authelia middleware works well.

For most other components, middlewares are in use in their default Traefik labels, so adding an additional `.middlewares` key will not work. You may need to inject additional middlewares on top of the default ones. Not all components may (yet) have a variable for doing so. Consider contributing to various roles to allow additional middlewares to be injected dynamically!


#### Protecting a service with OpenID Connect

For services which support OpenID Connect, you can enable the [experimental OpenID Connect identity provider](https://www.authelia.com/configuration/identity-providers/open-id-connect/) in Authelia.

You will need some additional configuration like this:

```yaml
authelia_config_identity_providers_oidc_clients:
  - id: grafana
    description: Grafana
    secret: HASH_OF_THE_SHARED_SECRET
    public: false
    authorization_policy: one_factor
    redirect_uris:
      - https://mash.example.com/grafana/login/generic_oauth
    scopes:
      - openid
      - profile
      - groups
      - email
    userinfo_signing_algorithm: none

authelia_config_identity_providers_oidc_issuer_private_key: |
  KEY CONTENT GOES HERE.
  TO GENERATE A KEY, USE: `openssl genpkey -algorithm RSA -out FILE_NAME`
```

The example configuration above configures a single OpenID Connect client (application) called `grafana` (see the [Grafana](grafana.md) service supported by this playbook), which supposedly lives at the base URL of `https://mash.example.com/grafana`.

You will need to create a shared secret and hash its value (e.g. `php -r 'echo password_hash("PASSWORD_HERE",  PASSWORD_ARGON2ID);'`). Feel free to use another language (or tool) for creating a hash as well. A few different hash algorithms are supported besides Argon2id.

Finally, configure your application, hooking it to Authelia's OpenID Connect identity provider.
You can get inspired by the [sample configuration](grafana.md#single-sign-on--authelia) we have created for [Grafana](grafana.md).

## Extending the Authelia configuration

The Authelia Ansible role provides various variables for configuring Authelia. You can see their default values in the [`defaults/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-authelia/blob/main/defaults/main.yml) of the Authelia role.

If a dedicated variable is not available for you to use or if you wish to override some hardcoded default, you can always use the `authelia_configuration_extension_yaml` Ansible variable for extending/overriding the default configuration.

## Related services

- [authentik](authentik.md) — An open-source Identity Provider focused on flexibility and versatility.
- [Keycloak](keycloak.md) — An open source identity and access management solution
- [OAuth2-Proxy](oauth2-proxy.md) — A reverse proxy and static file server that provides authentication using OpenID Connect Providers (Google, GitHub, [Authentik](authentik.md), [Keycloak](keycloak.md), and others) to SSO-protect services which do not support SSO natively
