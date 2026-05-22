"""Support for eNet Smart Home sensor entities."""
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN
from .enet import EnetClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up eNet sensor entities from config entry."""
    client: EnetClient = hass.data[DOMAIN][config_entry.entry_id]

    try:
        devices = client.get_devices()
    except Exception as err:
        _LOGGER.error("Failed to fetch eNet devices: %s", err)
        return

    entities = []
    for device in devices:
        if not device.channels:
            continue

        for channel in device.channels:
            # Light sensors
            if channel.channel_type == "CT_1F18":
                location = device.location.split(":")[-1]
                entities.append(
                    EnetLightSensor(client, channel, f"Light Level {location}")
                )
            # Temperature sensors
            elif channel.channel_type in ("CT_1F19", "CT_TADO_ZH", "CT_TADO_ZAC", "CT_TADO_ZHW"):
                location = device.location.split(":")[-1]
                entities.append(
                    EnetTemperatureSensor(client, channel, f"Temperature {location}")
                )

    async_add_entities(entities)


class EnetLightSensor(SensorEntity):
    """Representation of an eNet light sensor."""

    _attr_device_class = SensorDeviceClass.ILLUMINANCE
    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = "lx"

    def __init__(self, client: EnetClient, channel: Any, name: str) -> None:
        """Initialize the sensor."""
        self._client = client
        self._channel = channel
        self._attr_name = name
        self._attr_unique_id = channel.uid

    @property
    def native_value(self) -> float | None:
        """Return the current illuminance value."""
        try:
            return float(self._channel.get_value())
        except (ValueError, TypeError):
            return None


class EnetTemperatureSensor(SensorEntity):
    """Representation of an eNet temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = "°C"

    def __init__(self, client: EnetClient, channel: Any, name: str) -> None:
        """Initialize the sensor."""
        self._client = client
        self._channel = channel
        self._attr_name = name
        self._attr_unique_id = channel.uid

    @property
    def native_value(self) -> float | None:
        """Return the current temperature value."""
        try:
            return float(self._channel.get_value())
        except (ValueError, TypeError):
            return None
