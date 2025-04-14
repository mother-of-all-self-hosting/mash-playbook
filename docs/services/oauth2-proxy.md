# OAuth2-Proxy

[OAuth2-Proxy](https://oauth2-proxy.github.io/oauth2-proxy/) is a reverse proxy and static file server that provides authentication using OpenID Connect Providers (Google, GitHub, [Authentik](authentik.md), [Keycloak](keycloak.md), and others) to SSO-protect services which do not support SSO natively.


## Modes of operation

OAuth2-Proxy can be used in 2 different modes:

1. Capturing incoming traffic for the app (e.g. https://app.example.com/), and then proxying it to the application container if the user is authenticated

2. Letting the application itself capture incoming traffic for itself (on https://app.example.com/) and use Traefik's [ForwardAuth](https://doc.traefik.io/traefik/middlewares/http/forwardauth/) middleware to authenticate the request via OAuth2-Proxy. In this case, OAuth2-Proxy will only handle the `/oauth2/` prefix on the application domain (e.g. https://app.example.com/oauth/).

The 1st one is a bit invasive, as it requires moving all custom reverse-proxying configuration for the handled domain to the OAuth2-Proxy side.

The 2nd one lets you keep the existing application configuration. However, it needs all URLs to go to one service (the application) with the exception of `/oauth2/` (which should go to OAuth2-Proxy). As such, it it requires that both services (the application and OAuth2-Proxy) run on the same machine.

Our [Sample configuration](#sample-configuration) below uses [ForwardAuth](https://doc.traefik.io/traefik/middlewares/http/forwardauth/).

The [OAuth2-Proxy Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-oauth2-proxy) should be flexible enough to let you reconfigure it for both modes of operation. However, if feasible, we recommend using the 2nd (ForwardAuth) method.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server
- an OIDC provider running anywhere. See [Choosing a provider](#choosing-a-provider).


## Choosing a provider

To use OAuth2-Proxy, you need to choose an [OIDC provider](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/).

This can be any of the supported providers. If hosting your own (via this playbook or via other means), the OIDC provider may be hosted anywhere (not necessarily on the same server as OAuth2-Proxy or the service you're SSO-protecting).


## Sample configuration

The configuration is [provider](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/)-specific and also depends on the the service you're SSO-protecting, on which server it runs (in relation to OAuth-Proxy), etc.

Below is a **sample** configuration for protecting a static website (in this case powered by the [Hubsite](hubsite.md)) service via [Keycloak](keycloak.md).

For this to work as described here, both OAuth2-Proxy and the protected service (e.g. [Hubsite](hubsite.md)) need to run on the same machine.

Keycloak may run anywhere.

You also need to have prepared Keycloak and a "Client app" for it, according to the [Keycloak OIDC](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/keycloak_oidc) documentation of OAuth2-Proxy.


#### OAuth2-Proxy configuration

```yaml
########################################################################
#                                                                      #
# oauth2_proxy                                                         #
#                                                                      #
########################################################################

oauth2_proxy_enabled: true

oauth2_proxy_environment_variable_provider: keycloak-oidc
oauth2_proxy_environment_variable_provider_display_name: SSO

oauth2_proxy_environment_variable_client_id: hubsite
oauth2_proxy_environment_variable_client_secret: ''
oauth2_proxy_environment_variable_oidc_issuer_url: https://keycloak.example.com/realms/my-realm
oauth2_proxy_environment_variable_redirect_url: "https://{{ hubsite_hostname }}/oauth2/callback"

oauth2_proxy_environment_variable_code_challenge_method: S256

# Generate this with: `python -c 'import os,base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())'`
oauth2_proxy_environment_variable_cookie_secret: ''

oauth2_proxy_container_labels_additional_labels: |
  traefik.http.routers.{{ oauth2_proxy_identifier }}-hubsite.rule=Host(`{{ hubsite_hostname }}`) && PathPrefix(`/oauth2/`)
  traefik.http.routers.{{ oauth2_proxy_identifier }}-hubsite.service={{ oauth2_proxy_identifier }}
  traefik.http.routers.{{ oauth2_proxy_identifier }}-hubsite.entrypoints={{ oauth2_proxy_container_labels_traefik_entrypoints }}
  traefik.http.routers.{{ oauth2_proxy_identifier }}-hubsite.tls={{ oauth2_proxy_container_labels_traefik_tls }}
  traefik.http.routers.{{ oauth2_proxy_identifier }}-hubsite.tls.certResolver={{ oauth2_proxy_container_labels_traefik_tls_certResolver }}

########################################################################
#                                                                      #
# /oauth2_proxy                                                        #
#                                                                      #
########################################################################
```

After adding this to your `vars.yml` file, [re-run the playbook](../installing.md): `just install-service oauth-2proxy`.

This merely configures OAuth2-Proxy to handle the `/oauth2/` paths for Hubsite's domain.

[Hubsite configuration adjustments](#hubsite-configuration-adjustments) are also necessary, so proceed to do those as well.


### Hubsite configuration adjustments

Now that OAuth2-Proxy is ready and handling the `/oauth2/` paths on the domain Hubsite is running, we need to set up Traefik's [ForwardAuth](https://doc.traefik.io/traefik/middlewares/http/forwardauth/) middlware, so that all Hubsite requests would consult OAuth2-Proxy.

The configuration described below is based on the official [Configuring for use with the Traefik (v2) ForwardAuth middleware](https://oauth2-proxy.github.io/oauth2-proxy/configuration/overview#configuring-for-use-with-the-traefik-v2-forwardauth-middleware) documentation of OAuth2-Proxy.

```yml
########################################################################
#                                                                      #
# hubsite                                                              #
#                                                                      #
########################################################################

# Your other Hubsite configuration goes here.
# See the documentation in hubsite.md.

hubsite_container_labels_additional_labels: |
  # Create a middleware which catches "unauthenticated" errors and serves the OAuth-Proxy sign in page.
  traefik.http.middlewares.{{ hubsite_identifier }}-oauth-errors.errors.status=401-403
  traefik.http.middlewares.{{ hubsite_identifier }}-oauth-errors.errors.service={{ oauth2_proxy_identifier }}
  traefik.http.middlewares.{{ hubsite_identifier }}-oauth-errors.errors.query=/oauth2/sign_in?rd={url}

  # Create a middlware which passes each incoming request to OAuth2-Proxy,
  # so it can decide whether it should be let through (to Hubsite) or should blocked (serving the OAuth2-Proxy sign in page).
  traefik.http.middlewares.{{ hubsite_identifier }}-oauth-auth.forwardAuth.address=http://{{ oauth2_proxy_identifier }}:{{ oauth2_proxy_container_process_http_port }}/oauth2/auth

  traefik.http.middlewares.{{ hubsite_identifier }}-oauth-auth.forwardAuth.trustForwardHeader=true

  # Let a few HTTP headers set by OAuth2-Proxy get passed to Hubsite.
  # Hubsite is a static website, so it cannot make use of them.
  # Nevertheless, this is here as an example of how you can whitelist headers,
  # so that applications which can make use of these headers can benefit from it.
  # See more information about this in the comments for `oauth2_proxy_environment_variable_set_xauthrequest`.
  traefik.http.middlewares.{{ hubsite_identifier }}-oauth-auth.forwardAuth.authResponseHeaders=X-Auth-Request-Preferred-Username, X-Auth-Request-Groups

  # Inject the 2 middlewares defined above into the router of the Hubsite service
  traefik.http.routers.{{ hubsite_identifier }}.middlewares={{ hubsite_identifier }}-oauth-errors,{{ hubsite_identifier }}-oauth-auth

########################################################################
#                                                                      #
# /hubsite                                                             #
#                                                                      #
########################################################################
```

After adding this to your `vars.yml` file, [re-run the playbook](../installing.md): `just install-service hubsite`.

Some [services](../supported-services.md) already define their own `middlewares` in their Traefik `labels` file, so you may not be able to inject new ones the same way as done for Hubsite above.

Specific services (e.g. [Nextcloud](./nextcloud.md)) provide Ansible variables (`nextcloud_container_labels_traefik_http_middlewares_custom`) for injecting new middlewares at a specific position (priority) in the list. Others services (Ansible roles) do not support this yet, which would prevent you from using them this way. Consider submitting an issue or better yet opening a PR to improve these services.


## Further reading

If you'd like to do something more advanced, the [`ansible-role-oauth2-proxy` Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-oauth2-proxy) is very configurable and should let you do what you need.

Take a look at [its `default/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-oauth2-proxy/blob/main/defaults/main.yml) for available Ansible variables you can use in your own `vars.yml` configuration file.


## Related services

- [authentik](authentik.md) — An open-source Identity Provider focused on flexibility and versatility.
- [Keycloak](keycloak.md) — An open source identity and access management solution
- [Authelia](authelia.md) — An open-source authentication and authorization server that can work as a companion to [common reverse proxies](https://www.authelia.com/overview/prologue/supported-proxies/) (like [Traefik](traefik.md) frequently used by this playbook)
