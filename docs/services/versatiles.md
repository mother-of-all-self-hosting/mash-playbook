<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 - 2024 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Versatiles

The playbook can install and configure [Versatiles](https://versatiles.org) for you.

Versatiles is a free stack for generating and serving vector tiles based on [OpenStreetMap](https://openstreetmap.com) data.

See the project's [documentation](https://docs.versatiles.org/) to learn what Versatiles does and why it might be useful to you.

## Dependencies

This service requires the following other services:

- a [Traefik](traefik.md) reverse-proxy server

## Adjusting the playbook configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# versatiles                                                           #
#                                                                      #
########################################################################

versatiles_enabled: true

versatiles_hostname: tiles.example.com

########################################################################
#                                                                      #
# /versatiles                                                          #
#                                                                      #
########################################################################
```

## Usage

After running the command for installation, Versatiles becomes available at the specified hostname like `https://tiles.example.com`.

![Map of Dresden](../assets/versatiles/map-example.jpeg)

To embed the map on a website, add the following tags to the website:

```html
<!-- add MapLibre JavaScript and CSS -->
<script src="https://tiles.example.com/assets/lib/maplibre-gl/maplibre-gl.js"></script>
<link href="https://tiles.example.com/assets/lib/maplibre-gl/maplibre-gl.css" rel="stylesheet" />

<!-- add container for the map -->
<div id="map" style="width:100%;aspect-ratio:16/9"></div>

<!-- start map -->
<script>
  new maplibregl.Map({
    container: 'map',
    style: 'https://tiles.example.com/assets/styles/colorful.json'
  }).addControl(new maplibregl.NavigationControl());
</script>
```

Refer to [examples from MapLibre](https://maplibre.org/maplibre-gl-js/docs/examples/) for details about adjustments.
