<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 MASH project contributors
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Sergio Durigan Junior

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Forgejo Runner

The playbook can install and configure [Forgejo Runner](https://code.forgejo.org/forgejo/runner) for you.

Forgejo Runner is a runner to use with [Forgejo Actions](https://forgejo.org/docs/latest/admin/actions/). It provides a way to perform CI using Forgejo.

See the project's [documentation](https://forgejo.org/docs/latest/admin/actions/runner-installation/) to learn what Forgejo Runner does and why it might be useful to you.

> [!WARNING]
> The projects' documentation does **not recommend** running Forgejo Runner on the same machine as the Forgejo instance for security reasons.

## Prerequisites

### Retrieve a registration token

To set up Forgejo Runner for Forgejo, you will need to retrieve the registration token which is used for registering the runner on the Forgejo instance.

The registration token can be obtained via Forgejo's web interface by going to `Site Administration -> Actions -> Runners -> Create new runner`. See [this section](https://forgejo.org/docs/latest/admin/actions/runner-installation/#standard-registration) on the official documentation for the latest information.

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# forgejo_runner                                                       #
#                                                                      #
########################################################################

forgejo_runner_enabled: true

########################################################################
#                                                                      #
# /forgejo_runner                                                      #
#                                                                      #
########################################################################
```

### Set the Forgejo instance URL

It is necessary to specify the URL of the Forgejo instance as well, for which the runner is used. Add the following configuration to your `vars.yml` file:

```yaml
forgejo_runner_instance_url: "https://example.com"
```

If the Forgejo instance is also managed by the playbook and set to be accessible at `https://mash.example.com/forgejo`, you can set the URL as below:

```yaml
forgejo_runner_instance_url: "{{ forgejo_hostname }}{{ forgejo_path_prefix }}"
```

Remove `{{ forgejo_path_prefix }}` if the instance is not configured to host under the subpath.

### Set the registration token

You also need to set the registration token retrieved on the Forgejo instance by adding the following configuration to your `vars.yml` file:

```yaml
forgejo_runner_registration_token: REGISTRATION_TOKEN_HERE
```

### Set runner's labels

It is required to specify the labels of a runner, which are used to determine which jobs the runner can run, and how to run them.

For example, you can specify a label to `forgejo_runner_labels` as below:

```yaml
forgejo_runner_labels:
  - ubuntu-22.04:docker://node:20-bullseye
```

Since the labels are an important aspect of the runner, they should be carefully chosen. Read [the official documentation](https://forgejo.org/docs/latest/admin/actions/#choosing-labels) for more information.

### Customize the runner's name (optional)

By default the runner's name is set to `forgejo-runner-by-mash-playbook`. You can customize it by adding the following configuration to your `vars.yml` file:

```yaml
forgejo_runner_runner_name: "Your Runner Name Here"
```

### Increase the capacity (optional)

By default the playbook specifies the capacity of the runner (how many concurrent tasks it can run) to `1`. You can increase it per the computation power of the machine where the runner is used by adding the following configuration to your `vars.yml` file:

```yaml
forgejo_runner_capacity: 2
```

## Usage

After running the command for installation, the Forgejo Runner instance becomes available.

>[!NOTE]
> The runner will register with the Forgejo instance (provided via the `forgejo_runner_instance_url` variable) and generate a `.runner` file inside its configuration path. This file should not be modified manually. If for some reason you wish to force the registration to run again, you can delete the `.runner` file and restart the service.
>
> If you wish to change the labels associated with the runner, you can simply modify the `forgejo_runner_labels` variable and run the playbook again. There is no need to delete the `.runner` file and run the registration again.

## Related services

- [Forgejo](forgejo.md) — Self-hosted lightweight software forge (Git hosting service, etc.)
- [Woodpecker CI](woodpecker-ci.md) — Simple Continuous Integration (CI) engine with great extensibility
