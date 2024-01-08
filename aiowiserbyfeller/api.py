"""Wrapper for Wiser by Feller API"""
from __future__ import annotations

from typing import List

from .auth import Auth
from .device import Device
from .errors import InvalidLoadType
from .job import Job
from .load import Dali, DaliRgbw, DaliTw, Dim, Load, Motor, OnOff
from .scene import Scene
from .smart_button import SmartButton
from .system import SystemFlag, SystemCondition
from .time import NtpConfig
from .timer import Timer
from .util import validate_str


class WiserByFellerAPI:
    """Class to communicate with the Feller Wiser µGateway API. More
    details regarding specific payloads are documented on
    https://feller-ag.github.io/wiser-api/"""

    # pylint: disable=too-many-public-methods

    def __init__(self, auth: Auth):
        self.auth = auth

    # -- Device Info ---------------------------------------------------

    async def async_get_info(self) -> dict:
        """Get important information about components of the µGateway
        device. Version strings have the full format MAJOR.MINOR.PATCH
        or shorter. MAJOR, MINOR and PATCH are integers without leading
        zeros and each strictly increasing with time."""
        return await self.auth.request("get", "info", require_token=False)

    async def async_get_info_debug(self) -> dict:
        """Get detailed information for testing and debugging a µGateway
        device. Version strings have the full format MAJOR.MINOR.PATCH
        or shorter. MAJOR, MINOR and PATCH are integers without leading
        zeros and each strictly increasing with time. Git hashes are
        shortened to first few digits, and end with -dirty if the build
        includes uncommitted changes. Time strings are in ISO 8601
        format YYYY-MM-DDThh:mm:ss."""
        return await self.auth.request("get", "info/debug", require_token=False)

    # -- Time ----------------------------------------------------------

    async def async_get_time_now(self) -> dict:
        """Get the current system time of the device and the uptime
        since last startup.
        System time strings are in ISO 8601 format YYYY-MM-DDThh:mm:ss."""
        return await self.auth.request("get", "time/now")

    async def async_set_time_now(self, utc: str) -> dict:
        """System time strings are in ISO 8601 format YYYY-MM-DDThh:mm:ss.
        The value of uptime is read-only!"""
        data = {"utc": utc}
        return await self.auth.request("put", "time/now", json=data)

    async def async_get_time_ntp_config(self) -> NtpConfig:
        """Read the current NTP configuration."""
        data = await self.auth.request("get", "time/ntpconfig")
        return NtpConfig(data, self.auth)

    async def async_set_time_ntp_config(self, interval: int, urls: list) -> NtpConfig:
        """Set a new NTP configuration. The existing urls-array is
        replaced by the new one! If an URL in the new array occurs more
        than once then all copies after the first will be removed."""
        data = await self.auth.request(
            "put", "time/ntpconfig", json={"interval": interval, "urls": urls}
        )
        return NtpConfig(data, self.auth)

    async def async_patch_time_ntp_config(self, data: dict) -> NtpConfig:
        """Set a new interval and/or prepend new entries to the URLs
        array. If an URL in the new array occurs more than once then all
        copies after the first will be removed."""

        data = await self.auth.request("patch", "time/ntpconfig", json=data)
        return NtpConfig(data, self.auth)

    async def async_get_time_sun_info(self) -> dict:
        """The current implementation assumes that you are at the center
        of Switzerland!"""
        return await self.auth.request("get", "time/suninfo")

    async def async_get_time_sun_info_date(self, date: str) -> dict:
        """Calculate the sunrise and sunset times of today. Calculate
        the sunrise and sunset times on a specific date. The current
        implementation assumes that you are at the center of
        Switzerland! The date string is formatted in ISO 8601 format
        YYYY-mm-dd"""
        return await self.auth.request("get", f"time/suninfo/{date}")

    # -- Network -------------------------------------------------------

    async def async_get_net_scan(self) -> list:
        """Return connectable WLAN routers in range. Scan the wireless
        environment for connectible WLAN access-points in range. Each
        scan will take approximately 5 seconds! The response is an array
        of objects, each with ssid, bssid, sec, channel and rssi."""
        return await self.auth.request("get", "net/scan")

    async def async_get_net_mdns(self) -> list:
        """Get all hosts of all service types that were discovered since
        last reboot. In access-point mode the hostname, IP address and
        port of the µGateway itself can be found under http, lisa and
        zapp."""
        return await self.auth.request("get", "net/mdns")

    async def async_broadcast_net_mdns(self, service: str) -> list:
        """Broadcast a MDNS Service Discovery to the connected WLAN to
        discover new service hosts. Then get all hosts of all service
        types that were discovered since last reboot. In access-point
        mode the hostname, IP address and port of the µGateway itself
        can be found under http, lisa and zapp."""

        validate_str(
            service,
            ["http", "lisa", "zapp"],
            error_message="Invalid mdns service value",
        )

        return await self.auth.request("post", "net/mdns", json={"service": service})

    async def async_get_net_wlans(self) -> list[dict]:
        """Get an array of all stored WLAN configurations."""
        return await self.auth.request("get", "net/wlans")

    async def async_get_create_wlan_config(
        self, ssid: str, sec: str, password: str
    ) -> dict:
        """Create a new WLAN configuration. A configuration must have at
        least a non-empty ssid or bssid. The password must be missing or
        empty if sec is missing or OPEN. For all other values of sec a
        valid password must be set."""
        config = {"ssid": ssid, "sec": sec, "password": password}
        return await self.auth.request("post", "net/wlans", json=config)

    async def async_delete_wlan_configs(self):
        """Delete all WLAN configurations. During next reboot the order
        list of Current State will be cleared and the µGateway starts in
        access-point mode!"""
        return await self.auth.request("delete", "net/wlans")

    async def async_get_net_wlan(self, wlan_id: int) -> dict:
        """Get one WLAN configuration with all its properties."""
        return await self.auth.request("get", f"net/wlans/{wlan_id}")

    async def async_replace_net_wlan_config(self, config_id: int, config: dict) -> dict:
        """Replace an existing WLAN configuration with a completely new
        one. The new values may be empty strings. Missing properties are
        set to default values. The new WLAN configuration has the same
        limitations as explained in section POST /wlans."""
        return await self.auth.request("put", f"net/wlans/{config_id}", json=config)

    async def async_update_net_wlan(self, config_id: int, config: dict) -> dict:
        """Patch some new values into an existing WLAN configuration.
        The new values may be empty strings. The resulting WLAN
        configuration has the same limitations as explained in section
        POST /wlans."""
        return await self.auth.request("put", f"net/wlans/{config_id}", json=config)

    async def async_delete_net_wlan(self, config_id: int) -> dict:
        """Delete a WLAN configuration. The response contains the
        deleted WLAN configuration."""
        return await self.auth.request("delete", f"net/wlans/{config_id}")

    async def async_get_net_state(self) -> dict:
        """Read the current network state."""
        return await self.auth.request("get", "net/state")

    async def async_set_net_state(self, state: dict) -> dict:
        """Set a new network state. If an optional key is missing then
        its value is reset to default. The existing order array is
        replaced by the new one. If an id in the new order array occurs
        more than once then all copies after the first will be removed.
        Attention: The property https is for future use, do not change
        it!"""
        return await self.auth.request("put", "net/state", json=state)

    async def async_update_net_state(self, state: dict) -> dict:
        """Change values in the network state. If an optional key is
        missing then its value stays unchanged. The existing order array
        is appended at the end of the new one to build a combined array.
        If an id in the combined order array occurs more than once then
        all copies after the first will be removed. Attention: The
        property https is for future use, do not change it!"""
        return await self.auth.request("patch", "net/state", json=state)

    async def async_get_net_rssi(self) -> int:
        """Return the current RSSI in dBm. This read-only service
        returns the Received Signal Strength Indication of the µGateway
        device. A RSSI from -1 to -49 means good and from -50 to -69 the
        link quality is ok. A RSSI beyond -70 may lead to delayed
        responses or even WLAN disassociation! Warning: It is only
        possible to get the RSSI in router mode, alias station mode!
        Getting the RSSI in access-point mode will raise an error."""
        data = await self.auth.request("get", "net/rssi")
        return data["rssi"]

    async def async_get_hostname(self) -> str:
        """Return hostname of µGateway."""
        data = await self.async_get_net_state()
        return data["hostname"]

    # -- Rooms ---------------------------------------------------------

    async def async_get_rooms(self) -> dict:
        """Get all object with the corresponding description of each
        room."""
        return await self.auth.request("get", "rooms")

    async def async_create_room(self, room: dict) -> dict:
        """Create a new room."""
        return await self.auth.request("post", "rooms", json=room)

    async def async_get_room(self, room_id: int) -> dict:
        """Get one room with all its properties."""
        return await self.auth.request("get", f"rooms/{room_id}")

    async def async_update_room(self, room_id: int, room: dict) -> dict:
        """Patch new values into some properties of an existing room."""
        return await self.auth.request("patch", f"rooms/{room_id}", json=room)

    async def async_delete_room(self, room_id: int) -> dict:
        """Delete an existing room."""
        return await self.auth.request("delete", f"rooms/{room_id}")

    # -- Site Info -----------------------------------------------------

    async def async_get_site_info(self) -> dict:
        """Get all site information."""
        return await self.auth.request("get", "site")

    async def async_set_site_info(self, info: dict) -> dict:
        """Create a new site information object. If an object already
        exists it will be overwritten by this request"""
        return await self.auth.request("post", "site", json=info)

    async def async_update_site_info(self, info: dict) -> dict:
        """Patch new values into site."""
        return await self.auth.request("patch", "site", json=info)

    # -- Loads ---------------------------------------------------------

    async def async_get_loads(self) -> List[Load]:
        """Get all loads with all their properties."""
        data = await self.auth.request("get", "loads")
        return [self.resolve_class(light_data) for light_data in data]

    async def async_get_load(self, load_id: int) -> Load:
        """Get one load with all its properties."""
        raw_data = await self.auth.request("get", f"loads/{load_id}")
        return self.resolve_class(raw_data)

    async def async_update_load(self, load: Load) -> Load:
        """Update an existing load on the API"""
        raw_data = await self.async_patch_load(load.id, load.raw_data)
        return self.resolve_class(raw_data)

    async def async_patch_load(self, load_id: int, load: dict) -> dict:
        """Patch new values into an existing load."""
        return await self.auth.request("patch", f"loads/{load_id}", json=load)

    async def async_load_set_target_state(self, load_id: int, state: dict) -> Load:
        """Save new target state to µGateway. Note: A successful response
        assumes target_state as real state."""
        load = Load({"id": load_id}, self.auth)
        await load.async_set_target_state(state)

        return load

    async def async_load_ctrl(self, load_id: int, button: str, event: str) -> Load:
        """Invoke a button-event (ctrl) for one load."""
        load = Load({"id": load_id}, self.auth)
        await load.async_ctrl(button, event)

        return load

    async def async_load_ping(
        self, load_id: int, time_ms: int, blink_pattern: str, color: str
    ) -> dict:
        """Get the corresponding buttons to control a load lights up."""
        load = Load({"id": load_id}, self.auth)
        return await load.async_ping(time_ms, blink_pattern, color)

    async def async_get_loads_state(self) -> list[dict]:
        """Get an array with only the ids and state properties of all loads."""
        return await self.auth.request("get", "loads/state")

    async def async_get_load_state(self, load_id: int) -> dict:
        """Get only the id and state property of one load."""
        return await self.auth.request("get", f"loads/{load_id}/state")

    async def async_find_loads(
        self, on: bool, time: int, blink_pattern: str, color: str
    ) -> dict:
        """This service puts all loads into the find me mode. If the
        find me mode is on, all corresponding buttons to control a load
        lights up. As soon as a button is pressed, the pressed button
        stops lighting up and the µGateway sends the following event
        over the Websocket connection: {"findme": {"load": 345}}."""

        json = {"on": on, "time": time, "blink_pattern": blink_pattern, "color": color}

        return await self.auth.request("put", "loads/findme", json=json)

    # -- Account -------------------------------------------------------

    # Note: User claiming is already implemented in Auth

    async def async_clone_account(self, user: str, **kwargs) -> dict:
        """Run a user-account cloning from an existing user. Clone an
        existing user-account without pressing any button. If the
        cloning is successful, the response will contain the secret of
        the new user. The secret token of the existing user must be sent
        in the Authorization header!"""

        # TODO: Documentation is unclear whether these are the only values
        validate_str(user, ["installer", "admin", "enduser"])

        login = kwargs.get("login", None)
        company = kwargs.get("company", None)
        name = kwargs.get("name", None)

        json = {"user": user}

        if login is not None:
            json["login"] = login

        if login is not None:
            json["company"] = company

        if login is not None:
            json["name"] = name

        return await self.auth.request("post", "account/clone", json=json)

    async def async_get_clones(self) -> dict:
        """Get all account clone secrets from an existing user. The
        secret token of the existing user must be sent in the
        Authorization header!"""
        return await self.auth.request("get", "account/clones")

    async def async_get_account(self) -> dict:
        """Get all account information from the user
        (identified by header token)."""
        return await self.auth.request("get", "account")

    async def async_update_account(self, data: dict):
        """Patch new values or arbitrary keys into an account
        (identified by header token)."""
        return await self.auth.request("patch", "account", json=data)

    async def async_reset_account(self):
        """Reset an existing account. This method will delete all
        user-specific data like rooms and scenes, but not the account
        itself. The secret token must be sent in the Authorization
        header!"""
        return await self.auth.request("post", "account/reset")

    async def async_sync_account(self, sync: dict):
        """Sync user-specific data from an existing user (source-account)
        to other cloned accounts by passing secrets. Only cloned
        accounts secrets from existing user are allowed! Passing unique
        ids that does not exist from the existing user (source-account)
        but exists by the cloned accounts, those data will be removed!
        Allowed user-specific data (unique ids) to synchronize:
        rooms, schedulers, scenes, groupctrls, loads
        The secret token of the existing user must be sent in the
        Authorization header!"""
        return await self.auth.request("post", "account/sync", json=sync)

    async def async_sync_account_clones(self, sync: dict):
        """Sync user-specific data from an existing user (source-account)
        to all his cloned accounts. Passing unique ids that does not
        exist from the existing user (source-account) but exists by the
        cloned accounts, those data will be removed! Allowed
        user-specific data (unique ids) to synchronize:
        rooms, schedulers, scenes, groupctrls, loads
        The secret token of the existing user must be sent in the
        Authorization header!"""
        return await self.auth.request("post", "account/clones/sync", json=sync)

    async def async_delete_account(self) -> dict:
        """Delete an existing account (identified by header token)."""
        return await self.auth.request("delete", "account")

    # -- Devices -------------------------------------------------------

    async def async_get_devices(self) -> list[Device]:
        """Get a list of all devices."""
        devices = await self.auth.request("get", "devices")
        result = []
        for device_data in devices:
            if device_data["id"] != "00000000":
                result.append(Device(device_data, self.auth))

        return result

    async def async_get_devices_detail(self) -> list[Device]:
        """Get all devices with all properties. Attention: This service
        takes very long time at the first call! Approx. 1 second per
        device. So with 60 devices it takes 1 minute."""
        devices = await self.auth.request("get", "devices/*")
        result = []
        for device_data in devices:
            if device_data["id"] != "00000000":
                result.append(Device(device_data, self.auth))

        return result

    async def async_get_devices_info(self) -> dict:
        """General information about the connected devices."""
        return await self.auth.request("get", "devices/info")

    async def async_get_device(self, device_id: str) -> Device:
        """Get one device with all its properties."""
        raw_data = await self.auth.request("get", f"devices/{device_id}")
        return Device(raw_data, self.auth)

    async def async_delete_device(self, device_id: str) -> Device:
        """Delete an existing device."""
        raw_data = await self.auth.request("delete", f"devices/{device_id}")
        return Device(raw_data, self.auth)

    async def async_ping_device(self, device_id: str) -> bool:
        """Device will light up the yellow LEDs of all buttons for a
        short time."""

        device = Device({"id": device_id}, self.auth)
        return await device.async_ping()

    async def async_get_device_config(self, device_id: str) -> dict:
        """Get a new configuration object and set the device into
        configuration mode."""
        return await self.auth.request("get", f"devices/{device_id}/config")

    async def async_get_device_input_config(
        self, config_id: str, input_channel: int
    ) -> dict:
        """Get the configuration of a device input. Response content can
        vary depending on input-type!

        Args:
            config_id: id received by async_get_device_config()
            input_channel: 0..1 (for device with two loads)"""
        return await self.auth.request(
            "get", f"devices/config/{config_id}/inputs/{input_channel}"
        )

    async def async_set_device_input_config(
        self, config_id: str, input_channel: int, data: dict
    ) -> dict:
        """Change the configuration of a device input."""
        return await self.auth.request(
            "patch", f"devices/config/{config_id}/inputs/{input_channel}", json=data
        )

    async def async_get_device_output_config(
        self, config_id: str, output_channel: int
    ) -> dict:
        """Get the configuration of a device output. Response content
        can vary depending on output-type!"""
        return await self.auth.request(
            "get", f"devices/config/{config_id}/inputs/{output_channel}"
        )

    async def async_set_device_output_config(
        self, config_id: str, output_channel: int, data: dict
    ) -> dict:
        """Change the configuration of a device output."""
        return await self.auth.request(
            "patch", f"devices/config/{config_id}/outputs/{output_channel}", json=data
        )

    async def async_get_device_config_by_config_id(self, config_id: str) -> dict:
        """Get the current configuration."""
        return await self.auth.request("get", f"devices/config/{config_id}")

    async def async_apply_device_config(self, config_id: str) -> dict:
        """Apply the current configuration."""
        return await self.auth.request("put", f"devices/config/{config_id}")

    async def async_discard_device_config(self, config_id: str) -> dict:
        """Discard the current configuration."""
        return await self.auth.request("delete", f"devices/config/{config_id}")

    async def async_find_device(self) -> dict:
        """This service puts all devices into the find-me mode. If the
        find me mode is on, all devices lights up. As soon as a button
        is pressed, all devices stops lighting up."""
        return await self.auth.request("put", "devices/findme")

    # Note: Use Device instance to ping a device

    async def async_calibrate_motor_devices(self) -> dict:
        """Calibration of all motor-actuators. In new installations all
        motor-actuators must be calibrated before they can be used e.g.
        in a scene. This means that each motor-actuator must be moved
        once to the lower- and upper-end of the blind. After that, the
        motor-actuator knows the position of the blind and the learning
        flag in the blind-load status message is no longer set. There is
        no response data on successful calibration. The service returns
        an error, if a calibration is already running or if the
        calibration is not possible. Hint: This service can take a long
        time (up to 6 minutes) depending on the size of the blinds
        (windows) or bad installations!"""
        return await self.auth.request("put", "devices/motor/calibration")

    # -- Timers --------------------------------------------------------

    async def async_get_timers(self) -> list[Timer]:
        """Get a list of all timers."""
        data = await self.auth.request("get", "timers")
        return [Timer(timer_data, self.auth) for timer_data in data]

    async def async_create_timer(self, timer: Timer) -> Timer:
        """Create a new timer with given properties and a unique id.
        Unknown properties will be stored but ignored."""
        data = await self.auth.request("post", "timers", json=timer.raw_data)
        return Timer(data, self.auth)

    async def async_get_timer(self, timer_id: int) -> Timer:
        """Get one timer by id with all its properties."""
        data = await self.auth.request("get", f"timers/{timer_id}")
        return Timer(data, self.auth)

    async def async_update_timer(self, timer: Timer) -> Timer:
        """Put new values into an existing timer. Values of missing keys are
        reset to defaults. Unknown properties will be stored but ignored. A
        successful response contains the changed timer."""
        data = await self.auth.request("put", f"timers/{timer.id}", json=timer.raw_data)
        return Timer(data, self.auth)

    async def async_patch_timer(self, timer_id: int, timer: dict) -> dict:
        """Patch new values into some properties of an existing timer.
        Values of missing keys are preserved. Unknown properties will be
        stored but ignored. A successful response contains the changed
        timer."""
        return await self.auth.request("patch", f"timers/{timer_id}", json=timer)

    async def async_delete_timer(self, timer_id: int) -> Timer:
        """Delete an existing timer. A successful response contains the
        deleted timer."""
        data = await self.auth.request("delete", f"timers/{timer_id}")
        return Timer(data, self.auth)

    # -- Schedulers ----------------------------------------------------

    # Note: Schedulers are documented as app-only and thus are omitted
    #       for now.

    # -- Smart Buttons -------------------------------------------------

    async def async_get_smart_buttons(self) -> list[SmartButton]:
        """Get a list of all SmartButtons."""
        data = await self.auth.request("get", "smartbuttons")
        return [SmartButton(button_data, self.auth) for button_data in data]

    async def async_get_smart_button(self, button_id: int) -> SmartButton:
        """Get one SmartButton by id with all its properties."""
        data = await self.auth.request("get", f"smartbuttons/{button_id}")
        return SmartButton(data, self.auth)

    async def async_update_smart_button(self, button: SmartButton) -> SmartButton:
        """Store a job on that specified SmartButton. A successful
        response contains the changed SmartButton. Warning: Changing a
        job involves a lot of communication between µGateway and
        devices! This service may take a few seconds before the response
        is sent back!"""
        data = await self.auth.request(
            "patch", f"smartbuttons/{button.id}", json=button.raw_data
        )
        return SmartButton(data, self.auth)

    async def async_program_smart_buttons(
        self, on: bool, timeout: int, **kwargs
    ) -> dict:
        """Prepare or abort programming mode. The SmartButtons do not start
        blinking yet! But the µGateway is ready to receive the notify request."""

        json = {
            "on": on,
            "timeout": timeout,
        }

        button_type = kwargs.get("button_type", None)
        if button_type is not None:
            validate_str(button_type, ["scene", "groupctrl"])
            json["button_type"] = button_type

        owner = kwargs.get("owner", None)
        if owner is not None:
            validate_str(owner, ["all", "user"])
            json["owner"] = owner

        return await self.auth.request("post", f"smartbuttons/program", json=json)

    async def async_notify_smart_buttons(self) -> int:
        """Start blinking all SmartButtons and wait until one is
        pressed. As soon as one blinking SmartButton is pressed, all
        SmartButtons stop blinking and the notify request comes back
        with a response. If no SmartButton is pressed, an error response
        is sent."""

        result = await self.auth.request("get", f"smartbuttons/notify")

        return result["button"]

    # -- Jobs ----------------------------------------------------------

    async def async_get_jobs(self) -> list[Job]:
        """Get a list of all jobs."""
        data = await self.auth.request("get", "jobs")
        return [Job(job_data, self.auth) for job_data in data]

    async def async_create_job(self, job: Job) -> Job:
        """Create a new job with a unique id and given target states, a
        button control and/or scripts. The target states without state
        properties will be completed with the current state of their
        loads."""
        data = await self.auth.request("post", "jobs", json=job.raw_data)
        return Job(data, self.auth)

    async def async_get_job(self, job_id: int) -> Job:
        """Get one job by id with all its properties."""
        data = await self.auth.request("get", f"jobs/{job_id}")
        return Job(data, self.auth)

    async def async_update_job(self, job: Job) -> Job:
        """Replace the flag values, target states, button control or
        scripts in an existing Job. A successful response contains the
        changed job."""
        data = await self.auth.request("put", f"jobs/{job.id}", json=job.raw_data)
        return Job(data, self.auth)

    async def async_patch_job(self, job_id: int, job: dict) -> Job:
        """Append more loads with their current or given states to the
        existing target states. Append more flag values to the existing
        ones. Change the event and/or button in the existing button
        control, or append more loads to it. Append more filenames to
        the existing list of scripts. A successful response contains the
        changed job."""
        data = await self.auth.request("patch", f"jobs/{job_id}", json=job)
        return Job(data, self.auth)

    async def async_delete_job(self, job_id: int) -> Job:
        """Delete an existing job. A successful response contains the
        deleted Job."""
        data = await self.auth.request("delete", f"jobs/{job_id}")
        return Job(data, self.auth)

    async def async_delete_jobs_loads(self, load_ids: list[int]):
        """Delete specified loads from all jobs. Delete the specified
        loads from all jobs and remove their associated bindings. A
        successful response contains the list of ids of the deleted
        loads."""
        return await self.auth.request(
            "delete", f"jobs/loads", json={"loads": load_ids}
        )

    async def async_job_trigger_states(self, job_id: int):
        """Send all target states to their corresponding Loads. The flag
        values, button control and scripts are ignored by this method! A
        successful response contains the Job."""
        job = Job({"id": job_id}, self.auth)
        return job.async_trigger_states()

    async def async_trigger_flags(self, job_id: int):
        """Assign all flag values to their corresponding System Flags. The
        target states, button control and scripts are ignored by this
        method!"""
        job = Job({"id": job_id}, self.auth)
        return job.async_trigger_flags()

    async def async_trigger_ctrl(self, job_id: int):
        """Send the stored button control to all its Loads. The flag values,
        target states and scripts are ignored by this method! A successful
        response contains the Job."""
        job = Job({"id": job_id}, self.auth)
        return job.async_trigger_ctrl()

    # Note: Running specific ctrl endpoint omitted.

    async def async_trigger_scripts(self, job_id: int):
        """Execute all scripts of a job. Scripts must be uploaded before
        execution by the scripts service. The flag values, target states
        and the button control are ignored by this method! A successful
        response contains the Job. In case of an exception the error
        response contains the last line of the Traceback."""
        job = Job({"id": job_id}, self.auth)
        return job.async_trigger_scripts()

    async def async_trigger_all(self, job_id: int):
        """Trigger the whole job. Execute all target states, button
        controls, scripts and system flags. A successful response
        contains the Job. In case of an exception the error response
        contains the last line of the Traceback."""
        job = Job({"id": job_id}, self.auth)
        return job.async_trigger_all()

    async def async_trigger_button(
        self, job_id: int, event_type: str, button_type: str
    ):
        """Send the button control from the URL path to all stored loads.
        Send the button control from the URL path to all stored Loads.
        The flag values, target states and scripts are ignored by this
        method! A successful response contains the Job."""
        job = Job({"id": job_id}, self.auth)
        return job.async_trigger_button(event_type, button_type)

    # -- Group Ctrl ----------------------------------------------------

    # Note: Group Ctrls are documented as app-only and thus are omitted
    #       for now. This is used for secondary devices (Nebenstellen)
    #       to control loads.

    # -- Scenes --------------------------------------------------------

    async def async_get_scenes(self) -> list[Scene]:
        """Get a list of all scenes."""
        data = await self.auth.request("get", "scenes")
        return [Scene(scene_data, self.auth) for scene_data in data]

    async def async_create_scene(self, scene: Scene) -> Scene:
        """Create a new scene with given properties and a unique id."""
        data = await self.auth.request("post", "scenes", json=scene.raw_data)
        return Scene(data, self.auth)

    async def async_get_scene(self, scene_id: int) -> Scene:
        """Get one scene by id with all its properties."""
        data = await self.auth.request("get", f"scenes/{scene_id}")
        return Scene(data, self.auth)

    async def async_update_scene(self, scene: Scene) -> Scene:
        """Put new properties into an existing scene. Missing properties
        are removed. A successful response contains the changed scene."""
        scene.raw_data = await self.auth.request(
            "put", f"scenes/{scene.id}", json=scene.raw_data
        )

        return scene

    async def async_patch_scene(self, scene_id: int, scene: dict) -> dict:
        """Patch new values into some properties of an existing scene.
        Values of missing keys are preserved. A successful response
        contains the changed scene."""
        return await self.auth.request("patch", f"scenes/{scene_id}", json=scene)

    async def async_delete_scene(self, scene_id: int) -> Scene:
        """Delete an existing scene. A successful response contains the
        deleted scene."""
        data = await self.auth.request("delete", f"scenes/{scene_id}")
        return Scene(data, self.auth)

    # -- System --------------------------------------------------------

    async def async_get_system_health(self) -> dict:
        """Get system health parameters. The parameter wlan_resets counts
        system resets caused by WLAN adapter problems (excluding
        disassociation events). It counts up to 10 resets during the last
        hour or after last power-up."""
        return await self.auth.request("get", "system/health")

    async def async_get_system_reboot(self) -> None:
        """Reboot the µGateway by invoking a hardware reset. The reboot
        is delayed until the response of this service has been sent."""
        await self.auth.request("get", "system/reboot")

    async def async_post_system_reboot(self, delay: int) -> None:
        """Delayed reboot of the µGateway.
        Args:
            delay: Delay interval in seconds 0 ... 60 before reboot
        """
        await self.auth.request("post", "system/reboot", json={"delay": delay})

    async def async_post_system_network_reset(self) -> None:
        """Set the network state to access-point mode. The new network
        state will take effect after next reboot!"""
        await self.auth.request("post", "system/network-reset")

    # -- System Flags --------------------------------------------------

    async def async_get_system_flags(self) -> list[SystemFlag]:
        """Get a list of all System Flags."""
        data = await self.auth.request("get", "system/flags")
        return [SystemFlag(flag_data, self.auth) for flag_data in data]

    async def async_create_system_flag(self, data: SystemFlag) -> SystemFlag:
        """Create a new System Flag with given properties and a unique id."""

        data = await self.auth.request("post", "system/flags", json=data.raw_data)
        return SystemFlag(data, self.auth)

    async def async_get_system_flag(self, flag_id: int) -> SystemFlag:
        """Get one System Flag by id with all its properties."""
        data = await self.auth.request("get", f"system/flags/{flag_id}")
        return SystemFlag(data, self.auth)

    async def async_update_system_flag(self, flag: SystemFlag) -> SystemFlag:
        """Update an existing system flag on the API"""
        data = await self.async_patch_system_flag(flag.id, flag.raw_data)
        return SystemFlag(data, self.auth)

    async def async_patch_system_flag(self, flag_id: int, data: dict) -> dict:
        """Patch new values into some properties of an existing System
        flag. Values of missing keys are preserved. A successful response
        contains the changed flag."""

        return await self.auth.request("patch", f"system/flags/{flag_id}", json=data)

    async def async_delete_system_flag(self, flag_id: int) -> SystemFlag:
        """Delete an existing System Flag. A successful response contains
        the deleted Flag."""
        data = await self.auth.request("delete", f"system/flags/{flag_id}")
        return SystemFlag(data, self.auth)

    # -- System Conditions ---------------------------------------------

    async def async_get_system_conditions(self) -> list[SystemCondition]:
        """Get a list of all System Conditions."""
        data = await self.auth.request("get", "system/conditions")
        return [SystemCondition(cond_data, self.auth) for cond_data in data]

    async def async_create_system_condition(
        self, condition: SystemCondition
    ) -> SystemCondition:
        """Create a new System Condition with given properties and a
        unique id."""

        data = await self.auth.request(
            "post", "system/conditions", json=condition.raw_data
        )
        return SystemCondition(data, self.auth)

    async def async_get_system_condition(self, condition_id: int) -> SystemCondition:
        """Get one System Condition by id with all its properties."""

        data = await self.auth.request("get", f"system/conditions/{condition_id}")
        return SystemCondition(data, self.auth)

    async def async_update_system_condition(
        self, condition: SystemCondition
    ) -> SystemCondition:
        """Update an existing system condition on the API"""
        data = await self.async_patch_system_condition(condition.id, condition.raw_data)
        return SystemCondition(data, self.auth)

    async def async_patch_system_condition(
        self, condition_id: int, condition: dict
    ) -> dict:
        """Patch new values into some properties of an existing system
        condition. Values of missing keys are preserved. A successful
        response contains the changed condition."""

        return await self.auth.request(
            "patch", f"system/conditions/{condition_id}", json=condition
        )

    async def async_delete_system_condition(self, condition_id: int) -> SystemCondition:
        """Delete an existing System Condition. A successful response
        contains the deleted Condition."""

        data = await self.auth.request("delete", f"system/conditions/{condition_id}")
        return SystemCondition(data, self.auth)

    # -- Helpers -------------------------------------------------------

    def resolve_class(self, data: dict):
        """Resolve this library's implementation class for given load."""
        if data["type"] == "onoff":
            return OnOff(data, self.auth)
        if data["type"] == "dim":
            return Dim(data, self.auth)
        if data["type"] == "dali" and data["sub_type"] == "":
            return Dali(data, self.auth)
        if data["type"] == "dali" and data["sub_type"] == "tw":
            return DaliTw(data, self.auth)
        if data["type"] == "dali" and data["sub_type"] == "rgb":
            return DaliRgbw(data, self.auth)
        if data["type"] == "motor":
            return Motor(data, self.auth)

        raise InvalidLoadType("Invalid load type: " + data["type"])
