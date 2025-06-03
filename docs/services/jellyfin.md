# Jellyfin

[Jellyfin](https://jellyfin.org/) is an open-source personal media server that allows you to organize and stream your collection of movies, TV shows, and music.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# jellyfin                                                             #
#                                                                      #
########################################################################

jellyfin_enabled: true
jellyfin_hostname: jellyfin.example.com
jellyfin_container_additional_volumes:
  - type: bind
    src: /path/on/the/host/movies
    dst: /movies

  - type: bind
    src: /another-path/on/the/host/anime
    dst: /anime
    options: readonly

########################################################################
#                                                                      #
# /jellyfin                                                            #
#                                                                      #
########################################################################
```

## Security Notice

Unlike most MASH services, this service **runs with root privileges** and requires **read-write filesystem access** due to [upstream requirements](https://github.com/linuxserver/docker-jellyfin). These exceptions represent a deviation from our standard security practices. The container remains reasonably secure, but users should be aware of this modified security posture when deploying this service. We actively monitor upstream changes and will implement improved security configurations as soon as the Jellyfin container image supports non-root execution and read-only operations.

## Usage

After [installation](../installing.md), you should access your new Jellyfin instance at the URL you've chosen and create a username and password:

![Jellyfin Configure User](../assets/jellyfin/setup-1.png)

When prompted to add your media libraries keep in mind that it will be the path **inside** the container, most likely the `dst` parameter of your `jellyfin_container_additional_volumes` variable.

### Configuring DLNA & Local discovery

By default your Jellyfin instance cannot be connected to directly, and must be routed through Traefik (usually with HTTPS). This works fine for the web-app, phone, and TV apps. However, depending on your setup, you may want to connect directly to your server on the LAN with no HTTPS.

Keep in mind that doing so will send your Jellyfin password across the network in plain-text. This is not a recommended configuration. That said, here is how:

```yaml
# The main Jellyfin webserver port, setting this variable will expose that port and allow you to connect directly to it (without Traefik).
jellyfin_container_http_bind_port: 8096

# The Jellyfin DLNA server, used for clients to discover Jellyfin on the LAN
jellyfin_container_service_discover_bind_port: 1900

# Another service related to discovering Jellyfin on the LAN.
# From the docs:
# "Allows clients to discover Jellyfin on the local network. A broadcast message to this port with 'Who is JellyfinServer?' will get a JSON response that includes the server address, ID, and name."
jellyfin_container_client_discover_bind_port: 7359

# The server address the client discovery service should respond with
jellyfin_published_server_url: "http://{{ ansible_default_ipv4.address }}:{{ jellyfin_container_http_bind_port }}"
```
Upstream documentation: https://jellyfin.org/docs/general/post-install/networking/

After setting these variables you should be able to discover and connect to your Jellyfin server entirely on the LAN. If for some reason it is still not discoverable try inputting your `jellyfin_published_server_url` manually.

### Hardware Acceleration

To enable hardware acceleration you'll first need to determine your GPU brand. Once you've done this, read the corresponding section below:

#### Intel/ATI/AMD

For Intel/ATI/AMD GPUs enabling hardware acceleration is as easy as mounting the device into the container:

```yaml
# The path where the Intel/ATI/AMD GPU is on the host system
jellyfin_gpu_path: "/dev/dri"

# The path to mount the Intel/ATI/AMD GPU to in the container.
# Takes a path value (e.g. "/dev/dri"), or empty string to not mount.
jellyfin_gpu_bind_path: "{{ jellyfin_gpu_path }}"
```

Upstream documentation: https://github.com/linuxserver/docker-jellyfin#intelatiamd

#### NVIDIA

For NVIDIA GPUs enabling hardware acceleration is a little bit tricky since it (currently) requires the manual installation of the [NVIDIA container runtime](https://github.com/NVIDIA/nvidia-container-toolkit). Consult your distribution's documentation on installing this.

Once the runtime is installed and available, add the following configuration:

```yaml
# The container runtime that the container engine should use
jellyfin_container_runtime: "nvidia"

# To enable NVIDIA GPU hardware acceleration this value should either be 'all' or the UUID value of the GPU
# which can obtained with the command -> 'nvidia-smi --query-gpu=gpu_name,gpu_uuid --format=csv'
jellyfin_nvidia_visible_devices: "all"
```

Upstream documentation: https://github.com/linuxserver/docker-jellyfin#nvidia

## Recommended other services

Consider these other related services:

- [Radarr](radarr.md)
- [Sonarr](sonarr.md)
- [Jackett](jackett.md)
- [qBittorrent](qbittorrent.md)
- [Overseerr](overseerr.md)
- [Plex](plex.md)
