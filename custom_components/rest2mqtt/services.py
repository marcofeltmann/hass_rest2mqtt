"""Service handlers for REST2MQTT integration."""
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN


def register_services(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register services for the integration."""
    coordinator = entry.runtime_data.coordinator

    async def publish_mqtt_data(call: ServiceCall) -> None:
        """Publish data to MQTT."""
        service_name = call.data.get("service")
        message = call.data.get("message")

        if service_name and message:
            from homeassistant.components.mqtt import async_publish_message

            await async_publish_message(hass, f"{DOMAIN}/{service_name}", message, retain=True)

    hass.services.async_register(DOMAIN, "publish_data", publish_mqtt_data)