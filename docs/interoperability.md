# Configuring interoperability with other services

This playbook tries to get you up and running with minimal effort and provided you have followed the [example `vars.yml` file](../examples/vars.yml), will install the [Traefik](services/traefik.md) reverse-proxy server by default.

Sometimes, you're using a server which already has Traefik. In such cases these are undesirable:

- the playbook trying to run its own Traefik instance and running into a conflict with your other Traefik instance over ports (`tcp/80` and `tcp/443`)

- multiple playbooks trying to install Docker, etc.

Below, we offer some suggestions for how to make this playbook more interoperable. Feel free to cherry-pick the parts that make sense for your setup.


## Disabling Traefik installation

If you're installing [Traefik](services/traefik.md) on your server in another way, you can use your already installed Traefik instance and [disable the Traefik instance installed by MASH](services/traefik.md#using-another-traefik-instance-not-installing-traefik).

If you are using the [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy) playbook, it already runs its own Traefik instance (`matrix-traefik`). We recommend that you [disable the Traefik instance installed by MASH](services/traefik.md#using-another-traefik-instance-not-installing-traefik), because the Traefik instance installed by the Matrix playbook does the same, but also contains additional configuration for handling the Matrix federation port (`8448`).


## Disabling Docker installation

If you're installing [Docker](https://www.docker.com/) on your server in another way, disable this component from the playbook:

```yaml
mash_playbook_docker_installation_enabled: false
```


## Disabling timesyncing (systemd-timesyncd / ntp) installation

If you're installing `systemd-timesyncd` or `ntp` on your server in another way, disable this component from the playbook:

```yaml
devture_timesync_installation_enabled: false
```
