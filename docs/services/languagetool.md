<!--
SPDX-FileCopyrightText: 2024 Tiz
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# LanguageTool

The playbook can install and configure [LanguageTool](https://languagetool.org/) for you.

LanguageTool is an open source online grammar, style and spell checker.

See the project's [documentation](https://languagetool.org/dev) to learn what LanguageTool does and why it might be useful to you.

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

You can remove the `languagetool_path_prefix` variable definition, to make it default to `/`, so that the service is served at `https://mash.example.com/`.

### Enable n-gram data (optional)

LanguageTool can make use of large n-gram data sets to detect errors with words that are often confused, like "their" and "there". See [*Finding errors using n-gram data*](https://dev.languagetool.org/finding-errors-using-n-gram-data) to learn more.

>[!NOTE]
> The n-gram data set is huge and thus not enabled by default.

To make use of it with your own LanguageTool server, you may enable n-gram data and choose which languages' n-gram data to download by adding the following configuration to your `vars.yml` file:

```yaml
languagetool_ngrams_enabled: true

languagetool_ngrams_langs_enabled: ['fr', 'en']
```

Check the `languagetool_ngrams_langs` variable on [`default/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-languagetool/blob/main/defaults/main.yml) for a list of languages for which the Ansible role supports downloading n-gram data.

Additional languages which are not defined on the role may be available. You can redefine `languagetool_ngrams_langs` to have the role download URL for those languages. [PRs to the role](https://github.com/mother-of-all-self-hosting/ansible-role-languagetool) are welcome!

## Usage

After installation, your LanguageTool instance becomes available at the URL specified with `languagetool_hostname`.

You can test the instance by making a request to [LanguageTool's HTTP API](https://dev.languagetool.org/public-http-api) by running a *curl* command as follows: `curl --data "language=en-US&text=a simple test" https://mash.example.com/languagetool/v2/check`

There are [software that support LanguageTool as an add-on](https://dev.languagetool.org/software-that-supports-languagetool-as-a-plug-in-or-add-on). To use them with your instance, set `https://mash.example.com/languagetool/v2` to the URL (assuming you've installed at the `/languagetool` path prefix).
