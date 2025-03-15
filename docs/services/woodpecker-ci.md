# Woodpecker CI

This playbook can install and configure [Woodpecker CI](https://woodpecker-ci.org/) for you.

Woodpecker CI is a [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration) engine which can build and deploy your code automatically after pushing to a [Gitea](./gitea.md) or [Forgejo](./forgejo.md) repository.
If you are using [Forgejo](./forgejo.md), you might also be interested in [Forgejo Runner](https://code.forgejo.org/forgejo/runner) (that this playbook also [supports](forgejo-runner.md)).

A Woodpecker CI installation contains 2 components:

- one [Woodpecker CI **server**](#woodpecker-ci-server) (web interface, central management node)
- one or more [Woodpecker CI **agent**](#woodpecker-ci-agent) instances (which run your CI jobs)

It's better to run the **agent** instances elsewhere (not on the source-control server or a server serving anything of value) — on a machine that doesn't contain sensitive data.

Small installations which only run trusted CI jobs can afford to run an agent instance on the source-control server itself.

## Woodpecker CI Server

### Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

### Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# woodpecker-ci-server                                                 #
#                                                                      #
########################################################################

woodpecker_ci_server_enabled: true

woodpecker_ci_server_hostname: mash.example.com

woodpecker_ci_server_path_prefix: /ci

# Generate this secret with `openssl rand -hex 32`
#
# Note that this playbook only supports agent-specific secrets, which
# means that if you choose to share this secret with an agent, the
# server will register it as a non-persistent agent.
#
# See the definition of
# woodpecker_ci_agent_config_agent_secret below for more details.
woodpecker_ci_server_config_agent_secret: ''

woodpecker_ci_server_config_admins: [YOUR_USERNAME_HERE]

# Add one or more usernames that match your version control system (e.g. Gitea) below.
# These users will have admin privileges upon signup.
woodpecker_ci_server_config_admins:
  - YOUR_USERNAME_HERE
  - ANOTHER_USERNAME_HERE

# Uncomment the line below if you'll be running Woodpecker CI agents on remote machines.
# If you'll only run agents on the same machine as the server, you can keep gRPC expose disabled.
# woodpecker_ci_server_container_labels_traefik_grpc_enabled: true

########################################################################
#                                                                      #
# /woodpecker-ci-server                                                #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://mash.example.com/ci`.

If you want to host the service at the root path, remove the `woodpecker_ci_server_path_prefix` variable override.

#### Gitea Integration

The Woodpecker CI server can integrate with [Gitea](gitea.md) using the following **additional** `vars.yml` configuration:

```yaml
woodpecker_ci_server_provider: gitea

# We must use the public URL here, because it's also used for login redirects
woodpecker_ci_server_config_gitea_url: "{{ gitea_config_root_url }}"

# Populate these with the OAuth 2 application information
# (see the Gitea configuration section above)
woodpecker_ci_server_config_gitea_client: GITEA_OAUTH_CLIENT_ID_HERE
woodpecker_ci_server_config_gitea_secret: GITEA_OAUTH_CLIENT_SECRET_HERE

woodpecker_ci_server_container_add_host_domain_name: "{{ gitea_hostname }}"
woodpecker_ci_server_container_add_host_ip_address: "{{ ansible_host }}"
```

#### Forgejo Integration

The Woodpecker CI server can integrate with [Forgejo](forgejo.md) using the following **additional** `vars.yml` configuration:

```yaml
woodpecker_ci_server_provider: forgejo

# We must use the public URL here, because it's also used for login redirects
woodpecker_ci_server_config_forgejo_url: "{{ forgejo_config_root_url }}"

# Populate these with the OAuth 2 application information
# (see the Forgejo configuration section above)
woodpecker_ci_server_config_forgejo_client: FORGEJO_OAUTH_CLIENT_ID_HERE
woodpecker_ci_server_config_forgejo_secret: FORGEJO_OAUTH_CLIENT_SECRET_HERE

woodpecker_ci_server_container_add_host_domain_name: "{{ forgejo_hostname }}"
woodpecker_ci_server_container_add_host_ip_address: "{{ ansible_host }}"
```

### Usage

After installation, you should be able to access the Woodpecker CI server instance at `https://mash.DOMAIN/ci` (matching the `woodpecker_ci_server_hostname` and `woodpecker_ci_server_path_prefix` values configured in `vars.yml`).

The **Log in** button should take you to Gitea, where you can authorize Woodpecker CI with the OAuth 2 application.

Follow the official Woodpecker CI [Getting started](https://woodpecker-ci.org/docs/usage/intro) documentation for additional usage details.


## Woodpecker CI Agent

As mentioned above, unless you completely trust your CI workloads, it's best to run the Woodpecker CI Agent on another machine.

### Dependencies

This service requires the following other services:

- a Woodpecker CI Server — installed via this playbook or otherwise

### Configuration

```yaml
########################################################################
#                                                                      #
# woodpecker-ci-agent                                                  #
#                                                                      #
########################################################################

woodpecker_ci_agent_enabled: true

# If the agent runs on the same machine as the server, enabling the agent
# is everything you need. The agent and server will be wired automatically.
#
# Otherwise, you'll need to configure the variables below:

# This needs to point to the server's gRPC host:port.
# If your Woodpecker CI Server is deployed using this playbook, its
# gRPC port will likely be 443. E.g., ci.example.com:443.
woodpecker_ci_agent_config_server: ''

# This playbook only supports agent-specific secrets, i.e., it is not recommended to use
# a shared secret between Woodpecker CI Server and all of its agents. Please refer to
# the following upstream documentation in order to learn how to register an agent and
# obtain a secret for it:
#
#   https://woodpecker-ci.org/docs/administration/agent-config#using-agent-token
#
# then, when you have the agent secret, uncomment the following line.
#woodpecker_ci_agent_config_agent_secret: ''

# Uncomment the line below if you want the agent to connect to the
# server over a secure gRPC channel (recommended).
#woodpecker_ci_agent_config_grpc_secure: true

# Uncomment the line below if you want the agent to verify the
# server's TLS certificate when connecting over a secure gRPC channel.
#woodpecker_ci_agent_config_grpc_verify: true

########################################################################
#                                                                      #
# /woodpecker-ci-agent                                                 #
#                                                                      #
########################################################################
```

### Usage

The agent should automatically register with the [Woodpecker CI server](#woodpecker-ci-server) and take jobs from it.
