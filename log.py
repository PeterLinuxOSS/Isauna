import logging
from colorlog import ColoredFormatter
CONSOLE = logging.StreamHandler()
CONSOLE.setLevel(logging.DEBUG)
class StandardLogger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        
        self.addHandler(CONSOLE)
        

formatter_color = ColoredFormatter(
    '%(log_color)s%(asctime)s %(levelname)s %(message)s%(reset)s',
    datefmt='%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red",
        "TRACE": "white",
    },
)
CONSOLE.setFormatter(formatter_color)

logger = StandardLogger(__name__)
logger.warning("load file")