# Hubsite

[Hubsite](https://github.com/moan0s/hubsite) is will provide you with a simple, static site that shows an overview of the available services.

You can use the following variables to enable & control your hubsite:

```yaml
########################################################################
#                                                                      #
# hubsite                                                              #
#                                                                      #
########################################################################

hubsite_enabled: true

hubsite_hostname: mash.example.com

hubsite_title: "My services"
hubsite_subtitle: "Just click on a service to use it"

# Use the `hubsite_service_list_additional` variable to add services that are not provided by this playbook
# hubsite_service_list_additional: |
#   {{
#     ([{'name': 'My blog', 'url': 'https://example.com', 'logo_location': '', 'description': 'A link to a blog not hosted by this playbook', 'priority': 1000 }])
#   }}

# If you want to explicitly control which services you want to show on this page you can overwrite
# hubsite_service_list_auto: |
#   {{
#     ([{'name': 'Miniflux', 'url': hubsite_service_miniflux_url, 'logo_location': '{{ role_path }}/assets/miniflux.png', 'description': 'An opinionated feed reader', 'priority': hubsite_service_miniflux_priority}] if hubsite_service_miniflux_enabled else [])
#     +
#     ([{'name': 'Uptime Kuma', 'url': hubsite_service_uptime_kuma_url, 'logo_location': '{{ role_path }}/assets/uptime-kuma.png', 'description': 'Check the status of the services', 'priority': hubsite_service_uptime_kuma_priority}] if hubsite_service_uptime_kuma_enabled else [])
#   }}
########################################################################
#                                                                      #
# /hubsite                                                             #
#                                                                      #
########################################################################
```

You can SSO-protect this website with the help of [Authelia](authelia.md) or [OAuth2-Proxy](oauth2-proxy.md) (connected to any OIDC provider).

>[!NOTE]
> You might be also interested in setting up [Homarr](homarr.md), a customizable dashboard for managing your favorite applications and services.
