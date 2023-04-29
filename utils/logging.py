from rich.logging import RichHandler
from rich.console import Console
from rich import inspect
import logging

class RichLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.console = Console()

    def __call__(self, *args):
        self.console.log(*args)

def setup_rich_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)]
    )

logging.setLoggerClass(RichLogger)
setup_rich_logger()
log = logging.getLogger('RichLogger')
