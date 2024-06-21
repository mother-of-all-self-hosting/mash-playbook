# Matterbridge

[Matterbridge](https://github.com/42wim/matterbridge)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# matterbridge                                                         #
#                                                                      #
########################################################################

matterbridge_enabled: true
matterbridge_toml_src_path: "{{ playbook_dir }}/path/to/your/matterbridge.toml.j2"
########################################################################
#                                                                      #
# /matterbridge                                                        #
#                                                                      #
########################################################################
```
