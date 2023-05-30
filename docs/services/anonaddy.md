# AnonAddy

[AnonAddy](https://anonaddy.com/) is an open-source Anonymous Email Forwarding. MASH can install AnonAddy with the [`nielscil/ansible-role-anonaddy`](https://github.com/nielscil/ansible-role-anonaddy) ansible role.


## Dependencies

This service requires the following other services:

- a [MariaDB](mariadb.md) database
- a [Redis](redis.md) data-store, installation details [below](#redis)
- a [Traefik](traefik.md) reverse-proxy server

This service requires the following ports:
- Port 25 for SMTP communication

## DNS Configuration

This service requires extra DNS records. The following setup is an example where:

- AnonAddy website is reachable from: `https://anonaddy.example.com`
- RSPAMD is reachable from: `https://anonaddy-rspamd.example.com`
- AnonAddy maildomain is: `localpart@anonaddy.example.com`

| Description                | Type  | Host                                      | Priority | Weight | Target                           |
|--------------------------- |-------|-------------------------------------------|----------|--------|----------------------------------|
| AnonAddy site              | CNAME | `anonaddy.example.com`                    | -        | -      | `mash.example.com`               |
| RSPAMD (optional)          | CNAME | `anonaddy-rspamd.example.com`             | -        | -      | `mash.example.com`               |
| Mail                       | MX    | `anonaddy.example.com`                    | 10       | 0      | `mash.example.com`               |
| DKIM (optional)            | TXT   | `default._domainkey.anonaddy.example.com` | -        | -      | Get from `install-anonaddy-dkim` |
| DMARC (optional)           | TXT   | `_dmarc.anonaddy.example.com`             | -        | -      | `v=DMARC1; p=quarantine;`        |
| SPF (optional)             | TXT   | `anonaddy.example.com`                    | -        | -      | `v=spf1 ip4:<your-ip> -all`      |

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# AnonAddy                                                            #
#                                                                      #
########################################################################

anonaddy_enabled: true

anonaddy_hostname: anonaddy.example.com

# Put a strong secret below, generated with `#base64:$(openssl rand -base64 32)` or in another way
anonaddy_key: '' 
# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
anonaddy_secret: ''

anonaddy_domain: anonaddy.example.com

# Redis configuration, as described below

# DKIM configuration (optional), as as described below

# GPG configuration (optional), as as described below

########################################################################
#                                                                      #
# /AnonAddy                                                           #
#                                                                      #
########################################################################
```

### Redis

As described on the [Redis](redis.md) documentation page, if you're hosting additional services which require Redis on the same server, you'd better go for installing a separate Redis instance for each service. See [Creating a Redis instance dedicated to AnonAddy](#creating-a-redis-instance-dedicated-to-anonaddy).

If you're only running AnonAddy on this server and don't need to use Redis for anything else, you can [use a single Redis instance](#using-the-shared-redis-instance-for-anonaddy).

#### Using the shared Redis instance for AnonAddy

To install a single (non-dedicated) Redis instance (`mash-redis`) and hook AnonAddy to it, add the following **additional** configuration:

```yaml
########################################################################
#                                                                      #
# redis                                                                #
#                                                                      #
########################################################################

redis_enabled: true

########################################################################
#                                                                      #
# /redis                                                               #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# AnonAddy                                                             #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point AnonAddy to the shared Redis instance
anonaddy_redis_host: "{{ redis_identifier }}"

# Make sure the AnonAddy service (mash-anonaddy.service) starts after the shared Redis service (mash-redis.service)
anonaddy_systemd_required_services_list_custom:
  - "{{ redis_identifier }}.service"

# Make sure the AnonAddy container is connected to the container network of the shared Redis service (mash-redis)
anonaddy_container_additional_networks_custom:
  - "{{ redis_identifier }}"

########################################################################
#                                                                      #
# /AnonAddy                                                            #
#                                                                      #
########################################################################
```

This will create a `mash-redis` Redis instance on this host.

This is only recommended if you won't be installing other services which require Redis. Alternatively, go for [Creating a Redis instance dedicated to AnonAddy](#creating-a-redis-instance-dedicated-to-anonaddy).


#### Creating a Redis instance dedicated to AnonAddy

The following instructions are based on the [Running multiple instances of the same service on the same host](../running-multiple-instances.md) documentation.

Adjust your `inventory/hosts` file as described in [Re-do your inventory to add supplementary hosts](../running-multiple-instances.md#re-do-your-inventory-to-add-supplementary-hosts), adding a new supplementary host (e.g. if `anonaddy.example.com` is your main one, create `anonaddy.example.com-deps`).

Then, create a new `vars.yml` file for the

`inventory/host_vars/anonaddy.example.com-deps/vars.yml`:

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
mash_playbook_service_identifier_prefix: 'mash-anonaddy-'
mash_playbook_service_base_directory_name_prefix: 'anonaddy-'

########################################################################
#                                                                      #
# /Playbook                                                            #
#                                                                      #
########################################################################


########################################################################
#                                                                      #
# redis                                                                #
#                                                                      #
########################################################################

redis_enabled: true

########################################################################
#                                                                      #
# /redis                                                               #
#                                                                      #
########################################################################
```

This will create a `mash-anonaddy-redis` instance on this host with its data in `/mash/anonaddy-redis`.

Then, adjust your main inventory host's variables file (`inventory/host_vars/anonaddy.example.com/vars.yml`) like this:

```yaml
########################################################################
#                                                                      #
# AnonAddy                                                             #
#                                                                      #
########################################################################

# Base configuration as shown above

# Point AnonAddy to its dedicated Redis instance
anonaddy_redis_host: mash-anonaddy-redis

# Make sure the AnonAddy service (mash-anonaddy.service) starts after its dedicated Redis service (mash-anonaddy-redis.service)
anonaddy_systemd_required_services_list_custom:
  - "mash-anonaddy-redis.service"

# Make sure the AnonAddy container is connected to the container network of its dedicated Redis service (mash-anonaddy-redis)
anonaddy_container_additional_networks_custom:
  - "mash-anonaddy-redis"

########################################################################
#                                                                      #
# /AnonAddy                                                            #
#                                                                      #
########################################################################
```

### DKIM and RSPAMD (optional)

If you want to use RSPAMD or want AnonAddy to have a lower spam-score, you should enable DKIM. The role can generate a DKIM key, see [install dkim](#install-dkim-optional), which then can be placed in the main inventory configuration like this:

```yaml
########################################################################
#                                                                      #
# AnonAddy                                                             #
#                                                                      #
########################################################################

# Base configuration as shown above

# RSPAMD
anonaddy_rspamd_enabled: true
# Put a strong secret below, generated with `pwgen -s 64 1` or in another way
anonaddy_rspamd_password: ''
# hostname should be unique and not part of main anonaddy domain
anonaddy_rspamd_hostname: anonaddy-rspamd.example.com

# Get the path from install-anonaddy-dkim
anonaddy_dkim_signing_key_path: '/data/dkim/anonaddy.example.com.private'

########################################################################
#                                                                      #
# /AnonAddy                                                            #
#                                                                      #
########################################################################
```

### GPG (optional)

If you want AnonAddy to have the possibility to encrypt the emails between you/your AnonAddy users and AnonAddy, you should enable GPG. The role can import a GPG key, see [install GPG](#install-gpg-optional). Before importing, you should add the following configuration:

```yaml
########################################################################
#                                                                      #
# AnonAddy                                                             #
#                                                                      #
########################################################################

# Base configuration as shown above

# the GPG private key generated following the install instructions
anonaddy_gpg_signing_key: ''
anonaddy_gpg_signing_key_fingerprint: ''

########################################################################
#                                                                      #
# /AnonAddy                                                            #
#                                                                      #
########################################################################
```

## Installation

If you've decided to install a dedicated Redis instance for AnonAddy, make sure to first do [installation](../installing.md) for the supplementary inventory host (e.g. `anonaddy.example.com-deps`), before running installation for the main one (e.g. `anonaddy.example.com`).

### Install DKIM (optional)

If you've decided to use DKIM, run the tag `install-anonaddy-dkim` after you installed the whole application using `install-all`. Paste the printed DKIM public key in the DKIM DNS record and add the printed value for `anonaddy_dkim_signing_key_path` to your variables as seen in [configure dkim](#dkim-and-rspamd-optional).


### Install GPG (optional)

If you've decided to use GPG, then you should first generate a GPG keypair (on your local system) for the AnonAddy mail address. You should not set a passphase.

```
gpg --full-gen-key

Example:

Please select what kind of key you want:
   (1) RSA and RSA (default)
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
  (14) Existing key from card
Your selection? 1
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (3072) 4096
Requested keysize is 4096 bits
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 0
Key does not expire at all
Is this correct? (y/N) y

GnuPG needs to construct a user ID to identify your key.

Real name: AnonAddy
Email address: anonaddy@anonaddy.example.com
Comment:

...

public and secret key created and signed.

pub   rsa4096 2023-05-30 [SC]
      C3950C727B3846FFB7005FEE3926F5A3BCC2CFF0
uid                      AnonAddy <anonaddy@anonaddy.example.com>
sub   rsa4096 2023-05-30 [E]
```

Find the public key fingerprint (can be found in the output by `pub`). In this example it is `C3950C727B3846FFB7005FEE3926F5A3BCC2CFF0` and should be placed in the `anonaddy_gpg_signing_key_fingerprint` variable as seen in [configure gpg](#gpg-optional).

Export the previously generated private key. The provided key should be installed in the `anonaddy_gpg_signing_key` variable as seen in [configure gpg](#gpg-optional).

```
gpg --armor --export-secret-key anonaddy@anonaddy.example.com
```

## Usage

After installation, you can create an user using by providing the `anonaddy_user_username` and `anonaddy_user_mail` variables to the tag `create-anonaddy-user` 
For example: 
```
just run-tags create-anonaddy-user -e "anonaddy_user_username=test" -e "anonaddy_user_mail=test@test.com"
```
Use the username and printed userid to login at your AnonAddy domain.

