#!/bin/bash

# Deploy HA integration to Raspberry Pi running Home Assistant OS
# Usage: ./deploy.sh

# Check if running on Linux/macOS (required for rsync)
if [[ "$OSTYPE" != "linux-gnu"* ]] && [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: rsync is only available on Linux and macOS"
    exit 1
fi

HA_USER="homeassistant"

if [[ -z $HA_IP ]]; then # HomeAssistant IP envvar missing
  # Get HA Pi IP from argument or prompt
  if [[ -n "$1" ]]; then # First Script Parameter set
    HA_IP="$1"
  else
    read -p "Enter HA Pi IP address: " HA_IP
  fi
fi

# Check if rsync is available
if ! command -v rsync &> /dev/null; then
    echo "Error: rsync is not installed"
    echo "Install with: sudo apt install rsync (Debian/Ubuntu) or brew install rsync (macOS)"
    exit 1
fi

# Check if ssh is available
if ! command -v ssh &> /dev/null; then
    echo "Error: ssh is not available"
    exit 1
fi

# Check if source directory exists
if [[ ! -d "custom_components/rest2mqtt" ]]; then
    echo "Error: custom_components/rest2mqtt/ directory not found"
    echo "Make sure you're running this from the integration root directory"
    exit 1
fi

# Backup existing integration (optional)
# TODO: Should be done on remote device.
echo "=== Backing up existing integration ==="
if [[ -d "/config/custom_components/rest2mqtt" ]]; then
    echo "Backing up to /config/custom_components/rest2mqtt.backup"
    cp -r /config/custom_components/rest2mqtt /config/custom_components/rest2mqtt.backup 2>/dev/null || echo "Backup not needed or failed"
fi

# Copy integration to HA OS

echo "=== Deploying REST2MQTT integration ==="
echo "From: $(pwd)/custom_components/rest2mqtt/"
echo "To: $HA_USER@$HA_IP:/config/custom_components/rest2mqtt/"
echo ""
echo "Running: rsync -avz --delete custom_components/rest2mqtt/ $HA_USER@$HA_IP:/config/custom_components/rest2mqtt/"
echo ""
rsync -avz --delete custom_components/rest2mqtt/ $HA_USER@$HA_IP:/config/custom_components/rest2mqtt/

if [[ $? -ne 0 ]]; then
    echo ""
    echo "Error: Failed to copy files"
    echo "Make sure SSH is running on your Pi and root access is configured"
    exit 1
fi

echo ""
echo "=== Restarting Home Assistant ==="
echo "Running: ssh $HA_USER@$HA_IP \"ha core restart\""
ssh $HA_USER@$HA_IP "ha core restart"

if [[ $? -ne 0 ]]; then
    echo ""
    echo "Error: Failed to restart HA"
    echo "Check your HA Pi's status"
    exit 1
fi

echo ""
echo "=== Deployment complete ==="
echo "Your REST2MQTT integration has been successfully deployed to Home Assistant OS"
echo ""
echo "To verify the integration was loaded:"
echo "  ssh $HA_USER@$HA_IP \"tail -f /config/home-assistant.log\""
echo "Then filter for: REST2MQTT"
