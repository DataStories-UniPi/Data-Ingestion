import sys
from pathlib import Path

from config import LOGS_DIR
from loguru import logger


def configure_logger(
    log_dir: Path = LOGS_DIR,
    log_file: str = "app.log",
    rotation: str = "10 MB",
    retention: str = "7 days",
):
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.remove()  # Remove the default handler
    logger.add(
        sys.stdout,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{module}:{line}</cyan> | <level>{message}</level>",
    )

    # Info-level file sink
    logger.add(
        sink=Path(log_dir) / f"{log_file}-info.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        rotation=rotation,
        retention=retention,
        compression="zip",
    )

    # Error-level file sink
    logger.add(
        sink=Path(log_dir) / f"{log_file}-error.log",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message} | {exception}",
        rotation=rotation,
        retention=retention,
        compression="zip",
    )

    logger.info("Logger has been configured.")
    return logger
