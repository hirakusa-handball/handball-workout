from pathlib import Path
import sys

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from defaults import DEFAULT_LIBRARY, DEFAULT_TODAYS_MENU

def main() -> None:
    print("Set APPS_SCRIPT_WEB_APP_URL and APPS_SCRIPT_API_KEY before execution.")

    import os

    web_app_url = os.environ["APPS_SCRIPT_WEB_APP_URL"]
    api_key = os.environ["APPS_SCRIPT_API_KEY"]

    response = requests.post(
        web_app_url,
        json={
            "action": "seed_defaults",
            "api_key": api_key,
            "library": DEFAULT_LIBRARY,
            "daily_menu": DEFAULT_TODAYS_MENU,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(data.get("error", "Failed to seed"))
    print("Seed completed via Apps Script.")


if __name__ == "__main__":
    main()
