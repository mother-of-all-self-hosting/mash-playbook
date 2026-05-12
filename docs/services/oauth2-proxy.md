<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# OAuth2-Proxy

The playbook can install and configure [OAuth2-Proxy](https://github.com/oauth2-proxy/oauth2-proxy) for you.

OAuth2-Proxy is a reverse proxy and static file server that provides authentication using OpenID Connect Providers (Google, GitHub, [authentik](authentik.md), [Keycloak](keycloak.md), and others) to SSO-protect services which do not support SSO natively.

See the project's [documentation](https://oauth2-proxy.github.io/oauth2-proxy/) to learn what OAuth2-Proxy does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [OIDC provider](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/) —  This may be hosted anywhere; not necessarily on the same server as OAuth2-Proxy or the service you're SSO-protecting
- [Traefik](traefik.md) reverse-proxy server

## Operation modes

OAuth2-Proxy can be used in two different modes:

1. Capturing incoming traffic for the app (e.g. <https://app.example.com/>), and then proxying it to the application container if the user is authenticated

2. Letting the application itself capture incoming traffic for itself (on <https://app.example.com/>) and use Traefik's [ForwardAuth](https://doc.traefik.io/traefik/middlewares/http/forwardauth/) middleware to authenticate the request via OAuth2-Proxy. In this case, OAuth2-Proxy will only handle the `/oauth2/` prefix on the application domain (e.g. <https://app.example.com/oauth2/>).

The first one is a bit invasive, as it will require all custom reverse-proxying configuration for the handled domain to be moved to the OAuth2-Proxy side.

The second one lets you keep the existing application configuration. However, this mode needs all URLs to go to one service (the application) with the exception of `/oauth2/` (which should go to OAuth2-Proxy). As such, it requires that both services (the application and OAuth2-Proxy) run on the same machine.

Our sample configuration below uses [ForwardAuth](https://doc.traefik.io/traefik/middlewares/http/forwardauth/). While the [Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-oauth2-proxy) which this playbook incorporates to manage the service should be flexible enough to let you reconfigure it for both modes, we recommend using the second (ForwardAuth) method if feasible.

## Sample configuration

Below is a sample configuration for protecting a static website (in this case powered by the [Hubsite](hubsite.md)) service with [Keycloak](keycloak.md). For this to work as described, both OAuth2-Proxy and the protected service need to run on the same machine. Keycloak may run anywhere.

>[!NOTE]
>
> - The configuration is specific to [providers](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/) and also depends on which service you're SSO-protecting, on which server it runs (in relation to OAuth-Proxy), etc.
> - You also need to have prepared Keycloak and a "Client app" for it. Please refer to the [Keycloak OIDC](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/keycloak_oidc) documentation on configuring OAuth2-Proxy.

### OAuth2-Proxy configuration

```yaml
########################################################################
#                                                                      #
# oauth2_proxy                                                         #
#                                                                      #
########################################################################

oauth2_proxy_enabled: true

oauth2_proxy_environment_variable_provider: keycloak-oidc
oauth2_proxy_environment_variable_provider_display_name: SSO

# Authorize oauth2-proxy with your OIDC credentials
oauth2_proxy_environment_variable_client_id: ""
oauth2_proxy_environment_variable_client_secret: ""
oauth2_proxy_environment_variable_oidc_issuer_url: https://keycloak.example.com/realms/my-realm
oauth2_proxy_environment_variable_redirect_url: "https://{{ navidrome_hostname }}/oauth2/callback"

oauth2_proxy_environment_variable_code_challenge_method: S256

# Generate this with: `python3 -c 'import os,base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())'`
oauth2_proxy_environment_variable_cookie_secret: ''

# Serve the OAuth2-Proxy authentication page
oauth2_proxy_container_labels_additional_labels_custom:
  - traefik.http.routers.{{ oauth2_proxy_identifier }}-navidrome.rule=Host(`{{ navidrome_hostname }}`) && PathPrefix(`/oauth2/`)
  - traefik.http.routers.{{ oauth2_proxy_identifier }}-navidrome.service={{ oauth2_proxy_identifier }}
  - traefik.http.routers.{{ oauth2_proxy_identifier }}-navidrome.entrypoints={{ oauth2_proxy_container_labels_traefik_entrypoints }}
  - traefik.http.routers.{{ oauth2_proxy_identifier }}-navidrome.tls={{ oauth2_proxy_container_labels_traefik_tls }}
  - traefik.http.routers.{{ oauth2_proxy_identifier }}-navidrome.tls.certResolver={{ oauth2_proxy_container_labels_traefik_tls_certResolver }}

########################################################################
#                                                                      #
# /oauth2_proxy                                                        #
#                                                                      #
########################################################################
```

After adding this to your `vars.yml` file, [re-run the playbook](../installing.md): `just install-service oauth2-proxy`.

This merely configures OAuth2-Proxy to handle the `/oauth2/` paths for Navidrome's domain.

Navidrome configuration adjustments are also necessary, so proceed to do those as well. Please see below for details.


### Navidrome configuration adjustments

Now that OAuth2-Proxy is ready and handling the `/oauth2/` paths on the domain Navidrome is running, we need to set up Traefik's [ForwardAuth](https://doc.traefik.io/traefik/middlewares/http/forwardauth/) middleware, so that all Navidrome requests would consult OAuth2-Proxy.

The configuration described below is based on the official [Configuring for use with the Traefik (v2) ForwardAuth middleware](https://oauth2-proxy.github.io/oauth2-proxy/configuration/overview#configuring-for-use-with-the-traefik-v2-forwardauth-middleware) documentation of OAuth2-Proxy and the [Externalized Authentication Quick Start](https://www.navidrome.org/docs/getting-started/extauth-quickstart/) guide.

> [!NOTE]
> This example assumes that you serve Navidrome under a dedicated hostname. If you are serving Navidrome under a path prefix, adjust the `PathPrefix` of the public rule to bypass authentication correctly.

```yml
########################################################################
#                                                                      #
# navidrome                                                            #
#                                                                      #
########################################################################

# Your other Navidrome configuration goes here.
# See the documentation in navidrome.md.

# Enable external authentication by setting ND_EXTAUTH_TRUSTEDSOURCES to include traefik's internal IP
# Specify the HTTP header containing the username (expects Remote-User by default)
navidrome_environment_variables_additional_variables: |
  ND_EXTAUTH_TRUSTEDSOURCES=172.16.0.0/12
  ND_EXTAUTH_USERHEADER=X-Auth-Request-Preferred-Username

# Block potentially malicious forwarding of the username header from external clients
navidrome_container_labels_traefik_additional_request_headers_custom:
  X-Auth-Request-Preferred-Username: ""

# Recollect middlewares from templates/labels.j2 for reuse
navidrome_container_labels_middlewares:
  - "{{ navidrome_container_labels_traefik_compression_middleware_name if navidrome_container_labels_traefik_compression_middleware_enabled }}"
  - "{{ navidrome_identifier ~ '-slashless-redirect' if navidrome_container_labels_traefik_path_prefix != '/' }}"
  - "{{ navidrome_identifier + '-add-request-headers' if navidrome_container_labels_traefik_additional_request_headers.keys() | length > 0 }}"
  - "{{ navidrome_identifier + '-add-response-headers' if navidrome_container_labels_traefik_additional_response_headers.keys() | length > 0 }}"

navidrome_container_labels_additional_labels_custom:
  # Create a middleware which catches "unauthenticated" errors and serves the OAuth2-Proxy sign in page.
  - traefik.http.middlewares.{{ navidrome_identifier }}-oauth-errors.errors.status=401-403
  - traefik.http.middlewares.{{ navidrome_identifier }}-oauth-errors.errors.service={{ oauth2_proxy_identifier }}
  - traefik.http.middlewares.{{ navidrome_identifier }}-oauth-errors.errors.query=/oauth2/sign_in?rd={url}

  # Create a middleware which passes each incoming request to OAuth2-Proxy,
  # so it can decide whether it should be let through (to Navidrome) or should be forwarded to the OAuth2-Proxy sign in page.
  - traefik.http.middlewares.{{ navidrome_identifier }}-oauth-auth.forwardAuth.address=http://{{ oauth2_proxy_identifier }}:{{ oauth2_proxy_container_process_http_port }}/oauth2/auth
  - traefik.http.middlewares.{{ navidrome_identifier }}-oauth-auth.forwardAuth.trustForwardHeader=true

  # Allow forwarding the HTTP header defined in ND_EXTAUTH_USERHEADER to identify users in Navidrome.
  # See more information about this in the comments for `oauth2_proxy_environment_variable_set_xauthrequest`.
  - traefik.http.middlewares.{{ navidrome_identifier }}-oauth-auth.forwardAuth.authResponseHeaders=X-Auth-Request-Preferred-Username

  # Inject the 2 middlewares defined above into the router of the Navidrome service
  - traefik.http.routers.{{ navidrome_identifier }}.middlewares={{ navidrome_container_labels_middlewares | select() | join(',') }},{{ navidrome_identifier }}-oauth-errors,{{ navidrome_identifier }}-oauth-auth

  # Authentication bypass for share and subsonic endpoints
  # Necessary if you want to stream music over the subsonic API and access shared content without authentication
  - traefik.http.routers.{{ navidrome_identifier }}-public.rule=Host(`{{ navidrome_hostname }}`) && (PathPrefix(`/share/`) || PathPrefix(`/rest/`))
  - traefik.http.routers.{{ navidrome_identifier }}-public.service={{ navidrome_identifier }}
  - traefik.http.routers.{{ navidrome_identifier }}-public.middlewares={{ navidrome_container_labels_middlewares | select() | join(',') }}
  - traefik.http.routers.{{ navidrome_identifier }}-public.entrypoints={{ navidrome_container_labels_traefik_entrypoints }}
  - traefik.http.routers.{{ navidrome_identifier }}-public.tls={{ navidrome_container_labels_traefik_tls | to_json }}
  - traefik.http.routers.{{ navidrome_identifier }}-public.tls.certResolver={{ navidrome_container_labels_traefik_tls_certResolver }}

########################################################################
#                                                                      #
# /navidrome                                                           #
#                                                                      #
########################################################################
```

After adding this to your `vars.yml` file, [re-run the playbook](../installing.md): `just install-service navidrome`.

Specific services (e.g. [Nextcloud](nextcloud.md)) provide Ansible variables (`nextcloud_container_labels_traefik_http_middlewares_custom`) for injecting new middlewares at a specific position (priority) in the list. Others services (Ansible roles) do not support this yet, which would prevent you from using them this way. Consider submitting an issue or better yet opening a PR to improve these services.

## Another sample configuration: Protecting specific prefixes of a website

Sometimes you want to protect only a specific endpoint of a website while leaving the rest of the site publicly available.

Below configuration demonstrates how to protect sensible endpoints (`/create`, `/admin` and `/dashboard`) of the [I hate money](ihatemoney.md) service behind Oauth2-Proxy, such that only authenticated users can create new projects and access the admin space (which needs further additional local credentials).

For this to work as described here, both OAuth2-Proxy and the protected service (e.g. [I hate money](ihatemoney.md)) need to run on the same machine.

### OAuth2-Proxy configuration

As in above example with Navidrome, we serve the OAuth2-Proxy authentication page under the `/oauth2/` prefix, adjusting `Host` and name the Traefik router in favor of "I hate money":

```yaml
oauth2_proxy_container_labels_additional_labels_custom:
  - traefik.http.routers.{{ oauth2_proxy_identifier }}-ihatemoney.rule=Host(`{{ ihatemoney_hostname }}`) && PathPrefix(`/oauth2/`)
  - traefik.http.routers.{{ oauth2_proxy_identifier }}-ihatemoney.service={{ oauth2_proxy_identifier }}
  - traefik.http.routers.{{ oauth2_proxy_identifier }}-ihatemoney.entrypoints={{ oauth2_proxy_container_labels_traefik_entrypoints }}
  - traefik.http.routers.{{ oauth2_proxy_identifier }}-ihatemoney.tls={{ oauth2_proxy_container_labels_traefik_tls }}
  - traefik.http.routers.{{ oauth2_proxy_identifier }}-ihatemoney.tls.certResolver={{ oauth2_proxy_container_labels_traefik_tls_certResolver }}
```

As usual, after changing your `vars.yml` file, [re-run the playbook](../installing.md): `just install-service oauth2-proxy`.

"I hate money" configuration adjustments are also necessary, so proceed below.

### "I hate money" configuration adjustments

Now that OAuth2-Proxy is ready and handling the `/oauth2/` paths on the domain "I hate money" is running on, we need to set up Traefik's [ForwardAuth](https://doc.traefik.io/traefik/middlewares/http/forwardauth/) middleware, so that all requests to the protected endpoints would need authorisation from OAuth2-Proxy.

The configuration described below is based on the official [Configuring for use with the Traefik (v2) ForwardAuth middleware](https://oauth2-proxy.github.io/oauth2-proxy/configuration/overview#configuring-for-use-with-the-traefik-v2-forwardauth-middleware) documentation of OAuth2-Proxy.

```yml
########################################################################
#                                                                      #
# ihatemoney                                                           #
#                                                                      #
########################################################################

# Your other Ihatemoney configuration goes here.
# See the documentation in ihatemoney.md.

# Enable public project creation to resecure the endpoint with oauth2-proxy
ihatemoney_public_project_creation: true

# Recollect middlewares from templates/labels.j2 for reuse
ihatemoney_container_labels_middlewares:
  - "{{ ihatemoney_identifier ~ '-add-request-headers' if ihatemoney_container_labels_traefik_additional_request_headers.keys() | length > 0 }}"
  - "{{ ihatemoney_identifier ~ '-add-response-headers' if ihatemoney_container_labels_traefik_additional_response_headers.keys() | length > 0 }}"

ihatemoney_container_labels_additional_labels:
  # Create a middleware which catches "unauthenticated" errors and serves the OAuth2-Proxy sign in page.
  - traefik.http.middlewares.{{ ihatemoney_identifier }}-oauth-errors.errors.status=401-403
  - traefik.http.middlewares.{{ ihatemoney_identifier }}-oauth-errors.errors.service={{ oauth2_proxy_identifier }}
  - traefik.http.middlewares.{{ ihatemoney_identifier }}-oauth-errors.errors.query=/oauth2/sign_in?rd={url}

  # Create a middleware which passes incoming requests to OAuth2-Proxy,
  # so it can decide whether it should be let through (to Ihatemoney) or should be forwarded to the OAuth2-Proxy sign in page.
  - traefik.http.middlewares.{{ ihatemoney_identifier }}-oauth-auth.forwardAuth.address=http://{{ oauth2_proxy_identifier }}:{{ oauth2_proxy_container_process_http_port }}/oauth2/auth
  - traefik.http.middlewares.{{ ihatemoney_identifier }}-oauth-auth.forwardAuth.trustForwardHeader=true

  # Create a router for /create, /admin and /dashboard endpoints to secure with oauth2-proxy
  - traefik.http.routers.{{ ihatemoney_identifier }}-private.rule={{ ihatemoney_container_labels_traefik_rule }} && (PathPrefix(`/create`) || PathPrefix(`/admin`) || PathPrefix(`/dashboard`))
  - traefik.http.routers.{{ ihatemoney_identifier }}-private.service={{ ihatemoney_identifier }}
  # Inject the forwardauth middlewares defined above
  - traefik.http.routers.{{ ihatemoney_identifier }}-private.middlewares={{ ihatemoney_container_labels_middlewares | select() | join(',') }},{{ ihatemoney_identifier }}-oauth-errors,{{ ihatemoney_identifier }}-oauth-auth
  - traefik.http.routers.{{ ihatemoney_identifier }}-private.entrypoints={{ ihatemoney_container_labels_traefik_entrypoints }}
  - traefik.http.routers.{{ ihatemoney_identifier }}-private.tls={{ ihatemoney_container_labels_traefik_tls | to_json }}
  - traefik.http.routers.{{ ihatemoney_identifier }}-private.tls.certResolver={{ ihatemoney_container_labels_traefik_tls_certResolver }}

########################################################################
#                                                                      #
# /ihatemoney                                                          #
#                                                                      #
########################################################################
```

After adding this to your `vars.yml` file, [re-run the playbook](../installing.md): `just install-service ihatemoney`.

## Further reading

If you'd like to do something more advanced, the [`ansible-role-oauth2-proxy` Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-oauth2-proxy) is very configurable and should let you do what you need.

Take a look at [its `default/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-oauth2-proxy/blob/main/defaults/main.yml) for available Ansible variables you can use in your own `vars.yml` configuration file.

## Related services

- [authentik](authentik.md) — An open-source Identity Provider (IdP) focused on flexibility and versatility.
- [Keycloak](keycloak.md) — An open source identity and access management solution
- [Authelia](authelia.md) — An open-source authentication and authorization server that can work as a companion to [common reverse proxies](https://www.authelia.com/overview/prologue/supported-proxies/) (like [Traefik](traefik.md) frequently used by this playbook)
- [Pocket ID](pocket-id.md) — Simple OIDC provider for passkey-only authentication
