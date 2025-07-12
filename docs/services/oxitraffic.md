# OxiTraffic

[OxiTraffic](https://codeberg.org/mo8it/oxitraffic) is a self-hosted, simple and privacy respecting website traffic tracker, that this playbook can install, powered by the [mother-of-all-self-hosting/ansible-role-oxitraffic](https://github.com/mother-of-all-self-hosting/ansible-role-oxitraffic) Ansible role.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# oxitraffic                                                           #
#                                                                      #
########################################################################

oxitraffic_enabled: true
oxitraffic_hostname: traffic.example.org
oxitraffic_tracked_origin: https://example.org

########################################################################
#                                                                      #
# /oxitraffic                                                          #
#                                                                      #
########################################################################
```

You must include the counting script on the `oxitraffic_tracked_origin` by adding the following to you website
```html
<script type="module" src="https://YOUR-OXITRAFFIC_HOSTNAME/count.js"></script>
```

# Notes on Troubleshooting

Internal OxiTraffic errors will not be logged to `stdout` and will therefore not be part of `journalctl -fu mash-oxitraffic`. You should check the log file that is created by OxiTraffic with `tail -f logs/oxitraffic`.

# Data Protection

*This is not legal advice, talk to a lawyer!*

OxiTraffic does not collect IP Addresses, Browser Information etc.. Each visitor is assigned a anonymous ID upon visiting the site. This will only be used to store information on how long the visitor spends on this site. No cookies are set.
