# LanguageTool

[LanguageTool](https://languagetool.org/) is an open source online grammar, style and spell checker. Installing it is powered by the [etke.cc/roles/languagetool](https://gitlab.com/etke.cc/roles/languagetool) Ansible role and [Erikvl87/docker-languagetool](https://github.com/Erikvl87/docker-languagetool) docker image.

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) — a reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# languagetool                                                         #
#                                                                      #
########################################################################

languagetool_enabled: true

languagetool_hostname: mash.example.com
languagetool_path_prefix: /languagetool

########################################################################
#                                                                      #
# /languagetool                                                        #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/languagetool`.

You can remove the `languagetool_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

### Enabling n-gram data

LanguageTool can make use of large n-gram data sets to detect errors with words that are often confused, like *their* and *there*.
Learn more in [Finding errors using n-gram data](https://dev.languagetool.org/finding-errors-using-n-gram-data).

The **n-gram data set is huge and thus not part of the LanguageTool installation**. To make use of it with your own LanguageTool server, you may enable n-gram data and choose which languages to download n-gram data for.

For a list of languages for which the Ansible role supports downloading n-gram data, consult the `languagetool_ngrams_langs` variable in [the `default/main.yml` file](https://gitlab.com/etke.cc/roles/languagetool/-/blob/main/defaults/main.yml). Additional languages may be available. If the role doesn't have a download URL for them, consider redefining `languagetool_ngrams_langs` yourself with your own language-code to download URL mapping or submit a PR to the [languagetool Ansible role](https://gitlab.com/etke.cc/roles/languagetool).

```yaml
languagetool_ngrams_enabled: true

# See `languagetool_ngrams_langs` for a list of language-codes
# that the Ansible role supports.
languagetool_ngrams_langs_enabled: ['fr', 'en']
```

## Usage

After [installing](../installing.md), you can test your instance by making requests to [LanguageTool's HTTP API](https://dev.languagetool.org/public-http-api).

An example HTTP request can be made with [curl](https://curl.se/): `curl --data "language=en-US&text=a simple test" https://mash.example.com/languagetool/v2/check`

See the list of [software that supports LanguageTool as an add-on](https://dev.languagetool.org/software-that-supports-languagetool-as-a-plug-in-or-add-on) and set `https://mash.example.com/languagetool/v2` as the LanguageTool server (assuming you've installed at the `/languagetool` path prefix).
