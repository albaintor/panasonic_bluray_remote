"""Support for Panasonic Blu-ray players."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    ENTITY_ID_FORMAT
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, PANASONIC_COORDINATOR, DEFAULT_DEVICE_NAME
from .coordinator import PanasonicCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Use to setup entity."""
    _LOGGER.debug("Panasonic async_add_entities media player")
    coordinator = hass.data[DOMAIN][config_entry.entry_id][PANASONIC_COORDINATOR]
    async_add_entities(
        [PanasonicBluRayMediaPlayer(coordinator, coordinator.name)]
    )


class PanasonicBluRayMediaPlayer(CoordinatorEntity[PanasonicCoordinator], MediaPlayerEntity):
    """Representation of a Panasonic Blu-ray device."""

    _attr_icon = "mdi:disc-player"
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.STOP
        | MediaPlayerEntityFeature.PAUSE
        | MediaPlayerEntityFeature.NEXT_TRACK
        | MediaPlayerEntityFeature.PREVIOUS_TRACK
    )

    def __init__(self, coordinator, name):
        """Initialize the Panasonic Blue-ray device."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._attr_name = name
        self._attr_state = MediaPlayerState.OFF
        self._attr_media_position = 0
        self._attr_media_duration = 0
        self._unique_id = ENTITY_ID_FORMAT.format(
            f"{self.coordinator.api._host}_MediaPlayer")

    @property
    def unique_id(self) -> str | None:
        return self._unique_id

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

    def media_play(self) -> None:
        """Send play command."""
        self.coordinator.api.send_key("PLAYBACK")
        self.schedule_update_ha_state()

    def media_pause(self) -> None:
        """Send pause command."""
        self.coordinator.api.send_key("PAUSE")
        self.schedule_update_ha_state()

    def media_stop(self) -> None:
        """Send stop command."""
        self.coordinator.api.send_key("STOP")
        self.schedule_update_ha_state()

    def media_next_track(self):
        """Send next track command."""
        self.coordinator.api.send_key("SKIPFWD")
        self.schedule_update_ha_state()

    def media_previous_track(self):
        """Send the previous track command."""
        self.coordinator.api.send_key("SKIPREV")
        self.schedule_update_ha_state()
