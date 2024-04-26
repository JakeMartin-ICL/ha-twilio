"""Dataclass for Monzo data."""

from dataclasses import dataclass

from twilio.rest import Client


@dataclass
class TwilioCommandData:
    """A dataclass for holding data stored in hass.data."""

    client: Client
    from_number: str
