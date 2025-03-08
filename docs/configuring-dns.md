<!--
SPDX-FileCopyrightText: 2018 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring DNS settings

<sup>[Prerequisites](prerequisites.md) > Configuring DNS settings > [Getting the playbook](getting-the-playbook.md) > [Configuring the playbook](configuring-playbook.md) > [Installing](installing.md)</sup>

To reach your services, you'd need to do some DNS configuration.

**We recommend** that you:

- create at least one generic domain (e.g. `mash.example.com`) for easily hosting various services at different subpaths (e.g. `mash.example.com/miniflux`, `mash.example.com/radicale`, etc.). Even if you plan on hosting services at a dedicated subdomain, it's still convenient to have a generic domain and to use additional `CNAME` DNS records that point to it.

- create additional domains (`CNAME` DNS records pointing to the main generic domain) for large services or services that explicitly require their own dedicated domain

Some services (like [Uptime-kuma](services/uptime-kuma.md)) require being hosted at their own dedicated domain. Others, you can put on their own domain/subdomain or at subpaths on any domain you'd like.

## Example DNS settings

As an example setup, adjust DNS records as below.

| Service                    | Type  | Host    | Priority | Weight | Port | Target             |
|--------------------------- | ----- | ------- | -------- | ------ | ---- | -------------------|
| Miniflux, Radicale, others | A     | `mash`  | -        | -      | -    | `mash-server-IPv4` |
| Miniflux, Radicale, others | AAAA  | `mash`  | -        | -      | -    | `mash-server-IPv6` |
| Nextcloud                  | CNAME | `cloud` | -        | -      | -    | `mash.example.com` |

If you don't have IPv6 connectivity yet, you can skip the `AAAA` record. For more details about IPv6, see the [Configuring IPv6](./configuring-ipv6.md) documentation page.

With such a setup, you could reach:

- the feedreader [Miniflux](services/miniflux.md) at `https://mash.example.com/miniflux` (if you set `miniflux_hostname: mash.example.com` and `miniflux_path_prefix: /miniflux` in your `vars.yml`)

- the [Radicale](services/radicale.md) CalDAV/CardDAV sever at `https://mash.example.com/radicale` (if you set `radicale_hostname: mash.example.com` and `radicale_path_prefix: /radicale` in your `vars.yml`)

- Nextcloud at its own dedicated domain, at `https://cloud.example.com`

Hosting services at subpaths is more convenient, because it doesn't require you to create additional DNS records and no new SSL certificates need to be retrieved.

Still, if you'd like each service to have its own dedicated domain (or subdomain), feel free to configure services that way by making sure that you set `<service>_hostname` and `<service>_path_prefix` accordingly in your `vars.yml`.

Be mindful as to how long it will take for the DNS records to propagate.

**Note**: if you are using Cloudflare DNS, make sure to disable the proxy and set all records to "DNS only". Otherwise, fetching certificates will fail.

---------------------------------------------

[▶️](getting-the-playbook.md) When you're done with the DNS configuration and ready to proceed, continue with [Getting the playbook](getting-the-playbook.md).
