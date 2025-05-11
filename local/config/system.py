import asyncio

def setup_asyncio_policy():
    try:
        from asyncio import WindowsProactorEventLoopPolicy

        if not isinstance(asyncio.get_event_loop_policy(), WindowsProactorEventLoopPolicy):
            asyncio.set_event_loop_policy(WindowsProactorEventLoopPolicy())
    except (RuntimeError, ImportError, AttributeError) as e:
        print(f"[Warning] Could not set Windows asyncio policy: {e}")