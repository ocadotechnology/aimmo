"""
Sets up the AimmoAppConfig class. Since we don't want to reset the app config every
time the Django server reloads when we make a code change, the app config is set only
if the main thread isn't already running.
"""
import os

if os.environ.get("RUN_MAIN", None) != "true":
    default_app_config = "aimmo.apps.AimmoAppConfig"

__version__ = '0.55.0'
