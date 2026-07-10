<!--
SPDX-FileCopyrightText: 2026 Oliver Lorenz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# app-dooropener Ansible role

This is an [Ansible](https://www.ansible.com/) role which installs the [Dooropener PWA](https://github.com/oliverlorenz/app-dooropener) to run as a [Docker](https://www.docker.com/) container wrapped in a systemd service.

This role *implicitly* depends on:

- [`com.devture.ansible.role.playbook_help`](https://github.com/devture/com.devture.ansible.role.playbook_help)
- [`com.devture.ansible.role.systemd_docker_base`](https://github.com/devture/com.devture.ansible.role.systemd_docker_base)

Check [defaults/main.yml](defaults/main.yml) for the full list of supported options.

## Configuration

At minimum you need to set:

- `app_dooropener_hostname` — the hostname the PWA is served at
- `app_dooropener_config_home_assistant_base_url` — the HomeAssistant base URL (e.g. `https://api.example.com`)
- `app_dooropener_environment_homeassistant_token` — a HomeAssistant long-lived access token
- `app_dooropener_config_doors` — the list of doors, scripts and time-boxed PINs (see the example in [defaults/main.yml](defaults/main.yml))

`app_dooropener_environment_homeassistant_token` and `app_dooropener_config_doors` contain secrets, so define them in an ansible-vault-encrypted file (e.g. `inventory/host_vars/<server>/vault.yml`), not in plain `group_vars`.

The doors/PINs are rendered into `config.json` and bind-mounted read-only into the container. To rotate PINs, update `app_dooropener_config_doors` and re-run the playbook (`just setup-service app-dooropener <server>` or similar) — no image rebuild is required, only a container restart.
