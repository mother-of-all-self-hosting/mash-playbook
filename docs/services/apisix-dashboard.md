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
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# APISIX Dashboard (removed)

🪦 The playbook used to be able to install and configure [APISIX Dashboard](https://apisix.apache.org/docs/dashboard/USER_GUIDE/) as a service of its own, but no longer does, because upstream no longer ships it that way.

The APISIX Dashboard is now a pure front-end which lives **inside the `apache/apisix` container image itself**, first available in APISIX **3.13**. Upstream [has stated](https://github.com/apache/apisix-dashboard/releases/tag/notice) that it will not be released independently again and that there are no plans for further APISIX Dashboard container images.

The last standalone release, 3.0.1, dates from March 2023, and upstream says that it "should and only should be used with APISIX 3.0. Any higher or lower version has not been tested." The playbook installed APISIX 3.8.0 and newer alongside it, which is exactly the untested combination that warning is about. The role which installed it ([ansible-role-apisix-dashboard](https://github.com/mother-of-all-self-hosting/ansible-role-apisix-dashboard)) has been deprecated and archived.

## Migrating to the bundled dashboard

You do not need to install anything. If you run [APISIX Gateway](apisix-gateway.md) at version 3.13 or newer (the playbook is well past that), it is already serving the dashboard — at `/ui/` on its Admin API port.

> [!WARNING]
> The bundled dashboard is served from inside the Admin API's own `server` block, so it shares that listener's port and its `allow_admin` allowlist. **Making the dashboard reachable makes the Admin API reachable**, and while the Admin API requires a key, the dashboard itself is static files with no authentication of its own.
>
> This is a real difference from the standalone APISIX Dashboard, which had its own login page and its own user list. Do not simply point the hostname you used for `apisix_dashboard_hostname` at the Admin API and consider the job done.

See the **Reaching the bundled dashboard** section of the [APISIX Gateway](apisix-gateway.md) documentation for the safe ways to get to it — an SSH tunnel needs no public exposure at all.

## Uninstalling the service manually

The playbook can no longer help you uninstall the standalone APISIX Dashboard, so you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now mash-apisix-dashboard.service

rm -rf /mash/apisix-dashboard
```

If you were [running multiple instances of the APISIX Dashboard service](../running-multiple-instances.md), repeat the commands for each instance's service name and base path.

Your APISIX configuration is not affected. The standalone dashboard stored nothing of its own — it edited the [etcd](etcd.md) database that APISIX Gateway reads, and that database, along with all your routes and upstreams, stays where it is.

## Related services

- [APISIX Gateway](apisix-gateway.md) — An API Gateway and Ingress Controller, which now serves the dashboard itself
- [etcd](etcd.md) — Distributed key-value store, where APISIX keeps its configuration
