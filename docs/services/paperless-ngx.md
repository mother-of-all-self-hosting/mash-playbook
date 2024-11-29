# Paperless-ngx

[Paperless-ngx](https://paperless-ngx.com) s a community-supported open-source document management system that transforms your physical documents into a searchable online archive so you can keep, well, less paper. MASH can install paperless-ngx with the [`mother-of-all-self-hosting/ansible-role-paperless`](https://github.com/mother-of-all-self-hosting/ansible-role-paperless) ansible role.

**Warning** Paperless-ngx currently [does not support](https://github.com/paperless-ngx/paperless-ngx/issues/6352) running the container rootless, therefore the role has not the usual security features of other services provided by this playbook. This put your system more at higher risk as vulnerabilities can have a higher impact.

## Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Valkey](valkey.md) data-store, installation details [below](#valkey)
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# paperless                                                            #
#                                                                      #
########################################################################

paperless_enabled: true

paperless_hostname: paperless.example.org

# Set the following variables to create an initial admin user
# It will not re-create an admin user, it will not change a password if the user is already created
# paperless_admin_user: USERNAME
# paperless_admin_password: SECURE_PASSWORD

# Valkey configuration, as described below

########################################################################
#                                                                      #
# /paperless                                                           #
#                                                                      #
########################################################################
```

### Valkey

As described on the [Valkey](valkey.md) documentation page, if you're hosting additional services which require KeyDB on the same server, you'd better go for installing a separate Valkey instance for each service. See [Creating a Valkey instance dedicated to paperless-ngx](#creating-a-valkey-instance-dedicated-to-paperless-ngx).

If you're only running paperless-ngx on this server and don't need to use KeyDB for anything else, you can [use a single Valkey instance](#using-the-shared-valkey-instance-for-paperless).

#### Using the shared Valkey instance for paperless-ngx

To install a single (non-dedicated) Valkey instance (`mash-valkey`) and hook paperless to it, add the following **additional** configuration:

```yaml
########################################################################
#                                                                      #
# valkey                                                               #
#                                                                      #
########################################################################

valkey_enabled: true

########################################################################
#                                                                      #
# /valkey                                                              #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# paperless                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point paperless to the shared Valkey instance
paperless_redis_hostname: "{{ valkey_identifier }}"

# Make sure the paperless service (mash-paperless.service) starts after the shared KeyDB service (mash-valkey.service)
paperless_systemd_required_services_list_custom:
  - "{{ valkey_identifier }}.service"

# Make sure the paperless container is connected to the container network of the shared KeyDB service (mash-valkey)
paperless_container_additional_networks_custom:
  - "{{ valkey_identifier }}"

########################################################################
#                                                                      #
# /paperless                                                           #
#                                                                      #
########################################################################
```

This will create a `mash-valkey` Valkey instance on this host.

This is only recommended if you won't be installing other services which require KeyDB. Alternatively, go for [Creating a Valkey instance dedicated to paperless-ngx](#creating-a-valkey-instance-dedicated-to-paperless-ngx).


#### Creating a Valkey instance dedicated to paperless

The following instructions are based on the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation.

Adjust your `inventory/hosts` file as described in [Re-do your inventory to add supplementary hosts](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts), adding a new supplementary host (e.g. if `paperless.example.org` is your main one, create `paperless.example.org-deps`).

Then, create a new `vars.yml` file for the

`inventory/host_vars/paperless.example.org-deps/vars.yml`:

```yaml
---

########################################################################
#                                                                      #
# Playbook                                                             #
#                                                                      #
########################################################################

# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
# Various other secrets will be derived from this secret automatically.
mash_playbook_generic_secret_key: ''

# Override service names and directory path prefixes
mash_playbook_service_identifier_prefix: 'mash-paperless-'
mash_playbook_service_base_directory_name_prefix: 'paperless-'

########################################################################
#                                                                      #
# /Playbook                                                            #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# valkey                                                               #
#                                                                      #
########################################################################

valkey_enabled: true

########################################################################
#                                                                      #
# /valkey                                                              #
#                                                                      #
########################################################################
```

This will create a `mash-paperless-valkey` instance on this host with its data in `/mash/paperless-valkey`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/paperless.example.org/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# paperless                                                            #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point paperless to its dedicated Valkey instance
paperless_redis_hostname: mash-paperless-valkey

# Make sure the paperless service (mash-paperless.service) starts after its dedicated KeyDB service (mash-paperless-valkey.service)
paperless_systemd_required_services_list_custom:
  - "mash-paperless-valkey.service"

# Make sure the paperless container is connected to the container network of its dedicated KeyDB service (mash-paperless-valkey)
paperless_container_additional_networks_custom:
  - "mash-paperless-valkey"

########################################################################
#                                                                      #
# /paperless                                                           #
#                                                                      #
########################################################################
```
### Languages
If your documents aren't only english documents, it's recommend to set [PAPERLESS_OCR_LANGUAGE](https://docs.paperless-ngx.com/configuration/#PAPERLESS_OCR_LANGUAGE).
> It should be a 3-letter code, see the list of languages Tesseract supports.
> Set this to the language most of your documents are written in.
> This can be a combination of multiple languages such as `deu+eng`, in which case Tesseract will use whatever language matches best. Keep in mind that Tesseract uses much more CPU time with multiple languages enabled.

```
paperless_environment_variables_extension: |
   PAPERLESS_OCR_LANGUAGE=deu+eng
```

Additional if the language is not English, German, Italian, Spanish or French, the language has to be installed with the Command
[PAPERLESS_OCR_LANGUAGES](https://docs.paperless-ngx.com/configuration/#PAPERLESS_OCR_LANGUAGES)
```
paperless_environment_variables_extension: |
   PAPERLESS_OCR_LANGUAGES=tur ces chi-tra
```
> Make sure it's a space-separated list when using several values.


## Installation

If you've decided to install a dedicated Valkey instance for paperless, make sure to first do [installation](../installing.md) for the supplementary inventory host (e.g. `paperless.example.org-deps`), before running installation for the main one (e.g. `paperless.example.org`).


## Usage

Access your instance in your browser at `https://paperless.example.org`

Refer to the [official documentation](https://docs.paperless-ngx.com/) to learn how to use paperless.
