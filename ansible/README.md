# Ansible playbook

This playbook prepares the Raspberry Pi for use as voice assistant with [Rhasspy](https://github.com/synesthesiam/rhasspy) and [Node-RED](https://nodered.org). Both applications will be running on [Docker CE](https://docs.docker.com/get-docker/). It also stages driver files for a [ReSpeaker](https://respeaker.io) voice card and starts an [online radio Docker container](https://github.com/stdevel/radio_api).

[Raspberry Pi OS (*aka Raspbian*)](https://raspbian.org) is the preferenced distribution as it is more stable and offers better driver support for the ReSpeaker, but [Ubuntu Server](https://ubuntu.com/download/raspberry-pi) should also be possible. Please not that conventional Debian **won't work**.

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

```ini
[assistants]
192.168.178.200
```

When using Rasbian instead of Ubuntu, change the `remote_user` variable to `pi`.

Run the playbook:

```shell
$ ansible-playbook -i inventory
```

Wait - this can take up to 45 minutes.
Once finishes, login to the Raspberry Pi and compile the seeed-voicecard drive (*if you're using a ReSpeaker voice card*):

```shell
$ ssh ubuntu@<ip_address>
$ sudo bash
# cd seeed-voicecard
# ./ubuntu-prerequisite.sh
# ./install.sh
```

Once finished, reboot the system:

```shell
# reboot
```

You should now be able to access the applications via the following links:

- radio_api: [http://ip-address:5000](http://ip-address:5000)
- Rhasppy: [http://ip-address:12101](http://ip-address:12101)
- Node-RED: [http://ip-address:1880](http://ip-address:1880)

## Post-configuation

### Rhasspy

- Settings
  - Audio Recording > PyAudio
  - Wake Word > Rhasspy Raven or Porcupine
  - Speech to Text > Pocketsphinx
  - Intent Recognition > Fsticuffs
  - Text to Speech > NanoTTS
    - for MaryTTS: [http://marytts:59125/process](http://marytts:59125/process)
  - Audio Playing > aplay
  - Intent Handling > Remote HTTP
    - Remote URL: [http://ip-address:1880/intent](http://ip-address:1880/intent)
  - Sounds
    - Wake WAV: `/usr/lib/rhasspy/.venv/lib/python3.7/site-packages/snowboy/resources/ding.wav`
    - Recorded WAV: `/usr/lib/rhasspy/.venv/lib/python3.7/site-packages/snowboy/resources/dong.wav`
- Save Settings
- F5
- Download
- Sentences
  - Import from [sentences.ini](templates/sentences.ini)
  - Save

## TODOs

MaryTTS
