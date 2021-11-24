"""CSP config"""

from common.app_settings import domain, MODULE_NAME

CSP_CONFIG = {
    "CSP_DEFAULT_SRC": ("'self'",),
    "CSP_IMG_SRC": (
        f"{domain()}/static/",
        "https://p.typekit.net/",
    ),
    "CSP_FONT_SRC": ("https://use.typekit.net/",),
    "CSP_SCRIPT_SRC": (
        "https://use.typekit.net/mrl4ieu.js",
        "https://pyodide-cdn2.iodide.io/v0.15.0/full/",
    ),
    "CSP_CONNECT_SRC": (
        "https://pyodide-cdn2.iodide.io/v0.15.0/full/",
        f"wss://{MODULE_NAME}-aimmo.codeforlife.education/",
        f"https://{MODULE_NAME}-aimmo.codeforlife.education/",
    ),
}

if MODULE_NAME == "local":
    CSP_CONFIG["CSP_CONNECT_SRC"] += (
        "ws://localhost:*/",
        "ws://*:*/socket.io/",
        "http://*:*/socket.io/",
    )
