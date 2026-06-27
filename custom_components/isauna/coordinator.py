"""Data update coordinator for the iSauna integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    APPLY_DEBOUNCE,
    DATA_TEMPLATE,
    DOMAIN,
    LOGGER,
    MAX_TOLERATED_FAILURES,
    MODE_OFF,
    SCAN_INTERVAL_ACTIVE,
    SCAN_INTERVAL_IDLE,
    WRITABLE_KEYS,
)
from .device import IsaunaConnectionError, IsaunaDevice


class IsaunaCoordinator(DataUpdateCoordinator[dict]):
    """Polls the controller and auto-applies local control changes (debounced)."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, device: IsaunaDevice
    ) -> None:
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL_ACTIVE,
        )
        self.entry = entry
        self.device = device
        self._state: dict = dict(DATA_TEMPLATE)
        self._pending_seeded = False
        self._fail_count = 0
        # Coalesce rapid changes (e.g. dragging a slider) into a single send.
        self._apply_debouncer = Debouncer(
            hass,
            LOGGER,
            cooldown=APPLY_DEBOUNCE,
            immediate=False,
            function=self._async_apply,
        )

    async def _async_update_data(self) -> dict:
        try:
            new_data = await self.device.async_poll()
        except IsaunaConnectionError as err:
            self._fail_count += 1
            # Keep serving the last known good data through brief outages so the
            # entities don't flap to "unavailable" on a single refused poll.
            if self._fail_count <= MAX_TOLERATED_FAILURES and self._pending_seeded:
                LOGGER.debug(
                    "Poll failed (%s/%s), keeping last known data: %s",
                    self._fail_count,
                    MAX_TOLERATED_FAILURES,
                    err,
                )
                return dict(self._state)
            raise UpdateFailed(str(err)) from err

        self._fail_count = 0
        if new_data is not None:
            self._state.update(new_data)
            self._seed_pending()

        # Slow down polling while the sauna is off.
        self.update_interval = (
            SCAN_INTERVAL_IDLE
            if self._state.get("mode") == MODE_OFF
            else SCAN_INTERVAL_ACTIVE
        )
        return dict(self._state)

    def _seed_pending(self) -> None:
        """Initialise the staged set_* values from the controller once."""
        if self._pending_seeded:
            return
        self._state["set_mode"] = self._state.get("mode", MODE_OFF)
        self._state["set_temperature"] = self._state.get("desired_temperature", 30)
        self._state["set_infra1"] = self._state.get("infra1", 0)
        self._state["set_infra2"] = self._state.get("infra2", 0)
        self._pending_seeded = True

    async def async_set_local(self, key: str, value) -> None:
        """Apply a control change locally, then schedule a debounced send."""
        await self.async_set_local_many({key: value})

    async def async_set_local_many(self, values: dict) -> None:
        """Apply several control changes locally with a single debounced send."""
        for key, value in values.items():
            if key not in WRITABLE_KEYS:
                raise ValueError(f"unknown writable key: {key}")
            self._state[key] = value
        self.async_set_updated_data(dict(self._state))
        await self._apply_debouncer.async_call()

    async def _async_apply(self) -> None:
        """Send the full current state to the controller, then refresh."""
        try:
            await self.device.async_apply(self._state)
        except IsaunaConnectionError as err:
            LOGGER.warning("Failed to apply settings to controller: %s", err)
            return
        await self.async_request_refresh()

    async def async_shutdown(self) -> None:
        """Cancel any pending send on unload."""
        await self._apply_debouncer.async_shutdown()
        await super().async_shutdown()
