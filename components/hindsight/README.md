<!--
SPDX-FileCopyrightText: 2026 MASH project contributors
SPDX-FileCopyrightText: 2026 Robin Miller

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Hindsight

The playbook can install and configure [Hindsight](https://hindsight.vectorize.io/) for you.

Hindsight is an agent memory service: it extracts facts from content, stores them in PostgreSQL, and answers queries over them. It runs as two containers: an API (the memory engine, exposing `retain`, `recall` and `reflect`) and a control plane (the web UI).

See the project's [documentation](https://hindsight.vectorize.io/) to learn what Hindsight does and why it might be useful to you.

For details about configuring the [Ansible role for Hindsight](https://forgejo.littlecedar.net/littlecedar/ansible-role-mash-hindsight), you can check them via:

- 🌐 [the role's documentation](https://forgejo.littlecedar.net/littlecedar/ansible-role-mash-hindsight/src/branch/main/docs/configuring-hindsight.md) online
- 📁 `roles/galaxy/hindsight/docs/configuring-hindsight.md` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Traefik](traefik.md) reverse-proxy server
- An external **PostgreSQL 14+** instance with a vector extension (`pgvector` by default)

The role does not run a database. It also does not run an LLM, embedding or reranker provider: all of those are external, including with the `full` image variant.

## Prerequisites

The API runs its own migrations on startup, but the database and the vector extension must already exist. This cannot be handled by the playbook's [Postgres](postgres.md) integration, because the `postgres` role does not create PostgreSQL extensions.

Create the database on an existing PostgreSQL instance, using an image that ships the extension (the upstream `postgres` image does not):

```sh
docker run --rm -it --network=<postgres container network> pgvector/pgvector:pg18-trixie \
  psql "postgresql://<admin-user>:<admin-password>@<postgres-host>:5432/postgres" \
  -c 'CREATE ROLE hindsight LOGIN PASSWORD '"'"'<password>'"'"';' \
  -c 'CREATE DATABASE hindsight OWNER hindsight;'

docker run --rm -it --network=<postgres container network> pgvector/pgvector:pg18-trixie \
  psql "postgresql://<admin-user>:<admin-password>@<postgres-host>:5432/hindsight" \
  -c 'CREATE EXTENSION IF NOT EXISTS vector;'
```

If you use the playbook's `postgres` role and set its image to `pgvector/pgvector`, the role's [managed database](postgres.md) feature creates the database and role for you, but you still have to run the `CREATE EXTENSION` statement above against the new database.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# hindsight                                                            #
#                                                                      #
########################################################################

hindsight_enabled: true

hindsight_hostname: mash.example.com

# The PostgreSQL connection string. This role does not run a database.
hindsight_api_database_url: "postgresql://hindsight:PASSWORD_HERE@postgres:5432/hindsight"

# Provider configuration. The default `slim` image bundles no local embedding
# or reranker models, so both must be set. Provider settings are namespaced by
# provider — note `_OPENAI_` / `_COHERE_`, not a bare `_API_KEY`.
hindsight_api_environment_variables_additional_variables: |
  HINDSIGHT_API_LLM_PROVIDER=openai
  HINDSIGHT_API_LLM_API_KEY=sk-xxx
  HINDSIGHT_API_LLM_MODEL=gpt-4o-mini
  HINDSIGHT_API_EMBEDDINGS_PROVIDER=openai
  HINDSIGHT_API_EMBEDDINGS_OPENAI_API_KEY=sk-xxx
  HINDSIGHT_API_EMBEDDINGS_OPENAI_MODEL=text-embedding-3-small
  HINDSIGHT_API_RERANKER_PROVIDER=cohere
  HINDSIGHT_API_RERANKER_COHERE_API_KEY=xxx

########################################################################
#                                                                      #
# /hindsight                                                           #
#                                                                      #
########################################################################
```

### Exposing ports

The API is not exposed through Traefik; only the Control Plane is. By default neither service publishes a port, and both are reached through the reverse proxy. To reach them directly, for example from a client that does not go through the proxy:

```yaml
# Access to the Hindsight API
hindsight_api_host_bind_port: "127.0.0.1:8888"

# Access to the Control Plane UI
hindsight_controlplane_host_bind_port: "127.0.0.1:9999"
```

### Container user

The playbook runs both containers as the playbook's own user (`mash_playbook_uid`/`mash_playbook_gid`, wired to `hindsight_uid`/`hindsight_gid`), since neither upstream image ships a user for both services. The role then mounts the host's `/etc/passwd` read-only so the UID resolves to a real name, and points `HOME` at a writable tmpfs. Set `hindsight_uid`/`hindsight_gid` to `""` to keep the images' own users instead; both must be set or empty together.

### Image variants

`hindsight_api_image_variant` selects the published API image:

| Variant | Size | Bundled models |
| --- | --- | --- |
| `slim` (default) | ~500 MB | None — external embedding and reranker providers required |
| `full` | ~9 GB | Embedding and reranker models; the LLM is still external |

Both are published under the same version, so the role builds the tag as `<version>-<variant>`.

### Running the API only

The two services are independently toggleable and both are enabled by default. To run the API only, for example when the Control Plane is hosted elsewhere:

```yaml
hindsight_controlplane_enabled: false
```

### Authentication

The API is unauthenticated by default. To require an API key on every request, enable the built-in tenant extension:

```yaml
hindsight_api_tenant_extension: "hindsight_api.extensions.builtin.tenant:ApiKeyTenantExtension"

hindsight_api_environment_variables_additional_variables: |
  HINDSIGHT_API_TENANT_API_KEY=YOUR_SECRET_API_KEY
```

and give the Control Plane the same key:

```yaml
hindsight_controlplane_dataplane_api_key: "YOUR_SECRET_API_KEY"
```

Independently of that, `hindsight_controlplane_access_key` protects the Control Plane UI itself: when set, users must enter it to log in.

### Subpath deployment

Setting `hindsight_path_prefix` to something other than `/` (e.g. `/hindsight`) serves the API under that prefix. The role passes it as `HINDSIGHT_API_BASE_PATH` and adds Traefik strip-prefix and slashless-redirect middlewares.

The Control Plane's `NEXT_PUBLIC_BASE_PATH` is compiled into its Next.js bundle at build time and cannot be set from the environment, so the Control Plane only works correctly at `/` unless you build a custom image.

## Usage

After running the installation command, the Control Plane becomes available at the URL specified with `hindsight_hostname`. With the configuration above, the service is hosted at `https://mash.example.com`.

The API is reachable on the same host under `/v1/...` paths. Point your agent, MCP client or SDK at `https://mash.example.com`. Memory banks are created through the Control Plane.

Because the role does not expose the API through Traefik, a client that cannot reach the Control Plane's host can use `hindsight_api_host_bind_port` instead.

## Troubleshooting

### Check the service's logs

You can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu mash-hindsight-api` or `journalctl -fu mash-hindsight-controlplane` (or how you/your playbook named the service).

## Related services

- [Postgres](postgres.md) — the database the API stores memories in