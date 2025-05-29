"""Various value constants."""

# Device types for C block
DEVICE_C_TYPE_SCENE = "scene"
DEVICE_C_TYPE_MOTOR = "motor"
DEVICE_C_TYPE_DIMMER = "dimmer"
DEVICE_C_TYPE_SWITCH = "switch"
DEVICE_C_TYPE_WEATHER_STATION = "weather-station"
DEVICE_C_TYPE_WEATHER_STATION_REG = "weather-station-reg"
DEVICE_C_TYPE_HVAC = "hvac"
DEVICE_C_TYPE_SENSOR_TEMPERATURE = "sensor-temp"

# Device types for A block
DEVICE_A_TYPE_NOOP = "noop"
DEVICE_A_TYPE_SWITCH = "switch"
DEVICE_A_TYPE_MOTOR = "motor"
DEVICE_A_TYPE_DIMMER_LED = "dimmer-led"
DEVICE_A_TYPE_DIMMER_DALI = "dimmer-dali"
DEVICE_A_TYPE_WEATHER_STATION = "weather-station"
DEVICE_A_TYPE_WEATHER_STATION_REG = "weather-station-reg"
DEVICE_A_TYPE_HVAC = "hvac"

# Device generations
DEVICE_GENERATION_A = "A"
DEVICE_GENERATION_B = "B"

# Load types
LOAD_TYPE_ONOFF = "onoff"
LOAD_TYPE_DIM = "dim"
LOAD_TYPE_DALI = "dali"
LOAD_TYPE_MOTOR = "motor"
LOAD_TYPE_HVAC = "hvac"

# Load subtypes
LOAD_SUBTYPE_NONE = ""
LOAD_SUBTYPE_ONOFF_DTO = "dto"  # Impulse or off-delay setting
LOAD_SUBTYPE_DALI_TW = "tw"
LOAD_SUBTYPE_DALI_RGB = "rgb"
LOAD_SUBTYPE_MOTOR_RELAY = "relay"

# Kinds for light loads
KIND_LIGHT = 0
KIND_SWITCH = 1

# Kinds for motor loads
KIND_MOTOR = 0
KIND_VENETIAN_BLINDS = 1
KIND_ROLLER_SHUTTER = 2
KIND_AWNING = 3

# Input types
INPUT_TYPE_BUTTON = "button"
INPUT_TYPE_TEMPERATURE = "temperature"
INPUT_TYPE_HUMIDITY = "humidity"
INPUT_TYPE_BRIGHTNESS = "brightness"
INPUT_TYPE_WIND = "wind"
INPUT_TYPE_RAIN = "rain"
INPUT_TYPE_HAIL = "hail"

# Input subtypes
INPUT_SUBTYPE_BUTTON_TOGGLE = "toggle"
INPUT_SUBTYPE_BUTTON_UPDOWN = "up down"
INPUT_SUBTYPE_BUTTON_SCENE = "scene"
INPUT_SUBTYPE_BUTTON_SETUP_SENSOR = "setup_sensor"
INPUT_SUBTYPE_BUTTON_SETUP_WEST = "setup_west"
INPUT_SUBTYPE_BRIGHTNESS_LEFT = "left"
INPUT_SUBTYPE_BRIGHTNESS_CENTER = "center"
INPUT_SUBTYPE_BRIGHTNESS_RIGHT = "right"

# Sensor types
SENSOR_TYPE_TEMPERATURE = "temperature"
SENSOR_TYPE_BRIGHTNESS = "brightness"
SENSOR_TYPE_WIND = "wind"
SENSOR_TYPE_HAIL = "hail"
SENSOR_TYPE_RAIN = "rain"

# Sensor units
UNIT_TEMPERATURE_CELSIUS = "°C"

# Buttons
BUTTON_ON = "on"
BUTTON_OFF = "off"
BUTTON_UP = "up"
BUTTON_DOWN = "down"
BUTTON_TOGGLE = "toggle"
BUTTON_STOP = "stop"

# Events
EVENT_CLICK = "click"
EVENT_PRESS = "press"
EVENT_RELEASE = "release"

# HTTP Methods
HTTP_METHOD_GET = "get"
HTTP_METHOD_POST = "post"
HTTP_METHOD_PUT = "put"
HTTP_METHOD_PATCH = "patch"
HTTP_METHOD_DELETE = "delete"
