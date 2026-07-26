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
- `app_dooropener_environment_admin_password_hash` — scrypt hash protecting the admin PIN-management UI at `/admin`; generate it in the app repo with `npm run admin:hash-password` (never store the plaintext password)
- `app_dooropener_environment_admin_session_secret` — random secret used to sign the admin session cookie, e.g. `openssl rand -hex 32`
- `app_dooropener_config_doors` — the **initial seed** for the list of doors, scripts and time-boxed PINs (see the example in [defaults/main.yml](defaults/main.yml))

`app_dooropener_environment_homeassistant_token`, `app_dooropener_environment_admin_password_hash`, `app_dooropener_environment_admin_session_secret` and `app_dooropener_config_doors` contain secrets, so define them in an ansible-vault-encrypted file (e.g. `inventory/host_vars/<server>/vault.yml`), not in plain `group_vars`.

`config.json` (doors/PINs) lives in its own `config/` subdirectory on the host
(`{{ app_dooropener_base_path }}/config/config.json`), and that whole *directory* —
not just the file — is bind-mounted **writable** into the container at
`app_dooropener_container_config_dir` (`/config` by default). This is required
because the admin UI at `/admin` persists PIN changes at runtime via an atomic
temp-file-plus-rename, which needs write access to the containing directory, not
just the file itself; mounting only the file (as older versions of this role did)
fails with `EACCES` once the app tries to write. Because of this,
`app_dooropener_config_doors` only *seeds* `config.json` the first time the role
runs (`tasks/install.yml` uses `force: false`) — the playbook never overwrites an
existing `config.json` again, so it won't clobber admin-made changes. To reset
back to the seed value, delete `config.json` on the host and re-run the playbook.
