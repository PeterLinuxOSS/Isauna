"""Select platform for the iSauna integration (staged operating mode)."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import IsaunaConfigEntry
from .const import MODES
from .entity import IsaunaEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: IsaunaConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([IsaunaModeSelect(entry.runtime_data)])


class IsaunaModeSelect(IsaunaEntity, SelectEntity):
    """Operating mode applied to the controller (debounced) when changed."""

    _attr_translation_key = "set_mode"
    _attr_options = MODES

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "set_mode")

    @property
    def current_option(self) -> str | None:
        return self.data.get("set_mode")

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.async_set_local("set_mode", option)
