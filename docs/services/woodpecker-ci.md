# Woodpecker CI

This playbook can install and configure [Woodpecker CI](https://woodpecker-ci.org/) for you.

Woodpecker CI is a [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration) engine which can build and deploy your code automatically after pushing to a Gitea repository.

A Woodpecker CI installation contains 2 components:

- one [Woodpecker CI **server**](#woodpecker-ci-server) (web interface, central management node)
- one or more [Woodpecker CI **agent**](#woodpecker-ci-agent) instances (which run your CI jobs)

It's better to run the **agent** instances elsewhere (not on the source-control server or a server serving anything of value) - on a machine that doesn't contain sensitive data.

**Warning**: At the moment, running the **server** and **agent** on different machines cannot be done due to the server's gRPC port not being exposed publicly (at the Traefik level). If you need to do this, consider submitting a PR to the [Woodpecker CI server role](https://github.com/devture/com.devture.ansible.role.woodpecker_ci_server) to add support for this.

Small installations which only run trusted CI jobs can afford to run an agent instance on the source-control server itself.

## Woodpecker CI Server

### Dependencies

This service requires the following other services:

- a [Postgres](postgres.md) database
- a [Traefik](traefik.md) reverse-proxy server

### Configuration

Until [this Woodpecker CI issue](https://github.com/woodpecker-ci/woodpecker/issues/1636) is solved, Woodpecker CI can only be hosted at its own dedicated domain name, at the root path (`/`). It **cannot** be hosted at a subpath (e.g. `/ci`).

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# woodpecker-ci-server                                                 #
#                                                                      #
########################################################################

devture_woodpecker_ci_server_enabled: true

devture_woodpecker_ci_server_hostname: woodpecker.example.com

# Generate this secret with `openssl rand -hex 32`
devture_woodpecker_ci_server_config_agent_secret: ''

devture_woodpecker_ci_server_config_admins: [YOUR_USERNAME_HERE]

# Add one or more usernames that match your version control system (e.g. Gitea) below.
# These users will have admin privileges upon signup.
devture_woodpecker_ci_server_config_admins:
  - YOUR_USERNAME_HERE
  - ANOTHER_USERNAME_HERE

########################################################################
#                                                                      #
# /woodpecker-ci-server                                                #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the service to be hosted at `https://woodpecker.example.com`.

#### Gitea Integration

The Woodpecker CI server can integrate with [Gitea](gitea.md) using the following **additional** `vars.yml` configuration:

```yaml
devture_woodpecker_ci_server_provider: gitea

# We must use the public URL here, because it's also used for login redirects
devture_woodpecker_ci_server_config_gitea_url: "{{ gitea_config_root_url }}"

# Populate these with the OAuth 2 application information
# (see the Gitea configuration section above)
devture_woodpecker_ci_server_config_gitea_client: GITEA_OAUTH_CLIENT_ID_HERE
devture_woodpecker_ci_server_config_gitea_secret: GITEA_OAUTH_CLIENT_SECRET_HERE

devture_woodpecker_ci_server_container_add_host_domain_name: "{{ gitea_hostname }}"
devture_woodpecker_ci_server_container_add_host_ip_address: "{{ ansible_host }}"
```

To integrate with version-control systems other than Gitea, you'll need similar configuration.

### Usage

After installation, you should be able to access the Woodpecker CI server instance at `https://woodpecker.DOMAIN` (matching the `devture_woodpecker_ci_server_hostname` value configured in `vars.yml`).

The **Log in** button should take you to Gitea, where you can authorize Woodpecker CI with the OAuth 2 application.

Follow the official Woodpecker CI [Getting started](https://woodpecker-ci.org/docs/usage/intro) documentation for additional usage details.


## Woodpecker CI Agent

As mentioned above, unless you completely trust your CI workloads, it's best to run the Woodpecker CI Agent on another machine.

### Dependencies

This service requires the following other services:

- a Woodpecker CI Server - installed via this playbook or otherwise

### Configuration

```yaml
########################################################################
#                                                                      #
# woodpecker-ci-agent                                                  #
#                                                                      #
########################################################################

devture_woodpecker_ci_agent_enabled: true

# If the agent runs on the same machine as the server, enabling the agent
# is everything you need. The agent and server will be wired automatically.
#
# Otherwise, you'll need to configure the variables below:

# This needs to point to the server's gRPC port.
# By default, this port is not exposed, so.. you may need to do some extra work,
# which possibly involves contributing a PR to the Woodpecker CI server role:
# https://github.com/devture/com.devture.ansible.role.woodpecker_ci_server
devture_woodpecker_ci_agent_config_server: ''

# Enter your server's secret below.
# This value must match the `devture_woodpecker_ci_server_config_agent_secret` variable.
devture_woodpecker_ci_agent_config_agent_secret: ''

########################################################################
#                                                                      #
# /woodpecker-ci-agent                                                 #
#                                                                      #
########################################################################
```

### Usage

The agent should automatically register with the [Woodpecker CI server](#woodpecker-ci-server) and take jobs from it.
