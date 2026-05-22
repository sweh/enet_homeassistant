"""Config flow for eNet Smart Home integration."""
import asyncio
import logging
from typing import Any, Dict, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .enet import EnetClient

_LOGGER = logging.getLogger(__name__)

DOMAIN = "enet"


class EnetConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for eNet Smart Home integration."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle a flow initiated by the user."""
        if user_input is not None:
            errors = {}
            try:
                client = EnetClient(
                    user_input[CONF_HOST],
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                )
                await asyncio.to_thread(client.simple_login)
            except Exception as err:
                _LOGGER.error("Failed to connect to eNet: %s", err)
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(
                    user_input[CONF_HOST].replace("http://", "").replace("https://", "")
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input,
                )

            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_HOST): str,
                        vol.Required(CONF_USERNAME, default="admin"): str,
                        vol.Required(CONF_PASSWORD): str,
                    }
                ),
                errors=errors,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME, default="admin"): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
        )
