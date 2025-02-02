import config as cfg
from loguru import logger
from sqlalchemy import Engine, create_engine


def make_connection(dialect: str = "psycopg2") -> Engine:
    logger.info("Loading Database Credentials")

    if not all(
        hasattr(cfg, attr)
        for attr in [
            "DB_USER",
            "DB_PASSWORD",
            "DB_HOST",
            "DB_PORT",
            "DB_NAME",
        ]
    ):
        raise ValueError("Missing required configuration attributes for SSH tunnel.")

    connection_string = (
        f"postgresql+{dialect}://{cfg.DB_USER}:{cfg.DB_PASSWORD}"
        f"@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}"
    )

    logger.info(f"Connecting to {cfg.DB_NAME} DB on {cfg.DB_HOST}:{cfg.DB_PORT}")
    return create_engine(connection_string, pool_pre_ping=True, pool_recycle=3600)
