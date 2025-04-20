# Forgejo Runner

[Forgejo Runner](https://code.forgejo.org/forgejo/runner) is a runner to use with [Forgejo Actions](https://forgejo.org/docs/latest/admin/actions/). It provides a way to perform CI using Forgejo. You might also be interested in [Woodpecker CI](https://woodpecker-ci.org/) (that this playbook also [supports](woodpecker-ci.md)).

> [!WARNING]
> Upstream considers this software as being an **alpha release**, and says it should **not** be considered secure enough to deploy in production. Use at your own risk.


## Configuration

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

Labels are an important aspect of the runner, and as such should be carefully chosen. Read [the official documentation](https://forgejo.org/docs/latest/admin/actions/#labels-and-runs-on) for more information.


## Usage

After the installation, the runner will register with the Forgejo instance (provided via the `forgejo_runner_instance_url` variable) and generate a `.runner` file inside its configuration path. This file should not be modified manually. If for some reason you wish to force the registration to run again, you can delete the `.runner` file and restart the service.

If you wish to change the labels associated with the runner, you can simply modify the `forgejo_runner_labels` variable and run the playbook again. There is no need to delete the `.runner` file and run the registration again.
