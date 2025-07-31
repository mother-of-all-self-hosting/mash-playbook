
# Uninstalling

> [!WARNING]
> If you have trouble with your installation, you can [re-run the playbook](installing.md) and it will try to set things up again. **Uninstalling and then reinstalling rarely solves anything**.

To uninstall, run these commands (most are meant to be executed on the server itself):

- Ensure all services are stopped: `just stop-all` (if you can't get Ansible working to run this command, you can run `systemctl stop 'mash-*'` manually on the server)
- Delete the systemd `.service` and `.timer` files:
	```sh
	rm -f /etc/systemd/system/mash-*.{service,timer}
	systemctl daemon-reload
	```
- Delete some cached Docker images:
	```sh
	docker system prune -a
	# or delete them all:
	docker rmi $(docker images -aq)
	```
- Uninstall Docker itself, if necessary
- Delete the `/mash` directory:
	```sh
	rm -rf /mash
	```
