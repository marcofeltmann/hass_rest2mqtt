from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, LOGGER_NAME
from .coordinator import Rest2MqttCoordinator
from .sensor import async_setup_entry as sensor_setup_entry

PLATFORMS = ["sensor"]

LOGGER = __import__("logging").getLogger(LOGGER_NAME)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Rest2Mqtt integration from a config entry."""
    coordinator = Rest2MqttCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    
    from .coordinator import Rest2MqttData
    entry.runtime_data = Rest2MqttData(hass, entry, coordinator)
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if hasattr(entry, "runtime_data") and entry.runtime_data:
        await entry.runtime_data.coordinator.async_unload()
        entry.runtime_data = None
    
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)