"""Data update coordinator for REST2MQTT integration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import CONF_RESTORE, DOMAIN, LOGGER_NAME

LOGGER = __import__("logging").getLogger(LOGGER_NAME)


@dataclass
class Rest2MqttData:
    """Class to hold coordinator data."""

    hass: HomeAssistant
    entry: ConfigEntry
    coordinator: Rest2MqttCoordinator


class Rest2MqttCoordinator(DataUpdateCoordinator):
    """Class to coordinate data updates for REST2MQTT."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(
            hass,
            LOGGER,
            config_entry=entry,
            name=DOMAIN,
        )
        self.data: dict[str, Any] = {}
        self._host = entry.data.get("host")
        self._port = entry.data.get("port")
        self._restore = entry.data.get(CONF_RESTORE, False)
        self._rest_services = entry.data.get("rest_services", [])

    async def async_config_entry_first_refresh(self) -> None:
        """Fetch data once to setup."""
        await self.async_refresh()

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from source."""
        data = {
            "host": self._host,
            "port": self._port,
            "restore": self._restore,
            "timestamp": "2024-01-01T00:00:00Z",
            "services": [
                {"name": service["name"], "value": service.get("value", "N/A")}
                for service in self._rest_services
            ],
        }
        return data

    async def async_refresh(self) -> None:
        """Refresh the data."""
        try:
            data = await self._async_update_data()
            LOGGER.debug(
                "Got data for REST2MQTT integration: %s", data, extra={"mqtt_host": self._host, "mqtt_port": self._port}
            )
        except Exception as err:
            LOGGER.exception("Error updating REST2MQTT", extra={"mqtt_host": self._host, "mqtt_port": self._port})
            raise UpdateFailed(f"Error updating data: {err}") from err
        
        self.data = data

    async def async_unload(self) -> None:
        """Clear data."""
        self.data = {}