# Changedetection.io

[Changedetection.io](https://github.com/dgtlmoon/changedetection.io) is a simple **website change detection and restock monitoring** solution.


## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# Changedetection.io                                                   #
#                                                                      #
########################################################################

changedetection_enabled: true

changedetection_hostname: mash.example.com

changedetection_path_prefix: /changedetection

########################################################################
#                                                                      #
# /Changedetection.io                                                  #
#                                                                      #
########################################################################
```

### Playwright webdriver

Some advanced options like using javascript or using the Visual Selector tool use an additional playwright webdriver. To enable this driver, add the following **additional**  configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
changedetection_playwright_driver_enabled: true
```


### URL

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/changedetection`.

You can remove the `changedetection_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

## Usage

After installation, you can go to your given URL and start setting up Changedetection.io
