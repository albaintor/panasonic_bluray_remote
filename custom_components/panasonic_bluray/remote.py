"""Support for Panasonic Blu-ray players."""
from __future__ import annotations

import time
from typing import Iterable, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
    RemoteEntityFeature,
    ENTITY_ID_FORMAT
)

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

import logging

from .const import PANASONIC_COORDINATOR, DOMAIN, DEFAULT_DEVICE_NAME
from .coordinator import PanasonicCoordinator

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Panasonic Blu-Ray remote"

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Use to setup entity."""
    _LOGGER.debug("Panasonic async_add_entities remote")
    coordinator = hass.data[DOMAIN][config_entry.entry_id][PANASONIC_COORDINATOR]
    async_add_entities(
        [PanasonicBluRayRemote(coordinator, coordinator.name)]
    )


class PanasonicBluRayRemote(CoordinatorEntity[PanasonicCoordinator], RemoteEntity):
    """Representation of a Panasonic Blu-ray device."""

    _attr_icon = "mdi:disc-player"
    _attr_supported_features: RemoteEntityFeature = RemoteEntityFeature(0)

    def __init__(self, coordinator, name):
        """Initialize the Panasonic Blue-ray remote entity."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._attr_name = name
        self._attr_media_position_updated_at = None
        self._state : MediaPlayerState | None = None
        self._attr_name = name
        self._attr_media_position = 0
        self._attr_media_duration = 0
        self._unique_id = ENTITY_ID_FORMAT.format(
            f"{self.coordinator.api._host}_Remote")

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Mac address is unique identifiers within a specific domain
                (DOMAIN, self.coordinator.api._host)
            },
            name=self.coordinator.name,
            manufacturer="Panasonic",
            model=self.coordinator.name
        )

    @property
    def unique_id(self) -> str | None:
        return self._unique_id

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Update only if activity changed
        self.update()
        self.async_write_ha_state()
        return super()._handle_coordinator_update()

    def update(self) -> None:
        """Update the internal state by querying the device."""
        data = self.coordinator.data
        self._attr_state = data.get("state", None)
        self._attr_media_position = data.get("media_position", None)
        self._attr_media_position_updated_at = data.get("media_position_updated_at", None)
        self._attr_media_duration = data.get("media_duration", None)

    def turn_off(self) -> None:
        """Instruct the device to turn standby.

        Sending the "POWER" button will turn the device to standby - there
        is no way to turn it completely off remotely. However this works in
        our favour as it means the device is still accepting commands and we
        can thus turn it back on when desired.
        """
        if self._attr_state != MediaPlayerState.OFF:
            self.coordinator.api.send_key("POWER")

        self._attr_state = MediaPlayerState.OFF

    def turn_on(self) -> None:
        """Wake the device back up from standby."""
        if self._attr_state == MediaPlayerState.OFF:
            self.coordinator.api.send_key("POWER")

        self._attr_state = MediaPlayerState.IDLE

    def toggle(self, activity: str = None, **kwargs):
        """Toggle a device."""
        self.coordinator.api.send_key("POWER")

    def send_command(self, command: Iterable[str], **kwargs: Any) -> None:
        """Send commands to one device."""
        num_repeats = kwargs.get(ATTR_NUM_REPEATS, DEFAULT_NUM_REPEATS)
        delay_secs = kwargs.get(ATTR_DELAY_SECS, DEFAULT_DELAY_SECS)
        hold_secs = kwargs.get(ATTR_HOLD_SECS, DEFAULT_HOLD_SECS)

        for _ in range(num_repeats):
            for single_command in command:
                # Not supported : hold and release modes
                # if hold_secs > 0:
                #     self._device.send_key(single_command)
                #     time.sleep(hold_secs)
                # else:
                results = self.coordinator.api.send_key(single_command)
                _LOGGER.debug("send_command %s %d repeats %d delay : %s", ''.join(list(command)),
                              num_repeats, delay_secs, results[0])
                time.sleep(delay_secs)