"""Support for eNet Smart Home cover devices (blinds/jalousies)."""
import logging
from typing import Any

from homeassistant.components.cover import CoverEntity, CoverDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_CLOSED, STATE_OPEN
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
    """Set up eNet cover entities from config entry."""
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
            if channel.channel_type == "CT_1F03":  # Blinds
                location = device.location.split(":")[-1]
                entities.append(
                    EnetCover(client, channel, f"Jalousie {location}")
                )

    async_add_entities(entities)


class EnetCover(CoverEntity):
    """Representation of an eNet blinds/jalousie cover."""

    _attr_device_class = CoverDeviceClass.BLIND
    _attr_has_entity_name = True

    def __init__(self, client: EnetClient, channel: Any, name: str) -> None:
        """Initialize the cover."""
        self._client = client
        self._channel = channel
        self._attr_name = name
        self._attr_unique_id = channel.uid

    @property
    def current_cover_position(self) -> int:
        """Return current position (0-100, where 100 is fully open)."""
        value = self._channel.get_value()
        # eNet uses 0-100 where 0 is open, 100 is closed
        # HA uses 0=closed, 100=open
        return 100 - value

    @property
    def is_closed(self) -> bool:
        """Return True if cover is closed."""
        return self.current_cover_position == 0

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the cover."""
        self._channel.set_value(100)
        self.async_write_ha_state()

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the cover."""
        self._channel.set_value(0)
        self.async_write_ha_state()

    async def async_set_cover_position(self, **kwargs: Any) -> None:
        """Set cover to specific position."""
        position = kwargs.get("position", 0)
        # Convert from HA (0=closed, 100=open) to eNet (0=open, 100=closed)
        enet_value = 100 - position
        self._channel.set_value(enet_value)
        self.async_write_ha_state()

    async def async_stop_cover(self, **kwargs: Any) -> None:
        """Stop the cover."""
        # eNet doesn't support stop, just update position
        self.async_write_ha_state()
