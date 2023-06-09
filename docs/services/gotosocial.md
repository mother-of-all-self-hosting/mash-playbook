# GoToSocial

[GoToSocial](https://gotosocial.org/) is a self-hosted [ActivityPub](https://activitypub.rocks/) social network server, that this playbook can install, powered by the [mother-of-all-self-hosting/ansible-role-gotosocial](https://github.com/mother-of-all-self-hosting/ansible-role-gotosocial) Ansible role.

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# gotosocial                                                           #
#                                                                      #
########################################################################

gotosocial_enabled: true


# Hostname that this server will be reachable at.
# DO NOT change this after your server has already run once, or you will break things!
# Examples: ["gts.example.org","some.server.com"]
gotosocial_hostname: 'social.example.org'

########################################################################
#                                                                      #
# /gotosocial                                                          #
#                                                                      #
########################################################################
```

After installation, you can use `just run-tags gotosocial-add-user --extra-vars=username=<username> --extra-vars=password=<password> --extra-vars=email=<email>"`
to create your a user. Change `--tags=gotosocial-add-user` to `--tags=gotosocial-add-admin` to create an admin account.

## Advanced account domain configuration

The account domain is the second part of a user handle in the Fediverse. If your handle is @username@example.org, `example.org` is your account domain. By default GoToSocial will use `gotosocial_hostname` that you provide as account domain e.g. `social.example.org`. You might want to change this by setting `gotosocial_account_domain` if you want the domain on accounts to be `example.org` because it looks better or is just shorter/easier to remember.

**Warning** DO NOT change this change this after your server has already run once, or you will break things!

If you decide to use this read [the appropriate section of the installation guide](https://docs.gotosocial.org/installation_guide/advanced/#can-i-host-my-instance-at-fediexampleorg-but-have-just-exampleorg-in-my-username=) as you will have to do some additional work on the base domain.

```yaml
gotosocial_account_domain: "example.org"
```

## E-Mail configuration

You can use the following variables in your `vars.yml` to enable e-mail notifications.

```yml
# Check out https://docs.gotosocial.org/en/latest/configuration/smtp/ for a configuration reference
gotosocial_smtp_host: 'smtp.example.org'
gotosocial_smtp_username: gotosocial@example.org
gotosocial_smtp_password: yourpassword
gotosocial_smtp_from: gotosocial@example.org
```

## Usage

After [installing](../installing.md), you can visit at the URL specified in `gotosocial_hostname` and should see your instance.
Start to customize it at `social.example.org/admin`.

Use the [GtS CLI Tool](https://docs.gotosocial.org/en/latest/admin/cli/) to do admin & maintenance tasks. E.g. use 
```bash
docker exec -it mash-gotosocial /gotosocial/gotosocial admin account demote --username <username>
```
to demote a user from admin to normal user.

Refer to the [great official documentation](https://docs.gotosocial.org/en/latest/) for more information on GoToSocial.



## Migrate an existing instance

The following assumes you want to migrate from `serverA` to `serverB` (managed by mash) but you just cave to adjust the copy commands if you are on the same server.

Stop the initial instance on `serverA`

```bash
serverA$ systemctl stop gotosocial
```

Dump the database (depending on your existing setup you might have to adjust this)
```
serverA$ pg_dump gotosocial > latest.sql
```

Copy the files to the new server

```bash
serverA$ rsync -av -e "ssh" latest.sql root@serverB:/mash/gotosocial/
serverA$ rsync -av -e "ssh" data/* root@serverB:/mash/gotosocial/data/
```

Install (but don't start) the service and database on the server.

```bash
yourPC$ just run-tags install-all
yourPC$ just run-tags import-postgres --extra-vars=server_path_postgres_dump=/mash/gotosocial/latest.sql --extra-vars=postgres_default_import_database=mash-gotosocial
```

Start the services on the new server

```bash
yourPC$ just run-tags start
```

Done 🥳
