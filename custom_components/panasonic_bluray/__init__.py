"""The panasonic_bluray remote and media player component."""
from __future__ import absolute_import

from panacotta import PanasonicBD
from .const import DOMAIN, DEFAULT_DEVICE_NAME, PANASONIC_COORDINATOR, STARTUP, PANASONIC_API, NAME
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_HOST
from homeassistant.core import HomeAssistant
from .coordinator import PanasonicCoordinator

_LOGGER: logging.Logger = logging.getLogger(__package__)
_LOGGER.info(STARTUP)


PLATFORMS: list[Platform] = [
    Platform.MEDIA_PLAYER,
    Platform.REMOTE
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Unfolded Circle Remote from a config entry."""

    panasonic_device = PanasonicBD(entry.data[CONF_HOST])
    _LOGGER.debug("Panasonic device initialization")
    coordinator = PanasonicCoordinator(hass, panasonic_device, DEFAULT_DEVICE_NAME)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        PANASONIC_COORDINATOR: coordinator,
        PANASONIC_API: panasonic_device,
    }

    # Retrieve info from Remote
    # Get Basic Device Information
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(update_listener))
    # await zeroconf.async_get_async_instance(hass)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    try:
        coordinator: PanasonicCoordinator = hass.data[DOMAIN][entry.entry_id][PANASONIC_COORDINATOR]
        # coordinator.api.?
    except Exception as ex:
        _LOGGER.error("Sony device async_unload_entry error", ex)
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Update Listener."""
    #TODO Should be ?
    #await async_unload_entry(hass, entry)
    #await async_setup_entry(hass, entry)
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    try:
        coordinator: PanasonicCoordinator = hass.data[DOMAIN][entry.entry_id][PANASONIC_COORDINATOR]
        # coordinator.api.?
    except Exception as ex:
        _LOGGER.error("Panasonic device async_unload_entry error", ex)
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Update Listener."""
    # TODO Should be ?
    # await async_unload_entry(hass, entry)
    # await async_setup_entry(hass, entry)
    await hass.config_entries.async_reload(entry.entry_id)
