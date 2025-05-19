"""Support for jobs."""

from __future__ import annotations

from aiowiserbyfeller.auth import Auth
from aiowiserbyfeller.util import validate_str


class Job:
    """Representation of a job in the Feller Wiser µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a job object."""
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> int | None:
        """The id of the job."""
        return self.raw_data.get("id")

    @property
    def target_states(self) -> list[dict]:
        """List of objects each with a load and state properties."""
        try:
            return self.raw_data["target_states"]
        except KeyError:
            return []

    @property
    def flag_values(self) -> list[dict]:
        """List of objects each with a flag and a value."""
        try:
            return self.raw_data["flag_values"]
        except KeyError:
            return []

    @property
    def button_ctrl(self) -> dict | None:
        """List of button presses to be simulated in this job."""
        try:
            return self.raw_data["button_ctrl"]
        except KeyError:
            return None

    @property
    def scripts(self) -> list[str]:
        """List of script filenames relative to /flash/scripts/."""
        try:
            return self.raw_data["scripts"]
        except KeyError:
            return []

    @property
    def blocked_by(self) -> int | None:
        """Id of a system flag or condition that may block this job."""
        return self.raw_data["blocked_by"]

    @property
    def triggers(self) -> list[int]:
        """List of ids of scenes, groupctrls and schedulers using this job."""
        try:
            return self.raw_data["triggers"]
        except KeyError:
            return []

    async def async_refresh(self):
        """Fetch data from µGateway."""
        data = await self.auth.request("get", f"jobs/{self.id}")
        self.raw_data = data

    async def async_trigger_states(self):
        """Send all target states to their corresponding Loads.

        The flag values, button control and scripts are ignored by this method!
        A successful response contains the Job.
        """
        data = await self.auth.request("get", f"jobs/{self.id}/run")
        self.raw_data = data

    async def async_trigger_flags(self):
        """Assign all flag values to their corresponding System Flags.

        The target states, button control and scripts are ignored by this method!
        """
        data = await self.auth.request("get", f"jobs/{self.id}/setflags")
        self.raw_data = data

    async def async_trigger_ctrl(self):
        """Send the stored button control to all its Loads.

        The flag values, target states and scripts are ignored by this method!
        A successful response contains the Job.
        """
        data = await self.auth.request("get", f"jobs/{self.id}/ctrl")
        self.raw_data = data

    # Note: Running specific ctrl endpoint omitted.

    async def async_trigger_scripts(self):
        """Execute all scripts of a job.

        Scripts must be uploaded before execution by the scripts service.
        The flag values, target states and the button control are ignored by this method!
        A successful response contains the Job.
        In case of an exception the error response contains the last line of the Traceback.
        """
        data = await self.auth.request("get", f"jobs/{self.id}/execute")
        self.raw_data = data

    async def async_trigger_all(self):
        """Trigger the whole job.

        Execute all target states, button controls, scripts and system flags.
        A successful response contains the Job.
        In case of an exception the error response contains the last line of the Traceback.
        """
        data = await self.auth.request("get", f"jobs/{self.id}/trigger")
        self.raw_data = data

    async def async_trigger_button(self, event_type: str, button_type: str):
        """Send the button control from the URL path to all stored loads.

        The flag values, target states and scripts are ignored by this method!
        A successful response contains the Job.
        """

        validate_str(event_type, ["click", "press", "on"])
        validate_str(button_type, ["on", "off", "up", "down", "toggle", "stop"])

        data = await self.auth.request(
            "get", f"jobs/{self.id}/ctrl/{event_type}/{button_type}"
        )
        self.raw_data = data
