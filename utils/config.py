import asyncio
import sys
import json

def setup_asyncio_policy_if_windows():
    if sys.platform == 'win32':
        try:
            asyncio.get_running_loop()
            if isinstance(asyncio.get_event_loop_policy(), asyncio.WindowsProactorEventLoopPolicy):
                return None
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            return None
        except RuntimeError:
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            return None
        except Exception as e:
            return f"Could not set WindowsProactorEventLoopPolicy: {e}"

def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config

