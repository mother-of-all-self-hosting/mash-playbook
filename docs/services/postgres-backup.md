# Postgres Backup

This playbook can configure [docker-postgres-backup-local](https://github.com/prodrigestivill/docker-postgres-backup-local) for you via the [com.devture.ansible.role.postgres_backup](https://github.com/devture/com.devture.ansible.role.postgres_backup) Ansible role.

For a more complete backup solution (one that includes not only Postgres, but also other configuration/data files), you may wish to look into [borg backup](backup-borg.md).


## Configuration

To enable this service, add the following configuration to your `vars.yml` file and re-run the [installation](../installing.md) process:

```yaml
########################################################################
#                                                                      #
# devture-postgres-backup                                              #
#                                                                      #
########################################################################

devture_postgres_backup_enabled: true

########################################################################
#                                                                      #
# /devture-postgres-backup                                             #
#                                                                      #
########################################################################
```

Refer to the table below for additional configuration variables and their default values.


| Name                              | Default value                | Description                                                      |
| :-------------------------------- | :--------------------------- | :--------------------------------------------------------------- |
|`devture_postgres_backup_enabled`|`false`|Set to true to use [docker-postgres-backup-local](https://github.com/prodrigestivill/docker-postgres-backup-local) to create automatic database backups|
|`devture_postgres_backup_schedule`| `'@daily'` |Cron-schedule specifying the interval between postgres backups.|
|`devture_postgres_backup_keep_days`|`7`|Number of daily backups to keep|
|`devture_postgres_backup_keep_weeks`|`4`|Number of weekly backups to keep|
|`devture_postgres_backup_keep_months`|`12`|Number of monthly backups to keep|
|`devture_postgres_backup_base_path` | `"{{ mash_playbook_base_path }}/postgres-backup"` | Base path for postgres-backup. Also see `devture_postgres_backup_data_path` |
|`devture_postgres_backup_data_path` | `"{{ devture_postgres_backup_base_path }}/data"` | Storage path for postgres-backup database backups |
