# Stirling PDF

Stirling PDF is an online PDF converter and editor with many functionalities. Visit the [official website](https://www.stirlingpdf.com) or [demo](https://stirlingpdf.io) to learn more.

## Dependencies

- a [Traefik](traefik.md) reverse-proxy server (optional)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# stirling-pdf                                                         #
#                                                                      #
########################################################################

stirling_pdf_enabled: true

stirling_pdf_hostname: mash.example.com

# The path at which stirling_pdf is served.
# This value must either be `/` or not end with a slash (e.g. `/pdf`).
stirling_pdf_path_prefix: /stirlingpdf

# Set to true to download calibre onto stirling-pdf enabling pdf to/from book and advanced html conversion | default false
stirling_pdf_install_calibre: false

########################################################################
#                                                                      #
# /stirling-pdf                                                        #
#                                                                      #
########################################################################
```

### Optional Configuration

You can decide if you want to configure via environment variables or a configuration file. Environment variables outrank the configuration file.

To set addition environment variables use `stirling_pdf_environment_variables_extensions` in your `vars.yml` file.
To use the configuration file, use `stirling_pdf_extra_config` in your `vars.yml` file.

```yaml
stirling_pdf_extra_config: |
  	system:
    	defaultLocale: 'de-DE'

# OR

stirling_pdf_environment_variables_extensions: |
	SYSTEM_DEFAULTLOCALE=de-DE
```

Find all possible arguments in the [official documentation](https://docs.stirlingpdf.com/Advanced%20Configuration/How%20to%20add%20configurations).

All possible variables to configure the ansible-role can be found in its [defaults/main.yml](https://github.com/Bergruebe/ansible-role-stirling-pdf/blob/main/defaults/main.yml) file.
