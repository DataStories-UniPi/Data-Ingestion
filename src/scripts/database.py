import config as cfg
from loguru import logger
from sqlalchemy import Engine, create_engine

# from sqlalchemy_utils import create_database, database_exists


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
    engine = create_engine(connection_string, pool_pre_ping=True, pool_recycle=3600)

    # if database_exists(engine.url):
    #     logger.info(f"Database {engine.url.database} exists")
    # else:
    #     create_database(engine.url)
    #     logger.info(f"Database {engine.url.database} created")

    return engine


# def init_db(table_name="crowdedness") -> Literal[-1, 0, 1]:
#     engine = make_connection()

#     try:
#         with engine.connect() as conn:
#             logger.info("Connection established")

#             if inspect(engine).has_table(table_name):
#                 logger.info(f"Table {table_name} already exists")
#             else:
#                 create_table(engine, table_name)
#                 logger.info(f"Created table {table_name}")

#             return 0
#     except OperationalError as e:
#         logger.error(f"Connection failed | {e}")
#         return -1


# def create_table(engine: Engine, table_name: str):

#     meta = MetaData()
#     if table_name == "crowdedness":
#         table = Table(
#             table_name,
#             meta,
#             Column("id", Integer, primary_key=True, autoincrement=True),
#             Column("district_id", String(128), nullable=False),
#             Column("timestamp", Integer, nullable=False),
#             Column("crowd", Integer, nullable=False),
#         )
#     table.create(engine)
