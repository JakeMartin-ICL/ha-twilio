"""Config flow for the Twilio Command integration."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
import homeassistant.helpers.config_validation as cv

from .const import ACCOUNT_SID, AUTH_TOKEN, DOMAIN, FROM_NUMBER


class TwilioCommandConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Twilio Command config flow."""

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Perform main step of config flow."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[FROM_NUMBER],
                data={
                    ACCOUNT_SID: user_input[ACCOUNT_SID],
                    AUTH_TOKEN: user_input[AUTH_TOKEN],
                    FROM_NUMBER: user_input[FROM_NUMBER],
                },
            )

        data_schema = {
            vol.Required(ACCOUNT_SID): cv.string,
            vol.Required(AUTH_TOKEN): cv.string,
            vol.Required(FROM_NUMBER): cv.string,
        }

        return self.async_show_form(step_id="user", data_schema=vol.Schema(data_schema))
