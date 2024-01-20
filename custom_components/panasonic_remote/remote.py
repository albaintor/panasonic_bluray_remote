"""Support for Panasonic Blu-ray players."""
from __future__ import annotations

import time
from datetime import timedelta
from typing import Iterable, Any

from panacotta import PanasonicBD
import voluptuous as vol

from homeassistant.components.media_player import (
    MediaPlayerState
)

from homeassistant.components.remote import (
    ATTR_DELAY_SECS,
    ATTR_HOLD_SECS,
    ATTR_NUM_REPEATS,
    DEFAULT_DELAY_SECS,
    DEFAULT_HOLD_SECS,
    DEFAULT_NUM_REPEATS,
    RemoteEntity,
    PLATFORM_SCHEMA, RemoteEntityFeature
)

from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.util.dt import utcnow

import logging

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Panasonic Blu-Ray remote"

SCAN_INTERVAL = timedelta(seconds=30)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Panasonic Blu-ray remote platform."""
    conf = discovery_info if discovery_info else config
    try:
        async_add_entities([PanasonicBluRayRemote(conf[CONF_HOST], conf[CONF_NAME])], True)
    except OSError:
        _LOGGER.error(
            "Failed to connect to Panasonic player at %s:%s for remote entity. "
            "Please check your configuration",
            conf[CONF_HOST],
            conf[CONF_NAME],
        )


class PanasonicBluRayRemote(RemoteEntity):
    """Representation of a Panasonic Blu-ray device."""

    _attr_icon = "mdi:disc-player"
    _attr_supported_features: RemoteEntityFeature = RemoteEntityFeature(0)

    def __init__(self, ip, name):
        """Initialize the Panasonic Blue-ray device."""
        self._attr_media_position_updated_at = None
        self._device = PanasonicBD(ip)
        self._state = None
        self._attr_name = name
        self._attr_media_position = 0
        self._attr_media_duration = 0

    def update(self) -> None:
        """Update the internal state by querying the device."""
        # This can take 5+ seconds to complete
        state = self._device.get_play_status()

        if state[0] == "error":
            self._state = None
        elif state[0] in ["off", "standby"]:
            # We map both of these to off. If it's really off we can't
            # turn it on, but from standby we can go to idle by pressing
            # POWER.
            self._state = MediaPlayerState.OFF
        elif state[0] in ["paused", "stopped"]:
            self._state = MediaPlayerState.IDLE
        elif state[0] == "playing":
            self._state = MediaPlayerState.PLAYING

        # Update our current media position + length
        if state[1] >= 0:
            self._attr_media_position = state[1]
        else:
            self._attr_media_position = 0
        self._attr_media_position_updated_at = utcnow()
        self._attr_media_duration = state[2]

    def turn_off(self) -> None:
        """Instruct the device to turn standby.

        Sending the "POWER" button will turn the device to standby - there
        is no way to turn it completely off remotely. However this works in
        our favour as it means the device is still accepting commands and we
        can thus turn it back on when desired.
        """
        if self.state != MediaPlayerState.OFF:
            self._device.send_key("POWER")

        self._state = MediaPlayerState.OFF

    def turn_on(self) -> None:
        """Wake the device back up from standby."""
        if self.state == MediaPlayerState.OFF:
            self._device.send_key("POWER")

        self._state = MediaPlayerState.IDLE

    def toggle(self, activity: str = None, **kwargs):
        """Toggle a device."""
        self._device.send_key("POWER")

    def send_command(self, command: Iterable[str], **kwargs: Any) -> None:
        """Send commands to one device."""
        num_repeats = kwargs.get(ATTR_NUM_REPEATS, DEFAULT_NUM_REPEATS)
        delay_secs = kwargs.get(ATTR_DELAY_SECS, DEFAULT_DELAY_SECS)
        hold_secs = kwargs.get(ATTR_HOLD_SECS, DEFAULT_HOLD_SECS)

        _LOGGER.debug("async_send_command %s %d repeats %d delay", ''.join(list(command)), num_repeats, delay_secs)

        for _ in range(num_repeats):
            for single_command in command:
                # Not supported : hold and release modes
                # if hold_secs > 0:
                #     self._device.send_key(single_command)
                #     time.sleep(hold_secs)
                # else:
                self._device.send_key(single_command)
                time.sleep(delay_secs)