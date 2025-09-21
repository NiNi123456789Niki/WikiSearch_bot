import logging
import inspect


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(filename)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

def log(level: str, message):
    frame = inspect.stack()[1]
    caller_file = frame.filename.split("/")[-1]

    logger = logging.getLogger(caller_file)

    lvl = LEVELS.get(level.upper())
    if lvl is None:
        raise ValueError(f"Неизвестный уровень логирования: {level}")

    logger.log(lvl, message)