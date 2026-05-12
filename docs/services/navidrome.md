<!--
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 Thomas Miceli
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 Timofej Luitle

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Navidrome

The playbook can install and configure [Navidrome](https://www.navidrome.org/) for you.

Navidrome is a [Subsonic-API](http://www.subsonic.org/pages/api.jsp) compatible music server.

See the project's [documentation](https://www.navidrome.org/docs/) to learn what Navidrome does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# navidrome                                                            #
#                                                                      #
########################################################################

navidrome_enabled: true

navidrome_hostname: mash.example.com
navidrome_path_prefix: /navidrome

########################################################################
#                                                                      #
# /navidrome                                                           #
#                                                                      #
########################################################################
```

### File management

Since Navidrome is just a music player, you would need to prepare music files to be played with it.

If your server runs a file management service along with Navidrome such as [File Browser](filebrowser.md), [FileBrowser Quantum](filebrowser-quantum.md), and [Syncthing](syncthing.md), it is possible to upload files to the server or synchronize your music directory with it to make them accessible on Navidrome.

#### Preparing directories

First, let's create a directory to be shared with the services. You can make use of the [aux](auxiliary.md) role by adding the following configuration to your `vars.yml` file. We create two directories here; the directory to be shared among Navidrome and other services, and its parent directory. If you are willing to have other services share directories, you can add another path by adding one to the list:

```yaml
########################################################################
#                                                                      #
# aux                                                                  #
#                                                                      #
########################################################################

aux_directory_definitions:
  - dest: "{{ mash_playbook_base_path }}/storage"
  - dest: "{{ mash_playbook_base_path }}/storage/music"
# - dest: another shared directory path …

########################################################################
#                                                                      #
# /aux                                                                 #
#                                                                      #
########################################################################
```

#### Mounting the directory into the Navidrome container

Next, mount the `{{ mash_playbook_base_path }}/storage/music` directory into the Navidrome container. By default, Navidrome will look at the `/music` directory for music files, controlled by the `navidrome_environment_variable_nd_musicfolder` variable.

>[!NOTE]
> The directory may be mounted as read-only to prevent data inside the directory from accidentally being deleted or modified by Navidrome.

```yaml
########################################################################
#                                                                      #
# navidrome                                                            #
#                                                                      #
########################################################################

# Other Navidrome configuration …

navidrome_container_additional_volumes_custom:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/music"
    dst: "{{ navidrome_environment_variable_nd_musicfolder }}"
    options: readonly

########################################################################
#                                                                      #
# /navidrome                                                           #
#                                                                      #
########################################################################
```

#### Sharing the directory with other containers

You can then mount this `{{ mash_playbook_base_path }}/storage/music` directory on other service's container.

For example, adding the configuration below will let you to access to `/music` directory on the File Browser's UI, so that you can upload files to the server directly and make them accessible on Navidrome:

```yaml
########################################################################
#                                                                      #
# filebrowser                                                          #
#                                                                      #
########################################################################

# Other File Browser configuration …

filebrowser_container_additional_volumes_custom:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/music"
    dst: "/srv/music"

########################################################################
#                                                                      #
# /filebrowser                                                         #
#                                                                      #
########################################################################
```

Adding the configuration below makes it possible for the Syncthing service to synchronize the directory with other computers:

```yaml
########################################################################
#                                                                      #
# syncthing                                                            #
#                                                                      #
########################################################################

# Other Syncthing configuration …

syncthing_container_additional_volumes_custom:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/music"
    dst: /music

########################################################################
#                                                                      #
# /syncthing                                                           #
#                                                                      #
########################################################################
```

### Authenticating with an identity provider via OAuth2-Proxy

Although Navidrome currently does not offer a native OAuth2 client configuration, [external authentication](https://www.navidrome.org/docs/usage/integration/authentication/) via a trusted reverse-proxy is supported.

This will substitute the local sign-in flow and delegate authentication to a reverse-proxy, which will catch requests and pass usernames to Navidrome via HTML headers after authentication. Navidrome will trust configured proxies unconditionally, create local users and subsequently grant access to existent accounts based on the username header. The first user to login will receive admin privileges, subsequent first logins will be created as non-admin user.

The [OAuth2-Proxy](./oauth2-proxy.md) role supported by this playbook offers a reverse-proxy service capable to authenticate against Navidrome via OAuth2/OIDC and shall serve as such in the sample configuration provided below.

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

> [!CAUTION]
> As we use the less invasive 2. mode documented in [oauth2-proxy.md](./oauth2-proxy.md), Navidrome will see requests as coming from Traefik. Accordingly we tell Navidrome to trust the username header coming from our Traefik reverse-proxy.
>
> But Navidrome will automatically create new users at first login passed on by the username header if the source is trusted.
>
> Therefore we need to strip this header from all external requests in order to avoid risking unauthorized user creation:
> ```yml
> navidrome_container_labels_traefik_additional_request_headers_custom:
>   X-Auth-Request-Preferred-Username: ""
> ```
>
> Consider the more invasive 1. mode of OAuth2-Proxy if you want to exclude Traefik from your trusted IPs altogether and only accept authorization requests from OAuth2-Proxy directly.

> [!NOTE]
> Currently Navidrome user auto-creation from external sources is tightly coupled to serving the webpage index and may fail when the webpage is loaded from cache upon first login, e.g. when changing accounts within the same browser.

Configure OAuth2-Proxy as follows (e.g. with Keycloak):

```yml
########################################################################
#                                                                      #
# oauth2_proxy                                                         #
#                                                                      #
########################################################################

oauth2_proxy_enabled: true

oauth2_proxy_environment_variable_provider: keycloak-oidc
oauth2_proxy_environment_variable_provider_display_name: Keycloak

# Authorize OAuth2-Proxy with your OIDC credentials
oauth2_proxy_environment_variable_client_id: ""
oauth2_proxy_environment_variable_client_secret: ""
oauth2_proxy_environment_variable_oidc_issuer_url: https://keycloak.example.com/realms/my-realm
oauth2_proxy_environment_variable_redirect_url: "https://{{ navidrome_hostname }}/oauth2/callback"

oauth2_proxy_environment_variable_code_challenge_method: S256

# Generate this with: `python -c 'import os,base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())'`
oauth2_proxy_environment_variable_cookie_secret: ""

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

The first user to login via OAuth2-Proxy will become an administrator, subsequent logins will be created as non-admin user.

### Integrating with Prometheus (optional)

Navidrome can natively expose metrics to [Prometheus](prometheus.md).

#### Expose metrics internally

If Navidrome and Prometheus do not share a network (like Traefik), you can connect the Navidrome container network to Prometheus by adding the following configuration to your `vars.yml` file:

```yaml
prometheus_container_additional_networks_custom:
  - "{{ navidrome_container_network }}"
```

#### Expose metrics publicly

If Navidrome metrics are not scraped from a local Prometheus instance, you can expose the metrics publicly so that a remote instance can fetch them.

When exposing metrics publicly, you should consider to set up [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) **or anyone would be able to read your metrics**.

To expose the metrics publicly, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
mash_playbook_metrics_exposure_enabled: true
mash_playbook_metrics_exposure_hostname: mash.example.com
```

It will expose the metrics at `https://mash.example.com/metrics/mash-navidrome`.

To enable the HTTP Basic authentication, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
navidrome_container_labels_traefik_metrics_middleware_basic_auth_enabled: true

# See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details.
navidrome_container_labels_traefik_metrics_middleware_basic_auth_users: ""
```

## Usage

After running the command for installation, the Navidrome instance becomes available at the URL specified with `navidrome_hostname` and `navidrome_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/navidrome`.

To get started, open the URL with a web browser to create an administrator account. You can create additional users (admin-privileged or not) after that.

You can also connect various Subsonic-API-compatible [apps](https://www.navidrome.org/docs/overview/#apps) (desktop, web, mobile) to your Navidrome instance.

## Related services

- [Feishin](feishin.md) — Music player for Navidrome, Jellyfin, Funkwhale, etc.
