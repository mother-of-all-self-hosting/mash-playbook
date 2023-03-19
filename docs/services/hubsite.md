# Hubsite

Hubsite is will provide you with a simple, static site that shows an overview of the available services.

You can use the following variables to enable & control your hubsite:

```yaml
hubsite_enabled: true
hubsite_domain: "example.com"
hubsite_title: "My services"
hubsite_subtitle: "Just click on a service to use it"
# Use the `hubsite_service_list` variable to only enable services you want to show on this page
# hubsite_service_list: |
#   {{
#     ([{'name': 'Miniflux', 'logo_location': '{{ role_path }}/assets/miniflux.png', 'description': 'An opinionated feed reader '}] if miniflux_enabled else [])
#     +
#     ([{'name': 'Uptime Kuma', 'logo_location': '{{ role_path }}/assets/uptime-kuma.png', 'description': 'Check if the status of services'}] if uptime_kuma_enabled else [])
#   }}
```
