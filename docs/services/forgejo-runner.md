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
> Upstream considers this software as being an **alpha release**, and [claims](https://code.forgejo.org/forgejo/runner#forgejo-runner) it should **not** be considered secure enough to deploy in production. Use at your own risk. Also note that the documentation does **not recommend** running Forgejo Runner on the same machine as the Forgejo instance for security reasons.

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# forgejo-runner                                                       #
#                                                                      #
########################################################################

forgejo_runner_enabled: true

forgejo_runner_runner_name: "Your Runner Name Here"

# The instance URL.
forgejo_runner_instance_url: "https://example.com"

# The registration token.
#
# Should be obtained via the web interface, by going to:
#
#   Site Administration -> Actions -> Runners -> Create new runner
forgejo_runner_registration_token: "TOKEN_HERE"

# The capacity of the runner, i.e., how many concurrent tasks it can run.
forgejo_runner_capacity: 1

# The labels associated with this runner.
forgejo_runner_labels:
  - ubuntu-22.04:docker://node:20-bullseye

########################################################################
#                                                                      #
# /forgejo-runner                                                      #
#                                                                      #
########################################################################
```

As mentioned in the example above, the registration token should be obtained via Forgejo's web interface, by going to `Site Administration -> Actions -> Runners -> Create new runner`.

Labels are an important aspect of the runner, and as such should be carefully chosen. Read [the official documentation](https://forgejo.org/docs/latest/admin/actions/#choosing-labels) for more information.

## Usage

After running the command for installation, the Forgejo Runner instance becomes available.

The runner will register with the Forgejo instance (provided via the `forgejo_runner_instance_url` variable) and generate a `.runner` file inside its configuration path. This file should not be modified manually. If for some reason you wish to force the registration to run again, you can delete the `.runner` file and restart the service.

If you wish to change the labels associated with the runner, you can simply modify the `forgejo_runner_labels` variable and run the playbook again. There is no need to delete the `.runner` file and run the registration again.

## Related services

- [Forgejo](forgejo.md)
- [Woodpecker CI](woodpecker-ci.md)
