<!--
SPDX-FileCopyrightText: 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up services on the Matrix server configured with the MDAD playbook

If you use the [matrix-docker-ansible-deploy (MDAD)](https://github.com/spantaleev/matrix-docker-ansible-deploy/) Ansible playbook to manage [Matrix](https://matrix.org/) services on your server, you can configure the MASH playbook to set up services such as [Forgejo](services/forgejo.md), [GoToSocial](services/gotosocial.md), [Nextcloud](services/nextcloud.md), [PeerTube](services/peertube.md) and tons of other [supported services](./supported-services.md), along with the Matrix services on the same server. This page explains how to do so.

The basic steps to configure the MASH playbook and use it to install services are pretty same as doing so with the MDAD playbook: **setting up prerequisites (if running this playbook on a different computer), retrieving the MASH playbook, configuring it as well as the DNS records, and installing the services on the server**. If you have been accustomed to maintain Matrix services with the MDAD playbook, it should not be difficult to set up and use this playbook too.

💡 This article intends to be a guide for setting up the MASH playbook to install services on your Matrix server. If you want to know exact steps from setting up the prerequisites to running the installation command, please go to [this page](prerequisites.md) and read through the installation guide.

## Set up prerequisites

Most [prerequisites](prerequisites.md) for the MASH playbook are common to the MDAD playbook (you can check ones for the MDAD playbook [here](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/prerequisites.md)), so it is not likely that you would need to configure something special to run the MASH playbook.

Depending on the services to enable, you might have to open ports of the server. Consult each service's documentation page in `docs/` for details. By default, you do not have to open them by yourself.

For the local environment, please make sure that you have installed and configured prerequisites such as [Ansible](ansible.md), if you run the MASH playbook on a different computer than the one you run the MDAD playbook.

## Retrieve the MASH playbook

While it is technically not impossible to integrate the roles used by the MASH playbook to the MDAD playbook, you can just retrieve the MASH playbook and run it against the same server. This way is straightforward and recommended for most cases.

See [this page](getting-the-playbook.md) for details about how to get the playbook's source code. In the same way as for the MDAD playbook, you can retrieve the playbook with git or by downloading its ZIP archive.

## Configure DNS settings

After making sure that you have configured prerequisites and retrieving the MASH playbook, let's configure DNS records for the services which you are installing with this playbook.

To configure them, go to your DNS service provider, and adjust DNS records as described [here](configuring-dns.md).

If you are adding the common `mash.example.com` domain, set the same IP address as the Matrix server (e.g. `matrix.example.com`) to its A record.

💡 As [Uptime Kuma](services/uptime-kuma.md), which needs its subdomain for now, will be enabled by default with the sample configuration file, you can go ahead and set its CNAME record in advance. The record should match with `uptime_kuma_hostname`, which will be specified when configuring `vars.yml` file next. If you will not enable the service, you do not have to add the CNAME record, of course.

## Configure the MASH playbook

Next, you'll need to copy the sample inventory hosts file ([`hosts`](../examples/hosts)) and configuration file ([`vars.yml`](../examples/mash-for-matrix-docker-ansible-deploy-users/vars.yml)) modified for installing services on your Matrix server.

To do so, run the following commands inside the playbook directory. Before creating a directory, make sure to replace `mash.example.com` with your domain. Here `example.com` should be the same one where the Matrix server is hosted.

```sh
mkdir -p inventory/host_vars/mash.example.com

cp examples/hosts inventory/hosts

cp examples/mash-for-matrix-docker-ansible-deploy-users/vars.yml inventory/host_vars/mash.example.com/vars.yml
```

### Configure `hosts` file

After copying the files, let's edit your `hosts` file.

Because you are running the playbook against the same server where the Matrix services run, you can just copy the server's external IP address specified on `hosts` file on the MDAD playbook.

If you have edited the MDAD's `hosts` file on your preference (such as adjusting the SSH port), you might probably want to copy the entire line and replace the domain with the one for this playbook such as `mash.example.com`. This should work for most case, as you should have already connected to your Matrix server with such preference.

### Configure `vars.yml` file

Having edited the `hosts` file, you need to edit the `vars.yml` file by setting passwords, etc. Check the comments on the file for details about how to configure it.

Note that `example.com` is specified as hostname values for services enabled by default such as [exim-relay](services/exim-relay.md), [Uptime Kuma](services/uptime-kuma.md), etc., so do not forget to replace them with your domain.

💡 The modified sample `vars.yml` file is not configured to install basic services such as [Docker](services/docker.md) and [Traefik](services/traefik.md), as both have been installed and configured on your Matrix server with the MDAD playbook. Installing them with this playbook will cause conflicts on the server. You can check [this page on interoperability](interoperability.md) for more information.

## Install services by running the MASH playbook

After configuring the playbook, you can proceed to installing the services.

The step for installation is common to both MASH and MDAD playbooks (ie. fetching the Ansible roles and running the installation command), so there should not be a problem. If you do not feel confident pretty much, please see [this page](installing.md) to make sure what needs to be done.

You can see [this page](supported-services.md) for a full list of the supported services and pick services which you want to install. When enabling a service, please check its documentation for the instruction.

If you want to install services, you can do so whenever you want by running the playbook. However, it is generally not recommended to install a lot of services all at once, since it can overflow the server, which can already be suffering from heavy load of [Synapse](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/configuring-playbook-synapse.md), its de-facto Matrix homeserver.

After running the installation command, make sure to check the installed services can be accessed. **If you can access to them, the installation has completed and you can use the services along with the Matrix services**🎉

See [this section](installing.md#things-to-do-next) for details about what to do after successful installation. The MASH playbook, like the MDAD playbook, will **not** automatically run the maintenance task for you, so do not forget to update the playbook and re-run it **manually**.
