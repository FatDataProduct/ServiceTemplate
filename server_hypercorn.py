from hypercorn.config import Config

config = Config()
config.bind = ["0.0.0.0:8001"]

try:
    import uvloop
except ModuleNotFoundError:
    print("[*] Running without `uvloop`")
    uvloop = ...

from app.configuration import load_configuration
from app.program import configure_application
from app.services import configure_services

if uvloop is not ...:
    uvloop.install()

app = configure_application(*configure_services(load_configuration()))


if __name__ == "__main__":
    import anyio
    from hypercorn.asyncio import serve

    anyio.run(serve, app, config)
