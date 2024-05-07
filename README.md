# Panasonic Bluray Players for Home Assistant

This is a custom component to allow control of Panasonic Bluray Players [Homeassistant](https://home-assistant.io).

It is a fork of the existing Panasonic integration (media player) with the missing commands and an additional remote entity type.

To make it work with latest UHD bluray players (such as UB820), you will have to enable voice control in the network menu AND to patch the Panasonic firmware (not an easy procedure).
More information on [AVSForum](https://www.avforums.com/threads/lets-try-again-to-put-the-free-in-regionfreedom.2441584/post-31906429)
Tested correctly on Panasonic UB820.

## Installation 

**Recommended**

Use [HACS](https://hacs.xyz/).
   1. From within Home Assistant, click on the link to **HACS**
   2. Click on **Integrations**
   3. Click on the vertical ellipsis in the top right and select **Custom repositories**
   4. Enter the URL for this repository in the section that says _Add custom repository URL_ and select **Integration** in the _Category_ dropdown list
   5. Click the **ADD** button
   6. Close the _Custom repositories_ window
   7. You should now be able to see the _Panasonic Bluray_ card on the HACS Integrations page. Click on **INSTALL** and proceed with the installation instructions.
   8. Restart your Home Assistant instance and then proceed to the _Configuration_ section below.

**Manual**

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `panasonic_bluray`.
4. Download _all_ the files from the `custom_components/panasonic_bluray/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant

## Configuration
There is a config flow for this integration. After installing the custom component and restarting:

1. Navigate to **Settings** -> **Integrations** and click on **Add an integration**
2. Configure the `host` or `IP address` of the Panasonic Bluray Player
3. Click Submit and select your device area.
4. You should see the new device with the 2 entities : Media Player and Remote Control

Name|Required|Description|Default
--|--|--|--
`name`|no|Friendly name|Panasonic bluray
`host`|yes|Host or ip address| 

Available commands for remote entity :

Command|Description
--|--
POWERON|Power on
POWEROFF|Power off
POWER|Power toggle
OP_CL|Open/close
PLAYBACK|Play
PAUSE|Pause
STOP|Stop
SKIPFWD|Next chapter
SKIPREV|Previous chapter
REV|Rewind
CUE|Fast forward
D0|0 (-,)
D1|1 (@.)
D2|2 (ABC)
D3|3 (DEF)
D4|4 (GHI)
D5|5 (JKL)
D6|6 (MNO)
D7|7 (PQRS)
D8|8 (TUV)
D9|9 (WXYZ)
D12|12
SHARP|# ([_])
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
MNBACK|Manual skip -10s
MNSKIP|Manual skip +60s
2NDARY|2NDARY
PICTMD|PICTMD
DETAIL|DETAIL
RESOLUTN|Resolution
OSDONOFF|OSD ON/OFF
P_IN_P|Picture in picture
PLAYBACKINFO|Playback Info	 
CLOSED_CAPTION|Closed Caption
TITLEONOFF|Subtitle
HDR_PICTUREMODE|HDR Picture Mode
PICTURESETTINGS|Picture Setting
SOUNDEFFECT|Soud Effect
HIGHCLARITY|High clarity
SKIP_THE_TRAILER|Skip The Trailer
MIRACAST|Mirroring


## Examples
To trigger additional commands with the remote entity :
```yaml
service: remote.send_command
data:
  command: UP
target:
  entity_id: remote.panasonic_bluray_remote
```
