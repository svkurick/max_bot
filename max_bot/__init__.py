from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("max_bot")
except PackageNotFoundError:
    __version__ = "0.0.0"

from .bot import Bot
from .dispatcher.dispatcher import Dispatcher
from .polling.polling import run_polling
from .types.callback import Callback

__all__ = [
    "__version__",
    "Bot",
    "Dispatcher",
    "run_polling",
    "Callback",
]