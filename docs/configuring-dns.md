<!--
SPDX-FileCopyrightText: 2018 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring DNS settings

<sup>[Prerequisites](prerequisites.md) > Configuring DNS settings > [Getting the playbook](getting-the-playbook.md) > [Configuring the playbook](configuring-playbook.md) > [Installing](installing.md)</sup>

To make your services accessible, you need to configure DNS records.

**We recommend:**

- Creating at least one generic domain (e.g. `mash.example.com`) for hosting various services at different subpaths (e.g. `mash.example.com/miniflux`, `mash.example.com/radicale`, etc.). Even if you plan to host services at dedicated subdomains, it's convenient to have a generic domain and use additional `CNAME` DNS records pointing to it.
- Creating additional domains (`CNAME` DNS records pointing to the main generic domain) for large services or those that explicitly require their own dedicated domain.

Some services (like [Uptime Kuma](services/uptime-kuma.md)) require a dedicated domain. Others can be hosted on their own domain/subdomain or at subpaths on any domain you choose.

## Example DNS settings

As an example, adjust your DNS records as shown below:

| Service                    | Type  | Host    | Priority | Weight | Port | Target             |
|----------------------------|-------|---------|----------|--------|------|--------------------|
| Miniflux, Radicale, others | A     | `mash`  | -        | -      | -    | `mash-server-IPv4` |
| Miniflux, Radicale, others | AAAA  | `mash`  | -        | -      | -    | `mash-server-IPv6` |
| Nextcloud                  | CNAME | `cloud` | -        | -      | -    | `mash.example.com` |

If you don't have IPv6 connectivity, you can skip the `AAAA` record. For more details about IPv6, see the [Configuring IPv6](./configuring-ipv6.md) documentation page.

With this setup, you could reach:

- The feedreader [Miniflux](services/miniflux.md) at `https://mash.example.com/miniflux` (if you set `miniflux_hostname: mash.example.com` and `miniflux_path_prefix: /miniflux` in your `vars.yml`)
- The [Radicale](services/radicale.md) CalDAV/CardDAV server at `https://mash.example.com/radicale` (if you set `radicale_hostname: mash.example.com` and `radicale_path_prefix: /radicale` in your `vars.yml`)
- Nextcloud at its own dedicated domain, `https://cloud.example.com`

Hosting services at subpaths is often more convenient, as it doesn't require creating additional DNS records or retrieving new SSL certificates.

If you prefer each service to have its own dedicated domain (or subdomain), configure services accordingly by setting `<service>_hostname` and `<service>_path_prefix` in your `vars.yml`.

Be mindful of DNS propagation time.

**Note:** If you are using Cloudflare DNS, make sure to disable the proxy and set all records to "DNS only". Otherwise, certificate fetching will fail.

---

[▶️](getting-the-playbook.md) When you're done with DNS configuration and ready to proceed, continue with [Getting the playbook](getting-the-playbook.md).
