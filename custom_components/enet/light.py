"""Support for eNet Smart Home light entities."""
import asyncio
import logging
from typing import Any

from homeassistant.components.light import LightEntity, ColorMode
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
    """Set up eNet light entities from config entry."""
    client: EnetClient = hass.data[DOMAIN][config_entry.entry_id]

    try:
        devices = await asyncio.to_thread(client.get_devices)
    except Exception as err:
        _LOGGER.error("Failed to fetch eNet devices: %s", err)
        return

    entities = []
    for device in devices:
        if not device.channels:
            continue

        for channel in device.channels:
            # Dimmers and switches
            if channel.channel_type in ("CT_1F01", "CT_1F02", "CT_1F05", "CT_1F08", "CT_1F09"):
                location = device.location.split(":")[-1]
                is_dimmable = channel.has_brightness
                entities.append(
                    EnetLight(client, channel, f"Light {location}", is_dimmable)
                )

    async_add_entities(entities)


class EnetLight(LightEntity):
    """Representation of an eNet light/switch."""

    _attr_has_entity_name = True

    def __init__(
        self,
        client: EnetClient,
        channel: Any,
        name: str,
        is_dimmable: bool = False,
    ) -> None:
        """Initialize the light."""
        self._client = client
        self._channel = channel
        self._attr_name = name
        self._attr_unique_id = channel.uid
        self._is_dimmable = is_dimmable
        self._cached_value = channel.state  # Cache initial state

        if is_dimmable:
            self._attr_color_mode = ColorMode.BRIGHTNESS
            self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
        else:
            self._attr_color_mode = ColorMode.ONOFF
            self._attr_supported_color_modes = {ColorMode.ONOFF}

    @property
    def brightness(self) -> int | None:
        """Return brightness level (0-255)."""
        if not self._is_dimmable:
            return None
        # Use cached value to avoid blocking call
        value = self._cached_value
        # Convert from 0-100 to 0-255
        return int(value * 255 / 100)

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        # Use cached value to avoid blocking call
        return self._cached_value > 0

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""
        if "brightness" in kwargs:
            brightness = kwargs["brightness"]
            # Convert from 0-255 to 0-100
            value = int(brightness * 100 / 255)
            await asyncio.to_thread(self._channel.set_value, value)
            self._cached_value = value
        else:
            await asyncio.to_thread(self._channel.set_value, 100)
            self._cached_value = 100
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        await asyncio.to_thread(self._channel.set_value, 0)
        self._cached_value = 0
        self.async_write_ha_state()
