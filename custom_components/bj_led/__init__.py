from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, Event
from homeassistant.const import CONF_MAC, EVENT_HOMEASSISTANT_STOP

from .const import DOMAIN, CONF_RESET, CONF_DELAY
from .elkbledob import ELKBLEDOBInstance
import logging

LOGGER = logging.getLogger(__name__)
PLATFORMS = ["light"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    reset = entry.options.get(CONF_RESET, None) or entry.data.get(CONF_RESET, None)
    delay = entry.options.get(CONF_DELAY, None) or entry.data.get(CONF_DELAY, None)
    LOGGER.debug("Config Reset data: %s and config delay data: %s", reset, delay)

    instance = ELKBLEDOBInstance(entry.data[CONF_MAC], reset, delay, hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = instance

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    async def _async_stop(event: Event) -> None:
        """Close the connection."""
        await instance.stop()

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _async_stop)
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        instance = hass.data[DOMAIN][entry.entry_id]
        await instance.stop()
    hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    instance = hass.data[DOMAIN][entry.entry_id]
    if entry.title != instance.name:
        await hass.config_entries.async_reload(entry.entry_id)
