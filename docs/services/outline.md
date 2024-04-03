# Outline

[Outline](https://www.getoutline.com/) is an open-source knowledge base for growing teams.


## Dependencies

This service requires the following other services:

- [Postgres](postgres.md)
- [KeyDB](keydb.md)
- a [Traefik](traefik.md) reverse-proxy server


## Configuration

To enable this service, besides enabling the [required Dependencies](#dependencies), add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# outline                                                              #
#                                                                      #
########################################################################

outline_enabled: true

outline_hostname: outline.example.com

# This must be generated with: `openssl rand -hex 32`
outline_environment_variable_secret_key: ''

# The configuration below connects Outline to the KeyDB instance, for session storage purposes.
# You may wish to run a separate KeyDB instance for Outline, because KeyDB is not multi-tenant.
# Read more in docs/services/keydb.md.
outline_redis_hostname: "{{ keydb_identifier if keydb_enabled else '' }}"

outline_container_additional_networks_custom: |
  {{
    [keydb_container_network]
  }}

# By default, files are stored locally.
# To use another file storage provider, see the "File Storage" section below.

# At least one authentication method MUST be enabled for Outline to work.
# See the "Authentication" section below.

########################################################################
#                                                                      #
# /outline                                                             #
#                                                                      #
########################################################################
```

### URL

In the example configuration above, we configure the service to be hosted at `https://outline.example.com`.

While the Outline Ansible role provides an `outline_path_prefix` variable, Outline does not support being hosted at a subpath right now.

### File Storage

Outline supports multiple [file storage](https://docs.getoutline.com/s/hosting/doc/file-storage-N4M0T6Ypu7) mechanisms.

The default configuration stores files locally in a `data` directory, but you can also stores files on AWS S3 (or [compatible S3 altenative](https://docs.getoutline.com/s/hosting/doc/file-storage-N4M0T6Ypu7#h-s3-compatible-services)).

To enable S3 storage, add the following to your `vars.yml` configuration:

```yml
outline_environment_variable_file_storage: s3

outline_environment_variable_aws_access_key_id: ''
outline_environment_variable_aws_secret_access_key: ''
outline_environment_variable_aws_region: eu-central-1 # example
outline_environment_variable_aws_s3_upload_bucket_url: https://OUTLINE_ASSETS_BUCKET_NAME.s3.eu-central-1.amazonaws.com
outline_environment_variable_aws_s3_upload_bucket_name: OUTLINE_ASSETS_BUCKET_NAME
outline_environment_variable_aws_s3_force_path_style: false
```

### Authentication

For Outline to work, at least one [authentication method](https://docs.getoutline.com/s/hosting/doc/authentication-7ViKRmRY5o) must be enabled.

The Outline Ansible role provides dedicated Ansible variables for configuring these authentication methods via environment variables (see the `outline_environment_variable_*` variables in [`defaults/main.yml` of ansible-role-outline](https://github.com/mother-of-all-self-hosting/ansible-role-outline/blob/main/defaults/main.yml)).

If you need to pass additional environment variables to Outline, for which dedicated Ansible variables are not available, you can use `outline_environment_variables_additional_variables`.

If you define SMTP settings (see the `outline_environment_variable_smtp_*` variables in `defaults/main.yml`), the [Email magic link](https://docs.getoutline.com/s/hosting/doc/email-magic-link-N2CPh5tmTS) authentication method will be enabled:

Unfortunately, even with SMTP settings being defined, we haven't been able to get Outline to succesfully send emails just yet, hitting issues similar to [this one](https://github.com/outline/outline/discussions/2605).
