# Greenbone

Vulnerability scanner using Greenbone Community Edition.

The role defaults to off (`greenbone_enabled: false`). The live stack this role adopts uses Compose project `greenbone-community-edition`, directory `/opt/siem/greenbone`, and host port 9443. Set `greenbone_base_path` for that host before turning the role on.

The role copies `compose.yaml` only when that file is missing. It does not delete volumes. Feed data is refreshed by the host timer `greenbone-feed-sync.timer` at 03:15.
