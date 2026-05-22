# Integration Testing Guide

## Quick Validation

Run the automated integration tests:

```bash
python3 test_integration.py
```

This validates:
- ✅ Manifest and HACS JSON structure
- ✅ All required files exist
- ✅ Code structure and required methods
- ✅ Configuration completeness
- ✅ HomeKit code removed

## Setup in Home Assistant (Development)

### Option 1: Local Testing with HACS

1. **Install Home Assistant** (if not already installed)
   ```bash
   # Using Docker (recommended)
   docker run -d \
     --name homeassistant \
     -p 8123:8123 \
     -v $(pwd)/config:/config \
     -v /etc/localtime:/etc/localtime:ro \
     homeassistant/home-assistant:latest
   ```

2. **Install HACS** in Home Assistant
   - Go to Settings → Devices & Services → Create Integration
   - Search for HACS and install

3. **Add Custom Repository**
   - In HACS, click "⋮" → Custom repositories
   - Add: `https://github.com/sweh/enet_homeassistant`
   - Category: Integration
   - Click Add

4. **Install eNet Integration**
   - In HACS, search "eNet"
   - Click "Install"
   - Restart Home Assistant

5. **Setup the Integration**
   - Go to Settings → Devices & Services → Create Integration
   - Select "eNet Smart Home"
   - Enter your eNet server details:
     - Host: `http://10.0.1.12` (or your eNet server IP)
     - Username: `admin` (or your username)
     - Password: (your eNet password)

### Option 2: Direct Installation (Development)

For faster iteration during development:

1. **Copy to custom_components**
   ```bash
   cp -r custom_components/enet ~/.homeassistant/custom_components/
   # or in Docker:
   docker cp custom_components/enet <container_id>:/config/custom_components/
   ```

2. **Restart Home Assistant**
   - Settings → Developer Tools → YAML
   - Click "Restart Home Assistant"

3. **Setup the Integration** (same as above)

## Testing with Mock Data

### Simulating Devices Without eNet Server

Edit `custom_components/enet/enet.py` temporarily to mock devices:

```python
# In get_devices() method, add mock data for testing:
def get_devices(self):
    """Get all the devices registered on the server"""
    # For testing without real server:
    # return self._create_mock_devices()
    
    # Regular implementation:
    device_locations = self.get_device_locations()
    # ... rest of code
```

## Debugging

### View Integration Logs

In Home Assistant:
1. Settings → System → Logs
2. Search for "enet"
3. Watch logs in real-time

### Enable Debug Logging

Add to `configuration.yaml`:
```yaml
logger:
  logs:
    custom_components.enet: debug
```

### Check Loaded Entities

1. Go to Settings → Devices & Services
2. Find "eNet Smart Home" integration
3. View all discovered entities

## Common Issues

### "Cannot Connect to eNet"
- ✅ Verify eNet server IP/hostname is correct
- ✅ Check network connectivity: `ping 10.0.1.12`
- ✅ Verify username/password are correct
- ✅ Check if eNet server is running and accessible

### "No Devices Found"
- ✅ Verify devices are configured in eNet server
- ✅ Check device channel types (must match supported types)
- ✅ Review Home Assistant logs for errors

### "Entity Not Updating"
- ✅ Check network connectivity
- ✅ Verify entity platform is loaded (Settings → Devices & Services)
- ✅ Increase update frequency in manifest.json if needed

## Performance Testing

Monitor entity updates:
1. Settings → Developer Tools → State
2. Search for entities starting with `cover.`, `light.`, `sensor.`
3. Watch `last_updated` timestamps

Expected update frequency:
- Cover/Light: Every 60 seconds
- Sensors: Every 120 seconds (configurable)

## Code Quality

### Python Linting

```bash
# Install pylint
pip3 install pylint

# Check code
pylint custom_components/enet/*.py
```

### Type Checking

```bash
# Install mypy
pip3 install mypy

# Check types
mypy custom_components/enet/
```

## Next Steps

1. ✅ Run `python3 test_integration.py` - All tests should pass
2. ✅ Set up test Home Assistant instance
3. ✅ Add eNet server credentials
4. ✅ Verify all device entities appear
5. ✅ Test control (cover open/close, light on/off)
6. ✅ Check state updates from eNet server

Once all tests pass, the integration is ready for production use!
