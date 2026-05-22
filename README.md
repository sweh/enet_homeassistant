# Home Assistant eNet Smart Home Integration

[Home Assistant](https://www.home-assistant.io/) integration for [eNet smart home](https://www.enet-smarthome.com/de/ueber-enet/) devices from Jung/Gira.

This integration allows you to control and monitor:
* Window coverings (blinds/jalousies)
* Lights and dimmers
* Light sensors
* Temperature sensors

## Quick Start (HACS)

1. **HACS** → Custom repositories → Add `https://github.com/sweh/enet_homeassistant` (Category: Integration)
2. **HACS** → Integrations → Search "eNet" → Install
3. **Restart** Home Assistant
4. **Settings** → Devices & Services → Create Integration → eNet Smart Home
5. Enter your eNet server credentials
6. Done! 🎉

👉 [Detailed HACS Installation Guide](HACS_INSTALLATION.md)

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Custom repositories"
3. Add repository URL: `https://github.com/sweh/enet_homeassistant`
4. Select "Integration" as category
5. Click "Install"
6. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/enet` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

Add your eNet server to Home Assistant:

1. Go to Settings → Devices & Services
2. Click "Create Integration"
3. Select "eNet Smart Home"
4. Enter your eNet server details:
   * Host: IP address or hostname of your eNet server (e.g., `http://10.0.1.12`)
   * Username: eNet server username (default: `admin`)
   * Password: eNet server password

## Supported Devices

### Window Coverings
* Jalousien (blinds)

### Lights
* Switches (Schalten)
* Dimmers (brightness control)

### Sensors
* Light sensors (illuminance)
* Temperature sensors

## Testing

- 🧪 [Testing Guide](TESTING.md) - Local testing with mock server
- 🚀 [Quick Start Guide](TEST_QUICKSTART.md) - Fast validation commands

## References

* [eNet Smart Home Documentation](https://www.enet-smarthome.com/de/ueber-enet/)
* [Home Assistant Developer Docs](https://developers.home-assistant.io/)
* Based on [enet-homeassistant](https://github.com/mnordseth/enet-homeassistant)

