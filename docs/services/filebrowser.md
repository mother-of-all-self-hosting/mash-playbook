# Filebrowser

[Filebrowser](https://filebrowser.org) is a self-hosted file managing interface.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# filebrowser                                                          #
#                                                                      #
########################################################################

filebrowser_enabled: true

filebrowser_hostname: filebrowser.example.com

########################################################################
#                                                                      #
# /filebrowser                                                         #
#                                                                      #
########################################################################
```


## Usage

Head over the host and authenticate using `admin` as the user and password. Once authenticated you can modify the user and password.

Configuration can be tricky but most of the configuration can be set using the UI. Read further if you want further customization.

## Configuration

The configuration is managed in the database file, and although the official documentation allows to mount a JSON file, the persistance is kept in the database. See issue [filebrowser/filebrowser#2745](https://github.com/filebrowser/filebrowser/issues/2745).

This means that in order to make further configuration changes in Filebrowser you can use the CLI commands. But given some limitations of the Filebrowser database engine, this cannot be done while the server is running, see issue [filebrowser/filebrowser#2440](https://github.com/filebrowser/filebrowser/issues/2440).

This means that any configuration modification that you may need, needs to be done offline by using the binary, which can be downloaded from the [releases page](https://github.com/filebrowser/filebrowser/releases).

SSH into your server, download the binary and once extracted, stop the Filebrowser service.

```
sudo systemctl stop mash-filebrowser
```

Modify the configuration using a similar command to the following. For more configuration flags go to the [filebrowser config set](https://filebrowser.org/cli/filebrowser-config-set) page.

```
./filebrowser -d /mash/filebrowser/database.db config set --branding.name "M.A.S.H."
```

Finally, start the Filebrowser service again.

```
sudo systemctl start mash-filebrowser
```
