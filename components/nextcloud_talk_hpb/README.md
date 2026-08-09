<!--
SPDX-FileCopyrightText: 2026 MASH project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Nextcloud Talk High-Performance Backend (HPB)

The playbook can install and configure the [Nextcloud Talk High-Performance Backend (HPB)](https://github.com/nextcloud/talk-hpb) for you.

Nextcloud Talk HPB is a high-performance backend for Nextcloud Talk that provides WebRTC signaling, Janus WebRTC gateway, and NATS message broker services. It enables high-quality real-time communication for Nextcloud Talk.

See the project's [documentation](https://github.com/nextcloud/talk-hpb) to learn what HPB does and why it might be useful to you.

For details about configuring the [Ansible role for Nextcloud Talk HPB](https://forgejo.littlecedar.net/littlecedar/ansible-role-mash-nextcloud-talk-hpb), you can check them via:

- 🌐 [the role's documentation](https://forgejo.littlecedar.net/littlecedar/ansible-role-mash-nextcloud-talk-hpb) online
- 📁 `roles/galaxy/nextcloud-talk-hpb/` locally, if you have [fetched the Ansible roles](../installing.md)

## Dependencies

This service requires the following other services:

- [Nextcloud](nextcloud.md) — for Talk integration
- [Docker](docker.md) — container runtime
- [Traefik](traefik.md) reverse-proxy server (for exposing the signaling server)
- (optional) [coTURN](https://github.com/coturn/coturn) for WebRTC STUN/TURN server

## Architecture

Nextcloud Talk HPB consists of 4 separate systemd services:

1. **mash-nextcloud-talk-hpb** (main): Nextcloud Talk signaling server
2. **mash-nextcloud-talk-hpb-signaling**: Signaling component (exposed via Traefik)
3. **mash-nextcloud-talk-hpb-janus**: Janus WebRTC gateway (MCU)
4. **mash-nextcloud-talk-hpb-nats**: NATS message broker (internal communication)

## Configuration

To enable this service, add the following configuration to your `vars.yml` file:

```yaml
# Enable Nextcloud first
nextcloud_enabled: true

# Enable HPB
nextcloud_talk_hpb_enabled: true

# Configure signaling hostname
nextcloud_talk_hpb_signaling_hostname: talk.example.com
```

### Basic Configuration

The following variables control the basic HPB configuration:

```yaml
# Master toggle for the whole role
nextcloud_talk_hpb_enabled: true

# Base configuration
nextcloud_talk_hpb_identifier: "{{ mash_playbook_service_identifier_prefix }}nextcloud_talk_hpb"
nextcloud_talk_hpb_base_path: "{{ mash_playbook_base_path }}/{{ mash_playbook_service_base_directory_name_prefix }}nextcloud_talk_hpb"
nextcloud_talk_hpb_uid: "{{ mash_playbook_uid }}"
nextcloud_talk_hpb_gid: "{{ mash_playbook_gid }}"
```

### Signaling Server Configuration

```yaml
# Signaling server configuration
nextcloud_talk_hpb_signaling_enabled: "{{ nextcloud_talk_hpb_enabled }}"
nextcloud_talk_hpb_signaling_identifier: "{{ nextcloud_talk_hpb_identifier }}-signaling"
nextcloud_talk_hpb_signaling_base_path: "{{ nextcloud_talk_hpb_base_path }}/signaling"
nextcloud_talk_hpb_signaling_hostname: talk.example.com
nextcloud_talk_hpb_signaling_http_port: 8080
nextcloud_talk_hpb_signaling_sessions_hash_key: "{{ (mash_playbook_generic_secret_key + ':nextcloud_talk_hpb.sessions') | hash('sha512') | to_uuid }}"
```

### Janus Configuration

```yaml
# Janus configuration
nextcloud_talk_hpb_janus_enabled: "{{ nextcloud_talk_hpb_enabled }}"
nextcloud_talk_hpb_janus_identifier: "{{ nextcloud_talk_hpb_identifier }}-janus"
nextcloud_talk_hpb_janus_base_path: "{{ nextcloud_talk_hpb_base_path }}/janus"
nextcloud_talk_hpb_janus_stun_server: ""
nextcloud_talk_hpb_janus_stun_port: 3478
```

### NATS Configuration

```yaml
# NATS configuration
nextcloud_talk_hpb_nats_enabled: "{{ nextcloud_talk_hpb_enabled }}"
nextcloud_talk_hpb_nats_identifier: "{{ nextcloud_talk_hpb_identifier }}-nats"
nextcloud_talk_hpb_nats_base_path: "{{ nextcloud_talk_hpb_base_path }}/nats"
nextcloud_talk_hpb_nats_port: 4222
nextcloud_talk_hpb_nats_log_level: warn
```

### Nextcloud Integration

```yaml
# Nextcloud integration (optional but recommended)
nextcloud_talk_hpb_nextcloud_enabled: "{{ nextcloud_enabled }}"
nextcloud_talk_hpb_nextcloud_url: "{{ nextcloud_scheme }}://{{ nextcloud_hostname }}{{ nextcloud_path_prefix }}"
nextcloud_talk_hpb_nextcloud_secret: "{{ (mash_playbook_generic_secret_key + ':nextcloud_talk_hpb.nextcloud') | hash('sha512') | to_uuid }}"
```

### Full Configuration with coTURN

```yaml
nextcloud_enabled: true
coturn_enabled: true
traefik_enabled: true

nextcloud_talk_hpb_enabled: true
nextcloud_talk_hpb_signaling_hostname: talk.example.com
nextcloud_talk_hpb_signaling_sessions_hash_key: "{{ (mash_playbook_generic_secret_key + ':nextcloud_talk_hpb.sessions') | hash('sha512') | to_uuid }}"

# Janus with STUN/TURN
nextcloud_talk_hpb_janus_stun_server: "{{ coturn_public_hostname }}"
nextcloud_talk_hpb_janus_stun_port: 5349
```

## Tags Available

The role provides these tags:
- `setup-mash-nextcloud-talk-hpb`
- `setup-all`
- `install-mash-nextcloud-talk-hpb`
- `install-all`

## Installation Commands

```bash
# Install with HPB
just install nextcloud-talk-hpb

# Install without tags (auto-detects enabled services)
just install

# Using tags
just setup setup-nextcloud-talk-hpb
just install install-nextcloud-talk-hpb

# Check status
just status nextcloud-talk-hpb
```

## Validation Steps

After installation, verify:

```bash
# Check all services are running
systemctl status mash-nextcloud-talk-hpb.service
systemctl status mash-nextcloud-talk-hpb-signaling.service
systemctl status mash-nextcloud-talk-hpb-janus.service
systemctl status mash-nextcloud-talk-hpb-nats.service

# Check Docker containers
docker ps | grep mash-nextcloud-talk-hpb

# Verify Traefik routing
curl -I https://talk.example.com
```

## Nextcloud Configuration

In Nextcloud Admin → Talk → Advanced settings:

```
Turn server: turn:talk.example.com:443?transport=udp
Turn server: turn:talk.example.com:443?transport=tcp
STUN server: stun:talk.example.com:443
```

## Security Considerations

1. The signaling server is exposed to the internet - ensure Traefik TLS is configured
2. Use `nextcloud_talk_hpb_signaling_sessions_hash_key` for session security
3. Configure coTURN for WebRTC media relay (not direct port exposure)
4. Keep all container images updated
5. Monitor logs for suspicious activity

## Troubleshooting

Common issues:

1. **Services not starting**: Check Docker is running, verify configuration
2. **Traefik not routing**: Verify `nextcloud_talk_hpb_signaling_hostname` is DNS-resolvable
3. **Janus RTP issues**: Configure coTURN STUN/TURN properly
4. **Nextcloud can't connect**: Verify `nextcloud_talk_hpb_nextcloud_secret` matches

## Migration from Standalone HPB

If migrating from a standalone HPB installation:

1. Stop existing HPB services
2. Backup configuration and data
3. Run playbook with `nextcloud_talk_hpb_enabled: true`
4. Update Nextcloud Talk configuration
5. Verify functionality
6. Remove old standalone installation
