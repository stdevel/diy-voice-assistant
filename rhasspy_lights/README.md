# rhasspy_lights

Application that listens for Rhasspy events and animates when assistant wakes up or handles an intent.

## Installation

Run requirements via `pip3`:

```shell
$ pip3 install -r requirements.txt
```

Alternatively, check out the [`requirements.txt`](requirements.txt) file and try to find and install packages using your distribution's package manager.

## Usage

The application supports the following parameters:

| Parameter | Default | Description |
| --------- | ------- | ----------- |
| `-d` / `--debug` | no | Enables debugging outputs |
| `-b` / `--brightness` | `10` | Sets brightness (*1-100*) |
| `-p` / `--pattern` | `google` | Sets the animation pattern (*`echo`, `google`*) |
| `-H` / `--host` | `localhost` | Sets MQTT broker |
| `-P` / `--port` | `12183` | Sets MQTT port |
| `-u` / `--username` | *empty* | Sets MQTT username |
| `-p` / `--password` | *empty* | Sets MQTT password |

It can be launched as systemd unit:

```shell
# cp /usr/lib/systemd/user/lightsd.service /etc/systemd/system/
# systemctl daemon-reload
# systemctl enable --now lightsd.service
```

You might want to alter [`lightsd.service`](lightsd.service) to adjust the service user (*see `User` and `Group` definitions*) or additional parameters.
