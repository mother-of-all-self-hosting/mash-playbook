# Matterbridge

[Matterbridge](https://github.com/42wim/matterbridge)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

The configuration itself is documented [here](https://github.com/42wim/matterbridge/wiki/How-to-create-your-config)

```yaml
########################################################################
#                                                                      #
# matterbridge                                                         #
#                                                                      #
########################################################################

matterbridge_enabled: true
matterbridge_configuration_toml:
  accounts:
    - protocol: matrix
      identifier: someidentifier
      configuration:
        Server: "https://matrix.example.com"
        Login: "{{ matterbridge_matrix_user }}"
        Password: "{{ matterbridge_matrix_password }}"
        RemoteNickFormat: "{NICK}: "
        NoHomeServerSuffix: "false"

  gateways:
    - name: "A Gateway"
      enable: "true"
      channels:

        - type: inout
          account: matrix.someidentifier
          channel: "!roomA:matrix.example.com"

        - type: inout
          account: matrix.freifunk
          channel: "!roomB:matrix.example.com"

########################################################################
#                                                                      #
# /matterbridge                                                        #
#                                                                      #
########################################################################
```
