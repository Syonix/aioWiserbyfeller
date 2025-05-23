# Wiser by Feller API Async Python Library
[![aioWiserbyfeller](https://github.com/Syonix/aioWiserbyfeller/actions/workflows/python-app.yml/badge.svg)](https://github.com/Syonix/aioWiserbyfeller/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/Syonix/aioWiserbyfeller/graph/badge.svg?token=VU0MZKEMPM)](https://codecov.io/gh/Syonix/aioWiserbyfeller)
![PyPI - Version](https://img.shields.io/pypi/v/aioWiserbyfeller)
![GitHub License](https://img.shields.io/github/license/Syonix/aioWiserByFeller)

A modern async Python library to control and integrate **Wiser by Feller** smart light switches, cover controls, and scene buttons, hvac controls and weather stations into your Python applications.

> [!IMPORTANT]
> This integration implements [Wiser by Feller](https://wiser.feller.ch) and not [Wiser by Schneider Electric](https://www.se.com/de/de/product-range/65635-wiser/), which is a competing Smart Home platform (and is not compatible). It is even more confusing, as Feller (the company) is a local subsidiary of Schneider Electric, catering only to the Swiss market.

> [!CAUTION]
> **Warning:** This project is under **_heavy development_** and does not yet have a stable release. Expect breaking changes in susequent beta releases. All breaking changes will be documented in the [release notes](https://github.com/Syonix/aioWiserbyfeller/releases) including resultion advisories.

## 📦 Installation
```bash
pip install aiowiserbyfeller
```

## 🧑‍💻 Usage
```python
import asyncio
import aiohttp
from aiowiserbyfeller import Auth, WiserByFellerAPI

async def main():
    async with aiohttp.ClientSession() as session:
        auth = Auth(session, "192.168.0.42")  # Replace with the IP of your µGateway
        api = WiserByFellerAPI(auth)
        info = await api.async_get_info()
        print(info)

asyncio.run(main())
```

## 🧰 Basic Functionality
Wiser by Feller devices (except hvac controllers and weather stations) consist of two parts: The control front and the base module. There are switching base modules (for light switches and cover controllers) and non-switching base modules (for scene buttons and secondary controls).

Because the functionality changes when the same base module is used with a different front, the combination of the two is considered an unique device.

Devices are connected with each other by a proprietary [K+ bus system](https://www.feller.ch/de/connected-buildings/wiser-by-feller/installation-inbetriebnahme). One (and only one) device acts as a WLAN gateway (called µGateway) to interface with the system.

Learn more about Wiser devices on the [official website](https://wiser.feller.ch) and [API documentation](https://github.com/Feller-AG/wiser-tutorial).

## 🚀 Features
Here's what this library offers:

### ✨ Easy to use framework
The library abstracts API functionality and allows for easy authentication, interaction with devices and data validation. Work with device classes, allowing for strongly typed implementations. Helper methods and properties abstract as much complexity of the API as possible, while retaining full flexibility.

### 🚨 Status LEDs
Each front features a configurable RGB LED edge for their buttons, that you would normally configure in the [Wiser Home app](https://www.feller.ch/de/feller-apps). They can be configured in color and brightness. For buttons controlling a load, there can be two different brightnesses: One for if the load is on and one for if it is off. For others (e.g. scene buttons) there can only be one brightness, as there is no logical "on" state.

The library offers an intuitive way to update status LEDs without the need for complex back and forth with the API, allowing you to use them to represent other information than just the device state (e.g. completion of the washing machine program or motion in another room).

> [!IMPORTANT]
> Due to the implementation on the devices, the status light is not suited for fast updating, as multiple slow API calls are necessary.

### 🔌 WebSockets
The µGateway offers a Websocket connection, allowing for instant updates about state changes. This library offers a convenient way to establish a connection and tap into the update notifications.

### 🧪 **Robust test suite**
Extensive unit test coverage ensures high stability and confidence even if new functionality is added.

## ⚠️ Known Limitations
- The µGateway supports **REST and WebSockets only**. MQTT exists but is [not publicly accessible](https://github.com/Feller-AG/wiser-tutorial/issues/5).
- Device names appear in **German only**, due to limited international support.
- Status LED updates are **slow**, as they require multiple API calls.

## 🔗 Related Projects
- Check out the [Home Assistant integration](https://github.com/Syonix/ha-wiser-by-feller) built using this library.

## 🤝 Contributing
We welcome contributions! To get started:

1. Create a virtual environment: `python -m venv .venv`
2. Install dependencies: `pip install ".[test]"`
3. Make your changes.
4. Write or update unit tests.
5. Run tests with `pytest`
6. Open a Pull Request 🎉
