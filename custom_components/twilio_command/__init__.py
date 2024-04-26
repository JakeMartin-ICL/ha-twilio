"""The twilio_call component."""

from __future__ import annotations

import logging

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, callback

from .const import ACCOUNT_SID, AUTH_TOKEN, DOMAIN, FROM_NUMBER, MAKE_CALL_SERVICE
from .data import TwilioCommandData

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Get the Twilio Call notification service."""

    hass.data.setdefault(DOMAIN, {})
    number = entry.data[FROM_NUMBER]
    client = Client(entry.data[ACCOUNT_SID], entry.data[AUTH_TOKEN])
    hass.data[DOMAIN][entry.entry_id] = TwilioCommandData(client, number)

    try:
        account_instance = await hass.async_add_executor_job(client.api.account.fetch)
        hass.config_entries.async_update_entry(
            entry, title=f"{account_instance.friendly_name}: {number}"
        )
    except TwilioRestException as exc:
        _LOGGER.error(exc)

    @callback
    async def handle_call(call: ServiceCall) -> None:
        """Call to specified target users."""

        config_data: TwilioCommandData = hass.data[DOMAIN][call.data[FROM_NUMBER]]
        target = call.data["target_number"]
        twiml_url = call.data["twiml_url"]
        twiml_method = call.data.get("twiml_method", "GET")

        def make_call():
            config_data.client.calls.create(
                to=target,
                url=twiml_url,
                method=twiml_method,
                from_=config_data.from_number,
            )

        try:
            await hass.async_add_executor_job(make_call)
        except TwilioRestException as exc:
            _LOGGER.error(exc)

    hass.services.async_register(DOMAIN, MAKE_CALL_SERVICE, handle_call)

    return True
