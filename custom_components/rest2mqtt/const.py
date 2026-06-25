"""Constants for REST2MQTT integration."""

DOMAIN = "rest2mqtt"

LOGGER_NAME = DOMAIN

CONF_RESTORE_STATE = "restore_state"
CONF_RESTORE_STATE_DEFAULT = False

CONF_HOST = "host"
CONF_PORT = "port"
CONF_RESTORE = "restore"
CONF_REST_SERVICES = "rest_services"

DEFAULT_HOST = "mqtt.example.com"
DEFAULT_PORT = 1883
DEFAULT_RESTORE = False

MQTT_CLIENT_ID_BASE = DOMAIN

SERVICE_MQTT_PUBLISH = f"{DOMAIN}_publish"