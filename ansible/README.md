# Ansible playbook

This playbook prepares the Raspberry Pi for use as voice assistant with [Rhasspy](https://github.com/synesthesiam/rhasspy) and [Node-RED](https://nodered.org). Both applications will be running on [Docker CE](https://docs.docker.com/get-docker/). It also stages driver files for a [ReSpeaker](https://respeaker.io) voice card and starts an [online radio Docker container](https://github.com/stdevel/radio_api).

[Raspbian Buster](https://raspbian.org) should be installed on the Raspberry Pi.

## Dependencies

The following Ansible roles are used:
- [`weareinteractive.ufw`](https://galaxy.ansible.com/weareinteractive/ufw)
- [`nickjj.docker`](https://galaxy.ansible.com/nickjj/docker)

## Usage

Copy your SSH key to your Raspberry Pi:

```shell
$ ssh-copy-id pi@<ip-address>
```

Update the [`inventory`](inventory) file to include your Raspberry Pi IP addresses:

```
[assistants]
192.168.178.200
```

Run the playbook:

```shell
$ ansible-playbook -i inventory
```

Wait - this can take up to 45 minutes.
Once finishes, login to the Raspberry Pi and compile the seeed-voicecard drive (*if you're using a ReSpeaker voice card*):

```shell
$ ssh pi@<ip_address>
$ sudo bash
# cd seeed-voicecard
# ./install.sh
```

Once finished, reboot the system:

```shell
# sudo reboot
```

You should now be able to access both applications via the following links:
- Node-RED: http://<ip_address>:1880
- Rhasppy: http://<ip_address>:12101
