"""Sensor platform for REST2MQTT integration."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN


class Rest2MqttSensor(SensorEntity):
    """Representation of a REST2MQTT sensor."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, sensor_name: str) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._entry = entry
        self._sensor_name = sensor_name

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"rest2mqtt_{self._sensor_name}"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f"{DOMAIN}_{self._entry.entry_id}_{self._sensor_name}"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor_name)