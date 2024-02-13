# LanguageTool

[LanguageTool](https://languagetool.org/) is an open source online grammar, style and spell checker. Installing it is powered by the [etke.cc/roles/languagetool](https://gitlab.com/etke.cc/roles/languagetool) Ansible role and [Erikvl87/docker-languagetool](https://github.com/Erikvl87/docker-languagetool) docker image.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) - a reverse-proxy server 


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# LanguageTool                                                         #
#                                                                      #
########################################################################

languagetool_enabled: true

languagetool_hostname: mash.example.com
languagetool_path_prefix: /languagetool

########################################################################
#                                                                      #
# /LanguageTool                                                        #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/languagetool`.

You can remove the `languagetool_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

### Downloading models

By default, no language model are present. Enable `languagetool_ngrams_enabled` and configure `languagetool_ngrams_langs_enabled` so that the service downloads models.

```yaml
languagetool_ngrams_enabled: true
languagetool_ngrams_langs_enabled: ['fr', 'en']
```

## Usage

After [installing](../installing.md), you can test your instance by making requests to [LanguageTool's HTTP API](https://dev.languagetool.org/public-http-api).

An example HTTP request can be made with [curl](https://curl.se/): `curl --data "language=en-US&text=a simple test" https://mash.example.com/languagetool/v2/check`

See the list of [software that supports LanguageTool as an add-on](https://dev.languagetool.org/software-that-supports-languagetool-as-a-plug-in-or-add-on) and set `https://mash.example.com/languagetool/v2` as the LanguageTool server (assuming you've installed at the `/languagetool` path prefix).
