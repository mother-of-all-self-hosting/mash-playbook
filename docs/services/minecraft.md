<!--
SPDX-FileCopyrightText: 2025 XHawk87
SPDX-FileCopyrightText: 2025 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Minecraft

[Minecraft](https://docker-minecraft-server.readthedocs.io) is a first-person open-world procedurally-generated voxel-based sandbox game with RPG elements.

> [!WARNING]
> itzg docker-minecraft server is published under the Apache-2.0 license, however Minecraft itself is proprietary software, and by using this role you are agreeing to the [EULA](https://www.minecraft.net/en-us/eula). Know your rights!


## Dependencies

This service currently requires no other services.


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# minecraft                                                            #
#                                                                      #
########################################################################

minecraft_enabled: true

minecraft_bind_port: 25565

minecraft_environment_variables_additional: |
  MOTD=[Your Server Name Here]
  TYPE=PAPER
  VERSION=latest
  INIT_MEMORY=500M
  MAX_MEMORY=2G
  USE_AIKAR_FLAGS=true
  STOP_SERVER_ANNOUNCE_DELAY=10
  TZ=Europe/London
  LOG_TIMESTAMP=true
  DIFFICULTY=hard
  ENABLE_WHITELIST=true
  ENFORCE_WHITELIST=true
  WHITELIST=[Your Minecraft IGN Here]
  ENABLE_QUERY=false
  MAX_PLAYERS=20
  ENABLE_COMMAND_BLOCK=true
  SNOOPER_ENABLED=false
  SPAWN_PROTECTION=0
  VIEW_DISTANCE=16
  PVP=true
  ALLOW_FLIGHT=TRUE
  SIMULATION_DISTANCE=16
  PLAYER_IDLE_TIMEOUT=0
  INITIAL_ENABLED_PACKS=vanilla,bundle

########################################################################
#                                                                      #
# /minecraft                                                           #
#                                                                      #
########################################################################
```

In the example configuration above, we configure the server to be hosted on port `25565` on all network interfaces. Port forwarding will be required to access it. It will be the "latest" pinned version of [Paper minecraft server](https://papermc.io/), limited to 2GB of RAM, hard difficulty, only you on the whitelist, rather generous render distance, PvP, and bundles.

See the full set of available [Environment Variables](https://docker-minecraft-server.readthedocs.io/en/latest/variables/) to configure the server.


## Usage

After installation, you can use your Minecraft client to log into the game.

If you need to access the server console, you can do so via RCON:

```bash
ssh -t [Your MC server hostname] \
    sudo docker exec -it mash-minecraft \
        rcon-cli
```

You can then give yourself Operator status, or perform any other MC commands you wish.
