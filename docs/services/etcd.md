# etcd

[etcd](https://etcd.io/) is a strongly consistent, distributed key-value store that provides a reliable way to store data that needs to be accessed by a distributed system or cluster of machines. It gracefully handles leader elections during network partitions and can tolerate machine failure, even in the leader node.

Our current setup and documentation are **aiming at running etcd for internal purposes** (as a dependency for other [services](../supported-services.md)).

If you need a production deployment, you will need to install multiple etcd instances (on multiple machines) and connect them in a cluster.
This is beyond the scope of our documentation here.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# etcd                                                                 #
#                                                                      #
########################################################################

etcd_enabled: true

# By default, the playbook will set a root password by itself.
# If you'd like to set your own, uncomment and explicitly set this.
# etcd_environment_variable_etcd_root_password: ''

# Uncomment this if you'd like to run etcd without password-protection.
# etcd_environment_variable_allow_none_authentication: true

########################################################################
#                                                                      #
# /etcd                                                                #
#                                                                      #
########################################################################
```

If you'd like to do something more advanced, the [`ansible-role-etcd` Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-etcd) is very configurable and should not get in your way of exposing ports or configuring arbitrary settings.

Take a look at [its `default/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-etcd/blob/main/defaults/main.yml) for available Ansible variables you can use in your own `vars.yml` configuration file.


## Usage

As mentioned above, the purpose of the etcd component in this Ansible playbook is to serve as a dependency for other [services](../supported-services.md). For this use-case, you don't need to do anything special beyond enabling the component.
