# Maintenance and Troubleshooting

## How to see the current status of your services

You can check the status of your services by using `systemctl status`. Example:
```
sudo systemctl status mash-miniflux

● mash-miniflux.service - Miniflux (mash-miniflux)
   Loaded: loaded (/etc/systemd/system/mash-miniflux.service; enabled; vendor preset: disabled)
   Active: active (running) since Tue 2023-03-14 17:41:59 EET; 15h ago
```

You can see the logs by using journalctl. Example:
```
sudo journalctl -fu mash-miniflux
```


## Increasing logging

Various Ansible roles for various services supported by this playbook support a `*_log_level` variable or some debug mode which you can enable in your configuration and get extended logs.

[Re-run the playbook](installing.md) after making such  configuration changes.


## Remove unused Docker data

You can free some disk space from Docker by running `docker system prune -a` on the server.


## Postgres

See the dedicated [PostgreSQL Maintenance](services/postgres.md#maintenance) documentation page.
