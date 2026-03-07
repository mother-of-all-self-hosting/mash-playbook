<!--
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2026 Timofej Luitle

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Navidrome

[Navidrome](https://www.navidrome.org/) is a [Subsonic-API](http://www.subsonic.org/pages/api.jsp) compatible music server.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


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

# By default, Navidrome will look at the /music directory for music files,
# controlled by the `navidrome_environment_variable_nd_musicfolder` variable.
#
# You'd need to mount some music directory into the Navidrome container, like shown below.
# The "Syncthing integration" section below may be relevant.
# navidrome_container_additional_volumes:
#   - type: bind
#     src: /on-host/path/to/music
#     dst: /music
#     options: readonly

########################################################################
#                                                                      #
# /navidrome                                                           #
#                                                                      #
########################################################################
```

### Syncthing integration

If you've got a [Syncthing](syncthing.md) service running, you can use it to synchronize your music directory onto the server and then mount it as read-only into the Navidrome container.

We recommend that you make use of the [aux](auxiliary.md) role to create some shared directory like this:

```yaml
########################################################################
#                                                                      #
# aux                                                                  #
#                                                                      #
########################################################################

aux_directory_definitions:
  - dest: "{{ mash_playbook_base_path }}/storage"
  - dest: "{{ mash_playbook_base_path }}/storage/music"

########################################################################
#                                                                      #
# /aux                                                                 #
#                                                                      #
########################################################################
```

You can then mount this `{{ mash_playbook_base_path }}/storage/music` directory into the Syncthing container and synchronize it with some other computer:

```yaml
########################################################################
#                                                                      #
# syncthing                                                            #
#                                                                      #
########################################################################

# Other Syncthing configuration..

syncthing_container_additional_volumes:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/music"
    dst: /music

########################################################################
#                                                                      #
# /syncthing                                                           #
#                                                                      #
########################################################################
```

Finally, mount the `{{ mash_playbook_base_path }}/storage/music` directory into the Navidrome container as read-only:

```yaml
########################################################################
#                                                                      #
# navidrome                                                            #
#                                                                      #
########################################################################

# Other Navidrome configuration..

navidrome_container_additional_volumes:
  - type: bind
    src: "{{ mash_playbook_base_path }}/storage/music"
    dst: /music
    options: readonly

########################################################################
#                                                                      #
# /navidrome                                                           #
#                                                                      #
########################################################################
```

## Securing Navidrome behind OAuth2-Proxy

Navidrome currently only supports [external authentication](https://www.navidrome.org/docs/usage/integration/authentication/) via a trusted reverse-proxy.

It is possible to configure the OAuth2-Proxy role to protect Navidrome via OAuth2/OIDC.

Below you will find a sample configutaration that works with the Nextcloud OIDC provider.

```yml
########################################################################
#                                                                      #
# navidrome                                                            #
#                                                                      #
########################################################################

navidrome_enabled: true
navidrome_hostname: navidrome.hostname

navidrome_oidc_client_enabled: true
navidrome_oidc_redirect_uris: "https://{{ navidrome_hostname }}/oauth2/callback"
navidrome_oidc_client_id: "" 	  # pwgen -s 64 1
navidrome_oidc_client_secret: ""  # pwgen -s 64 1

navidrome_environment_variables_additional_variables: |
  ND_EXTAUTH_TRUSTEDSOURCES=172.16.0.0/12
  ND_EXTAUTH_USERHEADER=X-Auth-Request-Preferred-Username

navidrome_container_labels_middlewares:
  - "{{ navidrome_container_labels_traefik_compression_middleware_name if navidrome_container_labels_traefik_compression_middleware_enabled }}"
  - "{{ navidrome_identifier ~ '-slashless-redirect' if navidrome_container_labels_traefik_path_prefix != '/' }}"
  - "{{ navidrome_identifier + '-add-request-headers' if navidrome_container_labels_traefik_additional_request_headers.keys() | length > 0 }}"
  - "{{ navidrome_identifier + '-add-response-headers' if navidrome_container_labels_traefik_additional_response_headers.keys() | length > 0 }}"

navidrome_container_labels_additional_labels_custom:
  # Create a middleware which catches "unauthenticated" errors and serves the OAuth-Proxy sign in page.
  - traefik.http.middlewares.{{ navidrome_identifier }}-oauth-errors.errors.status=401-403
  - traefik.http.middlewares.{{ navidrome_identifier }}-oauth-errors.errors.service={{ oauth2_proxy_identifier }}
  - traefik.http.middlewares.{{ navidrome_identifier }}-oauth-errors.errors.query=/oauth2/sign_in?rd={url}

  # Create a middleware which passes each incoming request to OAuth2-Proxy,
  # so it can decide whether it should be let through (to Hubsite) or should blocked (serving the OAuth2-Proxy sign in page).
  - traefik.http.middlewares.{{ navidrome_identifier }}-oauth-auth.forwardAuth.address=http://{{ oauth2_proxy_identifier }}:{{ oauth2_proxy_container_process_http_port }}/oauth2/auth
  - traefik.http.middlewares.{{ navidrome_identifier }}-oauth-auth.forwardAuth.trustForwardHeader=true

  # Let the HTTP header defined in ND_EXTAUTH_USERHEADER get passed from OAuth2-Proxy to Navidrome.
  # See more information about this in the comments for `oauth2_proxy_environment_variable_set_xauthrequest`.
  - traefik.http.middlewares.{{ navidrome_identifier }}-oauth-auth.forwardAuth.authResponseHeaders=X-Auth-Request-Preferred-Username

  # Inject the 2 middlewares defined above into the router of the Navidrome service
  - traefik.http.routers.{{ navidrome_identifier }}.middlewares={{ navidrome_container_labels_middlewares | select() | join(',') }},{{ navidrome_identifier }}-oauth-errors,{{ navidrome_identifier }}-oauth-auth

  # Authentication bypass for share and subsonic endpoints
  # This is necessary if you want to stream music over the subsonic API and let unauthenticated users access the music that you want to share
  - traefik.http.routers.{{ navidrome_identifier }}-public.rule={{ navidrome_container_labels_traefik_rule }} && (PathPrefix(`/share/`) || PathPrefix(`/rest/`))
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

Then, configure OAuth2-Proxy:

```yml
########################################################################
#                                                                      #
# oauth2_proxy                                                         #
#                                                                      #
########################################################################

oauth2_proxy_enabled: true

oauth2_proxy_environment_variable_provider: oidc
oauth2_proxy_environment_variable_provider_display_name: "Nextcloud"

oauth2_proxy_environment_variable_oidc_issuer_url: "https://{{ nextcloud_hostname }}"
oauth2_proxy_environment_variable_redirect_url: "{{ navidrome_oidc_redirect_uris }}"
oauth2_proxy_environment_variable_client_id: "{{ navidrome_oidc_client_id }}"
oauth2_proxy_environment_variable_client_secret: "{{ navidrome_oidc_client_secret }}"

oauth2_proxy_environment_variable_code_challenge_method: S256

# Generate this with: `python -c 'import os,base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())'`
oauth2_proxy_environment_variable_cookie_secret: ""

oauth2_proxy_environment_variables_additional_variables: |
  OAUTH2_PROXY_WHITELIST_DOMAINS=.oauthprovider.hostname:*
  
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

## Usage

After running the command for installation, the Navidrome instance becomes available at the URL specified with `navidrome_hostname` and `navidrome_path_prefix`. With the configuration above, the service is hosted at `https://mash.example.com/navidrome`.

To get started, open the URL with a web browser to create an administrator account. You can create additional users (admin-privileged or not) after that.

You can also connect various Subsonic-API-compatible [apps](https://www.navidrome.org/docs/overview/#apps) (desktop, web, mobile) to your Navidrome instance.


## Recommended other services

- [Syncthing](syncthing.md) — a continuous file synchronization program which synchronizes files between two or more computers in real time. See [Syncthing integration](#syncthing-integration)
