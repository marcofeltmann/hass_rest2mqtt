# Contributing

## Development Setup

This repository contains a Home Assistant integration for REST services → MQTT.

## Deploying Changes to Home Assistant OS

### Using the deploy.sh script (recommended)

Copy the integration files to your HA device and restart HA using the `deploy.sh` script:

```bash
# With HA IP provided
./deploy.sh <ha-pi-ip-address>

# Or interactive version (prompts for HA IP)
./deploy.sh
```

The deployment script uses `rsync` to efficiently copy only changed files from your local development environment to the home-assistant device, then restarts Home Assistant.

### Using rsync manually (alternative)

If you prefer not to use the script, use this rsync command to copy the integration changes:

```bash
# Deploy entire integration
rsync -avz --delete custom_components/rest2mqtt/ root@ha-ip-address:/config/custom_components/rest2mqtt/
ssh root@ha-ip-address "ha core restart"

# For subsequent changes to individual files
rsync -avz custom_components/rest2mqtt/sensor.py root@ha-ip-address:/config/custom_components/rest2mqtt/
ssh root@ha-ip-address "ha core restart"
```

### rsync flags explained

Full rsync command:
```bash
rsync -avz --delete custom_components/rest2mqtt/ root@ha-ip-address:/config/custom_components/rest2mqtt/
```

**Flag breakdown:**

- `-a` — archive mode
  - Preserves file permissions, ownership, timestamps
  - Recursive copy (includes subdirectories)
  - Preserves symlinks

- `-v` — verbose
  - Shows which files are being transferred
  - Useful for debugging deployment issues

- `-z` — compress
  - Compresses data during transfer
  - Faster over network connections

- `--delete` — delete extraneous files
  - Removes files in destination not present locally
  - Keeps integration directory clean and up-to-date

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

1. Deploy to HA OS using `deploy.sh` script
2. Use the included test scenarios for manual testing
3. Check logs for any errors during setup

## Code Standards

- Follow Python 3.8+ syntax
- Use type hints throughout
- Include docstrings for all public methods
- Follow PEP 8 style guide
- Write comprehensive tests

## Getting Help

- [Home Assistant Integration Documentation](https://developers.home-assistant.io/docs/creating_integration_file_structure/)
- [Home Assistant GitHub](https://github.com/home-assistant)
- [Discord: home-assistant](https://discord.gg/c5D55pG)

## Support

For issues or questions:
- [GitHub Issues](https://github.com/home-assistant/core/issues)
- [Community Forum](https://community.home-assistant.io/)

## License

MIT