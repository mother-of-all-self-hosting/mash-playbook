# Prometheus SSH Exporter

This playbook can configure [Prometheus SSH Exporter](https://github.com/treydock/ssh_exporter).

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# prometheus-ssh-exporter                                              #
#                                                                      #
########################################################################

prometheus_ssh_exporter_enabled: true

# if you want to export ssh's probe endpoint, uncomment and adjust the following vars

# prometheus_ssh_exporter_hostname: mash.example.com
# prometheus_ssh_exporter_path_prefix: /metrics/ssh-exporter
# prometheus_ssh_exporter_basicauth_user: your_username
# prometheus_ssh_exporter_basicauth_password: your password

########################################################################
#                                                                      #
# /prometheus-ssh-exporter                                             #
#                                                                      #
########################################################################
```

## Usage

After you've installed the ssh exporter, your ssh prober will be available on `mash.example.com/metrics/ssh-exporter` with the basic auth credentials you've configured if hostname and path prefix where provided
