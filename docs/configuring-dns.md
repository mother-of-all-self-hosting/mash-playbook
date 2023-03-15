# Configuring DNS

To reach your services, you'd need to do some DNS configuration.

## DNS settings example

The DNS setup is dependent on which services you want to activate. You need t oset the first entry and an entry for each
service you activate that needs a (sub-)domain. Feel free to adjust the host to you liking (you can even use a separate domain).

| Service     | Type  | Host                   | Target              |
|-------------|-------|------------------------|---------------------|
| -           | A     | `example.com`          | `IP of your server` |
| Radicale    | CNAME | `calendar.example.com` | `example.com`       |
| Miniflux    | CNAME | `feed.example.com`     | `example.com`       |
| Uptime-kuma | CNAME | `status.example.com`   | `example.com`       |

Be mindful as to how long it will take for the DNS records to propagate.

When you're done configuring DNS, proceed to [Configuring the playbook](configuring-playbook.md).
