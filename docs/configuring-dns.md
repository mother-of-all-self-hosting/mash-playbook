# Configuring DNS

To reach your services, you'd need to do some DNS configuration. We recommend you set up at least one (sub-)domain. Each service can be hostet at a subpath of this domain or on separate (sub-)domains.

A simple example could be this

| Service               | Type  | Host                | Target              |
|-----------------------|-------|---------------------|---------------------|
| Miniflux and radicale | A     | `mash.example.com`  | `IP of your server` |
| Nextcloud             | CNAME | `cloud.example.com` | `mash.example.com`  |

Here you could reach the feedreader miniflux at https://mash.example.com/miniflux (if you set
`miniflux_path_prefix: /miniflux` in your `vars.yml`) and radicale at https://mash.example.com/radicale. In the example
the nextcloud has a different subdomain, so you could access it at https://cloud.example.com

Feel free to change this as you like, just make sure that you set `<service>_hostname` and `<service>_path_prefix`
accordingly in your `vars.yml`.

Be mindful as to how long it will take for the DNS records to propagate.

When you're done configuring DNS, proceed to [Configuring the playbook](configuring-playbook.md).
