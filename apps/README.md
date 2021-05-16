# apps

Collection of smaller Rhasspy apps.

## Generic instructions

Run requirements via `pip3`:

```shell
$ pip3 install -r requirements.txt
```

Alternatively, check out the [`requirements.txt`](requirements.txt) file and try to find and install packages using your distribution's package manager.

Applications can be launched as systemd unit:

```shell
# cp /usr/lib/systemd/user/<name>.service /etc/systemd/system/
# systemctl daemon-reload
# systemctl enable --now <name>.service
```
