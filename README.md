# Panasonic Bluray Players remote for Home Assistant

This is a custom component to allow control of Panasonic Bluray Players [Homeassistant](https://home-assistant.io).

It completes the existing Panasonic integration (media player) with the missing commands in a remote entity type.

To make it work with latest UHD bluray players (such as UB820), you will have to enable voice control in the network menu AND to patch the Panasonic firmware (not an easy procedure).
More information on [AVSForum](https://www.avforums.com/threads/lets-try-again-to-put-the-free-in-regionfreedom.2441584/post-31906429)
Tested correctly on Panasonic UB820.

## Installation 

**Recommanded**

Use [HACS](https://hacs.xyz/).

**Manual**

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `panasonic_remote`.
4. Download _all_ the files from the `custom_components/panasonic_remote/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant

## Configuration

Edit `configuration.yaml` and add `panasonic_remote` as a new `remote`

```yaml
remote:
  - platform: panasonic_remote
    name: Panasonic Blu-Ray remote
    host: 192.168.1.2
```

Name|Required|Description|Default
--|--|--|--
`name`|no|Friendly name|liveboxtvuhd
`host`|yes|Host or ip address| 

Available commands for remote entity :

Command|Description
--|--
POWER|Power toggle
OP_CL|Open/close
PLAYBACK|Play
PAUSE|Pause
STOP|Stop
SKIPFWD|Next chapter
SKIPREV|Previous chapter
REV|Rewind
D0|0
D1|1
D2|2
D3|3
D4|4
D5|5
D6|6
D7|7
D8|8
D9|9
D12|12
SHARP|#
CLEAR|* or cancel
UP|Up
DOWN|Down
LEFT|Left
RIGHT|Right
SELECT|Select
RETURN|Return
EXIT|Exit
MLTNAVI|Home
DSPSEL|Status
TITLE|Title
MENU|Menu
PUPMENU|Popup Menu
SHFWD1|SHFWD1
SHFWD2|SHFWD2
SHFWD3|SHFWD3
SHFWD4|SHFWD4
SHFWD5|SHFWD5
SHREV1|SHREV1
SHREV2|SHREV2
SHREV3|SHREV3
SHREV4|SHREV4
SHREV5|SHREV5
JLEFT|JLEFT
JRIGHT|JRIGHT
RED|Red
BLUE|Blue
GREEN|Green
YELLOW|Yellow
NETFLIX|Netflix
SKYPE|Skype
V_CAST|V_CAST
3D|3D
NETWORK|Network
AUDIOSEL|Audio language
KEYS|Keys
CUE|Cue
CHROMA|Chrooma
MNBACK|MNBACK
MNSKIP|MNSKIP
2NDARY|2NDARY
PICTMD|PICTMD
DETAIL|DETAIL
RESOLUTN|Resolution
OSDONOFF|OSD ON/OFF
P_IN_P|Picture in picture

## Examples
To trigger additional commands with the remote entity :
```yaml
service: remote.send_command
data:
  command: UP
target:
  entity_id: remote.panasonic_bluray_remote
```