# REST2MQTT

Home Assistant integration to call multiple REST services, store selected JSON data into an MQTT server, and provide sensors for each data selection in Home Assistant.

<!-- @todo Update with emoji support -->

## Overview

REST2MQTT is a Home Assistant custom integration designed to:

- Call multiple REST services/APIs
- Parse and filter the JSON responses
- Store the selected data in an MQTT server
- Make the data available through Home Assistant sensors for automation and visualization

The integration provides a unified way to integrate external API data into your Home Assistant ecosystem, making it easy to use data from various services in your automations and dashboards.

## Quickstart

### 1. Prerequisites

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or use the development environment
pip install -e .[dev]
```

### 2. Local Testing with Docker

```bash
# Build and start the development environment
docker-compose up -d

# The integration should be available for local testing
```

### 3. Testing on Home Assistant OS

To test this integration on a Raspberry Pi running Home Assistant OS:

```bash
# Deploy the integration to your HA device
./deploy.sh <ha-pi-ip-address>

# Or use interactive mode (will prompt for IP)
./deploy.sh
```

The deployment script uses `rsync` to efficiently copy only the changed files from your local development environment to the home-assistant device, followed by a restart of Home Assistant.

**Explore Test Scenarios - Run this command**
```bash
# Open test scenarios for manual testing
echo "Open the interactive scenarios in your browser"
```

### 4. Verify Integration

After deployment, check HA logs to verify the integration loaded:

```bash
ssh root@<ha-pi-ip-address> "tail -f /config/home-assistant.log" | grep REST2MQTT
```

## Project Structure

```
custom_components/rest2mqtt/
├── __init__.py           # Main integration entry point
├── config_flow.py        # User configuration flow
├── const.py              # Constants and configuration keys
├── coordinator.py        # Data Update Coordinator for polling
├── manifest.json         # Integration metadata
├── sensor.py             # Sensor platform implementation
├── services.py           # Service handlers
├── strings.json          # UI strings for config flow
└── translations/         # Multi-language support
    └── en.json          # English translations
```

## Key Files

### Manifest (`manifest.json`)
```json
{
  "domain": "rest2mqtt",
  "name": "REST2MQTT",
  "codeowners": ["@marcofeltmann"],
  "config_flow": true,
  "documentation": "https://github.com/marcofeltmann/hass_rest2mqtt",
  "iot_class": "cloud_polling",
  "requirements": ["paho-mqtt>=1.6.0", "aiohttp>=3.8.0"],
  "version": "1.0.0"
}
```

### Main Integration (`__init__.py`)
- Handles setup/unload of configuration entries
- Manages the integration lifecycle
- Uses standard Home Assistant patterns

### Configuration Flow (`config_flow.py`)
- Provides user interface for configuring REST2MQTT
- Handles MQTT connection parameters
- Includes validation and error handling

### Data Coordinator (`coordinator.py`)
- Uses `DataUpdateCoordinator` for efficient polling
- Handles REST service calls and data caching
- Provides error handling and retry logic

### Sensors (`sensor.py`)
- Implements sensor platforms for Home Assistant
- Provides real-time data updates
- Supports multiple sensor types

## Configuration

### In Home Assistant Configuration

Configure the integration in your `configuration.yaml`:

```yaml
rest2mqtt:
  host: "your-mqtt-server.com"
  port: 1883
  rest_services:
    - name: "weather_api"
      url: "https://api.weather.com/data"
      headers:
        Authorization: "Bearer your_api_key"
      parse_path: ["data", "temperature"]
      update_interval: 300  # seconds
    - name: "sensor_data"
      url: "https://api.example.com/sensor"
      headers:
        X-API-Key: "your_key"
```

### User Configuration Flow

Users configure the integration through a web UI that includes:

- MQTT server connection settings
- REST service definitions (URL, headers, parsing paths)
- Update intervals
- Data filtering and validation

## Services

### `rest2mqtt.publish_data`
Publish data to MQTT topics from Home Assistant scripts.

**Parameters:**
- `service_name` (required): Target MQTT service name
- `message` (required): Data to publish
- `topic` (optional): Custom MQTT topic override

**Example:**
```yaml
alias: Publish weather update
service: rest2mqtt.publish_data
target:
  entity_id: sensor.rest2mqtt_weather_data
data:
  service_name: "weather"
  message: "Temperature is 75°F"
```

## Testing

### Unit Tests

Run the full test suite:

```bash
# Run pytest
pytest

# Run specific test files
pytest test_integration.py
pytest test_config_flow.py
pytest test_sensor.py
```

### Integration Tests

For end-to-end testing with Home Assistant:

1. Deploy to HA OS using the `deploy.sh` script
2. Use the included test scenarios for manual testing
3. Check logs for any errors during setup

## Development

### Running the Dev Environment

This project uses Docker for isolated development:

```bash
docker-compose up -d   # Start with code hot-reload
docker-compose down   # Stop and clean up
```

### Using Hatch for Environment Management

The project uses Hatch for dependency management and testing:

```bash
# Run tests
hatch run test

# Run linting
hatch run lint

# Run type checking
hatch run type-check

# Run all checks
hatch run test lint type-check
```

### Developing and Testing Integration

To develop and test the integration locally, use the following steps:

1. Make changes to your integration files in `custom_components/rest2mqtt/`
2. Run tests to ensure changes work correctly
3. Deploy changes to HA OS using the deployment script
4. Verify the integration loads correctly in HA logs
5. Test the integration through the UI or automations

## Best Practices

1. **Use the coordinator pattern** for efficient polling of REST services
2. **Implement proper error handling** with try-except blocks
3. **Follow Python typing standards** for better code readability
4. **Use logging** for debugging and monitoring
5. **Write tests** for all integration components
6. **Use constants** for magic numbers and values

## Future Enhancements

- [ ] Add multiple sensor types (binary_sensor, switch, etc.)
- [ ] Implement polling configuration per service
- [ ] Add support for WebSocket APIs
- [ ] Implement data transformation and filtering
- [ ] Add Home Assistant dashboards support (lovelace)
- [ ] Implement integration quality scale (Bronze → Gold → Platinum)

## Contributions

Contributions are welcome! Please read the contributing guide for detailed instructions.

## Support

For issues or questions:
- [GitHub Issues](https://github.com/marcofeltmann/hass_rest2mqtt/issues)
- [Home Assistant Forums](https://community.home-assistant.io/)

## License

AGPLv3, see @LICENSE
