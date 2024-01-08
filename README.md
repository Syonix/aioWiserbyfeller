# Wiser by Feller API Async Python Library
[![aioWiserbyfeller](https://github.com/Syonix/aioWiserbyfeller/actions/workflows/python-app.yml/badge.svg)](https://github.com/Syonix/aioWiserbyfeller/actions/workflows/python-app.yml)

Use your Wiser by Feller smart light switches, cover controls and scene buttons in your python project.

**Beware:** This integration implements [Wiser by Feller](https://wiser.feller.ch) and not [Wiser by Schneider Electric](https://www.se.com/de/de/product-range/65635-wiser/), which is a competing Smart Home platform (and is not compatible). It es even more confusing, as Feller (the company) is a local subsidiary of Schneider Electric, catering only to the Swiss market.

## Functionality
### Devices
Wiser by Feller devices always consist of two parts: The control front and the base module. There are switching base modules (for light switches and cover controllers) and non-switching base modules (for scene buttons and secondary controls).

Because the functionality changes when the same base module is used with a different front, the combination of the two is considered an unique device.

Devices are connected with each other by a proprietary [K+ bus system](https://www.feller.ch/de/connected-buildings/wiser-by-feller/installation-inbetriebnahme). One (and only one) device acts as a WLAN gateway (called µGateway) to interface with the system.

### Status LEDs
Each front features a configurable RGB LED edge for their buttons. Normally you would configure those in the [Wiser Home app](https://www.feller.ch/de/feller-apps). They can be configured in color and brightness. For buttons controlling a load, there can be two different brightnesses: One for if the load is on and one for if it is off. For others (e.g. scene buttons) there can only be one brightness, as there is no logical "on" state. 

**Note:** Due to the implementation on the devices, the status light is not suited for fast updating, as multiple slow API calls are necessary.

## Known issues
- As of right now, the µGateway API only supports Rest and Websockets. MQTT is implemented, [but only for the proprietary app](https://github.com/Feller-AG/wiser-tutorial/issues/5).
- Note: device names are in German because manufacturer does not have an English online presence.