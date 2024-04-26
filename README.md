# ha-twilio
A standalone HACS-ready Twilio Home Assistant integration for making calls with arbitrary TwiML execution.

## Why use this over the core integration

 - Config flow setup via the UI
 - The ability to execute arbitrary TwiML code (rather than just TTS or `POST` accessed TwiML)

### Disadvantages compared to core

 - No webhooks for triggering events based on calls
 - Less convenient for simple TTS (I'm planning on adding a Notify entity once they're fully supported in HA rather than adding the legacy service now)
 - No SMS (also waiting on Notify entities)

## Installation 

In HACS, you'll need to add this repo as a custom repo, then restart. You'll then be able to add the integration normally via the UI. For more details on how to setup, see below.

## Setup

You'll need your account SID, auth token and the number you want to call from. You can add multiple config entries for the same account with different phone numbers.

## Usage

Call the `twilio_command.make_call service`. Choose your account/number, a target number, a url with your TwiML code and the http method to access it (usually `GET`).

For example, I have an automation that calls a gate keypad and presses `#` to open the gate using a very basic TwiML file hosted here: https://github.com/JakeMartin-ICL/twilio-twimls/blob/gate-control/gate-control.xml