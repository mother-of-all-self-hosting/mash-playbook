<!--
SPDX-FileCopyrightText: 2019 Edgars Voroboks
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2019-2025 MDAD project contributors
SPDX-FileCopyrightText: 2019-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Dominik Zajac
SPDX-FileCopyrightText: 2020 Mickaël Cornière
SPDX-FileCopyrightText: 2020 Tulir Asokan
SPDX-FileCopyrightText: 2020 jens quade
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Kim Brose
SPDX-FileCopyrightText: 2022 Travis Ralston
SPDX-FileCopyrightText: 2022 Vladimir Panteleev
SPDX-FileCopyrightText: 2022 Warren Bailey
SPDX-FileCopyrightText: 2022 Yan Minagawa
SPDX-FileCopyrightText: 2023 Antonis Christofides
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2023 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2025 Nicola Murino

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Firezone (removed)

🪦 The playbook used to be able to install and configure the legacy 0.7 version of [Firezone](https://www.firezone.dev/), but no longer includes this service, as the role to install it ([ansible-role-firezone](https://github.com/mother-of-all-self-hosting/ansible-role-firezone)) has been deprecated.

>[!NOTE]
> You might be interested in having a look at [WireGuard Easy](wg-easy.md).

## Uninstalling the service manually

If you still have Firezone installed on your server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now mash-firezone.service

rm -rf /mash/firezone

/mash/postgres/bin/cli-non-interactive -c 'DROP DATABASE firezone;'
```
