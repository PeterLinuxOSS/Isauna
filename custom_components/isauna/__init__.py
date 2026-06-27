"""The iSauna integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_HOST,
    CONF_PORT,
    CONF_TCP_PASSWORD,
    DEFAULT_PORT,
    DEFAULT_TCP_PASSWORD,
    PLATFORMS,
)
from .coordinator import IsaunaCoordinator
from .device import IsaunaDevice

type IsaunaConfigEntry = ConfigEntry[IsaunaCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: IsaunaConfigEntry) -> bool:
    """Set up iSauna from a config entry."""
    device = IsaunaDevice(
        host=entry.data[CONF_HOST],
        port=entry.data.get(CONF_PORT, DEFAULT_PORT),
        tcp_password=entry.data.get(CONF_TCP_PASSWORD, DEFAULT_TCP_PASSWORD),
    )
    coordinator = IsaunaCoordinator(hass, entry, device)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: IsaunaConfigEntry) -> bool:
    """Unload a config entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        await entry.runtime_data.async_shutdown()
    return unloaded
