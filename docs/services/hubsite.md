# Hubsite

[Hubsite](https://github.com/moan0s/hubsite) is will provide you with a simple, static site that shows an overview of the available services.

You can use the following variables to enable & control your hubsite:

```yaml
hubsite_enabled: true
hubsite_hostname: "example.com"
hubsite_title: "My services"
hubsite_subtitle: "Just click on a service to use it"
# Use the `hubsite_service_list_additional` variable to add services that are not provided by this playbook
# hubsite_service_list: |
#   {{
#     ([{'name': 'My blog', 'logo_location': '', 'description': 'A link to a blog not hosted by this playbook'}])
#   }}

# If you want to explicitly control which services you want to show on this page you can overwrite 
# hubsite_service_list_auto: |
#   {{
#     ([{'name': 'Miniflux', 'logo_location': '{{ role_path }}/assets/miniflux.png', 'description': 'An opinionated feed reader '}])
#     +
#     ([{'name': 'Uptime Kuma', 'logo_location': '{{ role_path }}/assets/uptime-kuma.png', 'description': 'Check if the status of services'}])
#   }}
```
