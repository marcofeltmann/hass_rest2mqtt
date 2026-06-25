from __future__ import annotations

from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_RESTORE
from homeassistant.core import HomeAssistant

from .const import (
    CONF_RESTORE_STATE,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_RESTORE,
    DOMAIN,
)

STEP_CONFIGURATION = "configuration"


def _get_user_configuration_schema(current_data: dict[str, Any]) -> dict:
    """Get the schema for user configuration step."""
    return {
        vol.Required(
            CONF_HOST, default=current_data.get(CONF_HOST, DEFAULT_HOST)
        ): str,
        vol.Required(
            CONF_PORT, default=current_data.get(CONF_PORT, DEFAULT_PORT)
        ): int,
        vol.Required(
            CONF_RESTORE, default=current_data.get(CONF_RESTORE, DEFAULT_RESTORE)
        ): bool,
        vol.Optional(
            CONF_RESTORE_STATE,
            default=current_data.get(CONF_RESTORE_STATE, DEFAULT_RESTORE),
        ): bool,
    }


def _validate_input(user_input: dict[str, Any]) -> dict[str, Any]:
    """Validate user inputs."""
    errors = {}
    
    host = user_input.get(CONF_HOST)
    port = user_input.get(CONF_PORT)
    
    if not host:
        errors[CONF_HOST] = "Host is required"
    
    if not port:
        errors[CONF_PORT] = "Port is required"
    
    return errors


class Rest2MqttConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Rest2Mqtt config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        if not user_input:
            return self._show_config_form()
        
        errors = _validate_input(user_input)
        
        if errors:
            return self._show_config_form(user_input, errors)
        
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        
        return self.async_create_entry(title="REST2MQTT", data=user_input)

    def _show_config_form(
        self, user_input: dict[str, Any] | None = None, errors: dict | None = None
    ) -> config_entries.ConfigFlowResult:
        """Show the configuration form."""
        data = user_input or {}
        schema = _get_user_configuration_schema(data)
        
        step_args = {
            "data": data,
            "errors": errors or {},
            "step_id": STEP_CONFIGURATION,
        }
        
        return self.async_show_form(
            step_id=STEP_CONFIGURATION,
            data_schema=vol.Schema(schema),
            **step_args,
        )