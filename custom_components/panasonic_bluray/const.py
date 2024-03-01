from datetime import timedelta
__version__ = "1.0.0"
PROJECT_URL = "https://github.com/albaintor/panasonic_bluray_remote"
ISSUE_URL = "{}issues".format(PROJECT_URL)

DOMAIN = "panasonic_bluray"
PANASONIC_COORDINATOR = "panasonic_coordinator"
NAME = "Panasonic Bluray"
DEFAULT_DEVICE_NAME = "Panasonic Bluray"
PANASONIC_API = "panasonic_api"
STARTUP = """
-------------------------------------------------------------------
{}
Version: {}
This is a custom integration.
If you have any issues with this you need to open an issue here:
{}
-------------------------------------------------------------------
""".format(
    NAME, __version__, ISSUE_URL
)

SCAN_INTERVAL = timedelta(seconds=10)
MIN_TIME_BETWEEN_SCANS = SCAN_INTERVAL
MIN_TIME_BETWEEN_FORCED_SCANS = timedelta(seconds=1)

