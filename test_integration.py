"""
Unit tests and validation for the eNet Home Assistant integration.

These tests verify the structure and basic functionality of the integration.
They can be run with: python3 -m pytest test_integration.py -v
"""

import sys
import json
from pathlib import Path


def test_manifest_exists():
    """Test that manifest.json exists and is valid."""
    manifest_path = Path(__file__).parent / "custom_components/enet/manifest.json"
    assert manifest_path.exists(), "manifest.json not found"
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    assert manifest["domain"] == "enet"
    assert manifest["name"] == "eNet Smart Home"
    assert "config_flow" in manifest
    assert manifest["config_flow"] is True
    assert "version" in manifest


def test_hacs_json_exists():
    """Test that hacs.json exists and is valid."""
    hacs_path = Path(__file__).parent / "custom_components/enet/hacs.json"
    assert hacs_path.exists(), "hacs.json not found"
    
    with open(hacs_path) as f:
        hacs = json.load(f)
    
    assert hacs["name"] == "eNet Smart Home"
    assert "domains" in hacs
    assert "cover" in hacs["domains"]
    assert "light" in hacs["domains"]
    assert "sensor" in hacs["domains"]


def test_integration_files_exist():
    """Test that all required integration files exist."""
    integration_path = Path(__file__).parent / "custom_components/enet"
    
    required_files = [
        "__init__.py",
        "config_flow.py",
        "cover.py",
        "light.py",
        "sensor.py",
        "enet.py",
        "manifest.json",
        "hacs.json",
    ]
    
    for file_name in required_files:
        file_path = integration_path / file_name
        assert file_path.exists(), f"Missing file: {file_name}"


def test_init_py_structure():
    """Test that __init__.py has required structure."""
    init_path = Path(__file__).parent / "custom_components/enet/__init__.py"
    content = init_path.read_text()
    
    # Check for required constants
    assert 'DOMAIN' in content and '"enet"' in content, "DOMAIN not defined"
    assert "PLATFORMS" in content, "PLATFORMS not defined"
    assert "async_setup" in content, "async_setup function not defined"
    assert "async_setup_entry" in content, "async_setup_entry function not defined"
    assert "async_unload_entry" in content, "async_unload_entry function not defined"


def test_config_flow_structure():
    """Test that config_flow.py has required structure."""
    config_flow_path = Path(__file__).parent / "custom_components/enet/config_flow.py"
    content = config_flow_path.read_text()
    
    assert "EnetConfigFlow" in content, "EnetConfigFlow class not found"
    assert "async_step_user" in content, "async_step_user method not found"
    assert "CONF_HOST" in content, "CONF_HOST not used"
    assert "CONF_USERNAME" in content, "CONF_USERNAME not used"
    assert "CONF_PASSWORD" in content, "CONF_PASSWORD not used"


def test_cover_entity_structure():
    """Test that cover.py has required structure."""
    cover_path = Path(__file__).parent / "custom_components/enet/cover.py"
    content = cover_path.read_text()
    
    assert "EnetCover" in content, "EnetCover class not found"
    assert "CoverEntity" in content, "CoverEntity not imported"
    assert "current_cover_position" in content, "current_cover_position property not found"
    assert "async_close_cover" in content, "async_close_cover method not found"
    assert "async_open_cover" in content, "async_open_cover method not found"
    assert "async_set_cover_position" in content, "async_set_cover_position method not found"


def test_light_entity_structure():
    """Test that light.py has required structure."""
    light_path = Path(__file__).parent / "custom_components/enet/light.py"
    content = light_path.read_text()
    
    assert "EnetLight" in content, "EnetLight class not found"
    assert "LightEntity" in content, "LightEntity not imported"
    assert "is_on" in content, "is_on property not found"
    assert "brightness" in content, "brightness property not found"
    assert "async_turn_on" in content, "async_turn_on method not found"
    assert "async_turn_off" in content, "async_turn_off method not found"


def test_sensor_entity_structure():
    """Test that sensor.py has required structure."""
    sensor_path = Path(__file__).parent / "custom_components/enet/sensor.py"
    content = sensor_path.read_text()
    
    assert "EnetLightSensor" in content, "EnetLightSensor class not found"
    assert "EnetTemperatureSensor" in content, "EnetTemperatureSensor class not found"
    assert "SensorEntity" in content, "SensorEntity not imported"
    assert "native_value" in content, "native_value property not found"


def test_enet_client_exists():
    """Test that enet.py client library exists."""
    enet_path = Path(__file__).parent / "custom_components/enet/enet.py"
    content = enet_path.read_text()
    
    assert "EnetClient" in content, "EnetClient class not found"
    assert "get_devices" in content, "get_devices method not found"
    assert "simple_login" in content, "simple_login method not found"


def test_readme_updated():
    """Test that README has been updated for HA integration."""
    readme_path = Path(__file__).parent / "README.md"
    content = readme_path.read_text()
    
    assert "Home Assistant" in content, "README should mention Home Assistant"
    assert "custom_components" in content or "HACS" in content, "README should mention custom_components or HACS"
    assert "HAP-python" not in content, "README should not mention HAP-python"


def test_requirements_updated():
    """Test that requirements.txt has been updated."""
    req_path = Path(__file__).parent / "requirements.txt"
    content = req_path.read_text()
    
    assert "requests" in content, "requests library should be required"
    assert "HAP-python" not in content, "HAP-python should not be in requirements"


def test_no_homekit_files():
    """Test that HomeKit-specific files have been removed."""
    root = Path(__file__).parent
    
    assert not (root / "main.py").exists(), "main.py should be removed"
    assert not (root / "enet.state").exists(), "enet.state should be removed"
    
    # enet.py should only exist in custom_components
    assert not (root / "enet.py").exists(), "enet.py should only be in custom_components"


if __name__ == "__main__":
    print("Running eNet Home Assistant Integration Tests\n")
    print("=" * 60)
    
    tests = [
        ("Manifest JSON validation", test_manifest_exists),
        ("HACS JSON validation", test_hacs_json_exists),
        ("Integration files exist", test_integration_files_exist),
        ("__init__.py structure", test_init_py_structure),
        ("Config flow structure", test_config_flow_structure),
        ("Cover entity structure", test_cover_entity_structure),
        ("Light entity structure", test_light_entity_structure),
        ("Sensor entity structure", test_sensor_entity_structure),
        ("eNet client exists", test_enet_client_exists),
        ("README updated", test_readme_updated),
        ("Requirements updated", test_requirements_updated),
        ("HomeKit files removed", test_no_homekit_files),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✓ {test_name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_name}")
            print(f"  Unexpected error: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"\nResults: {passed} passed, {failed} failed")
    
    sys.exit(0 if failed == 0 else 1)
