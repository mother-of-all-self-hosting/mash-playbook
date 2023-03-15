# Uninstalling

**Warning**: If you have some trouble with your installation, you can just [re-run the playbook](installing.md) and it will try to set things up again. **Uninstalling and then installing anew rarely solves anything**.

To uninstall, run these commands (most are meant to be executed on the server itself):

- ensure all services are stopped: `just stop` (if you can't get Ansible working to run this command, you can run `systemctl stop 'mash-*'` manually on the server)

- delete the systemd `.service` and `.timer` files (`rm -f /etc/systemd/system/mash-*.{service,timer}`) and reload systemd (`systemctl daemon-reload`)

- delete some cached Docker images (`docker system prune -a`) or just delete them all (`docker rmi $(docker images -aq)`)

- uninstall Docker itself, if necessary

- delete the `/mash` directory (`rm -rf /mash`)


