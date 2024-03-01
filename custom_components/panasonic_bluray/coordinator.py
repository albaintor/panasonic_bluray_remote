"""The IntelliFire integration."""
from __future__ import annotations

import logging
from typing import Any

import requests
from homeassistant.components.media_player import MediaPlayerState
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import utcnow
from panacotta import PanasonicBD

from .const import MIN_TIME_BETWEEN_SCANS, DOMAIN

_LOGGER = logging.getLogger(__name__)


class PanasonicCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Data update coordinator for an Unfolded Circle Remote device."""
    # List of events to subscribe to the websocket
    subscribe_events: dict[str, bool]

    def __init__(self, hass: HomeAssistant, panasonic_device: PanasonicBD, name: str) -> None:
        """Initialize the Coordinator."""
        super().__init__(
            hass,
            name=DOMAIN,
            logger=_LOGGER,
            update_interval=MIN_TIME_BETWEEN_SCANS,
        )
        self.hass = hass
        self.name = name
        self.api = panasonic_device
        self.data = {}

    async def _async_update_data(self) -> dict[str, Any]:
        """Get the latest data from the Unfolded Circle Remote."""
        _LOGGER.debug("Sony device coordinator update")
        try:
            self.data = await self.hass.async_add_executor_job(self.update)
            return self.data
        except Exception as ex:
            _LOGGER.error("Sony device coordinator error during update", ex)
            raise UpdateFailed(
                f"Error communicating with Sony device API {ex}"
            ) from ex

    def update(self) -> dict[str, any]:
        """Update the internal state by querying the device."""
        data = {}
        # This can take 5+ seconds to complete
        state = self.api.get_play_status()

        if state[0] == "error":
            data["state"] = None
        elif state[0] in ["off", "standby"]:
            # We map both of these to off. If it's really off we can't
            # turn it on, but from standby we can go to idle by pressing
            # POWER.
            data["state"] = MediaPlayerState.OFF
        elif state[0] in ["paused", "stopped"]:
            data["state"] = MediaPlayerState.IDLE
        elif state[0] == "playing":
            data["state"] = MediaPlayerState.PLAYING

        # Update our current media position + length
        if state[1] >= 0:
            data["media_position"] = state[1]
        else:
            data["media_position"] = 0
        data["media_position_updated_at"] = utcnow()
        data["media_duration"] = state[2]
        return data

