import os

from sqlalchemy import (Column, Enum, Integer, JSON,  Boolean, String, Table, create_engine, MetaData)
from dotenv import load_dotenv
from databases import Database
from datetime import datetime as dt
from pytz import timezone as tz
import enum

load_dotenv()
# Database url if none is passed the default one is used
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:apple@localhost/wind")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
 

parameter = Table(
    "parameters",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer), 
    Column("title", String(150)),
    Column("description", String(1000)),
    Column("created_at", String(50), default=dt.now().strftime("%Y-%m-%d %H:%M")),
    Column("updated_at", String(50), default=dt.now().strftime("%Y-%m-%d %H:%M"))
)

parameter_info = Table(
    "parameter_infos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("parameter_id", Integer),
    Column("param_index", String(150)),
    Column("value", JSON),
    Column("created_at", String(50), default=dt.now().strftime("%Y-%m-%d %H:%M")),
    Column("updated_at", String(50), default=dt.now().strftime("%Y-%m-%d %H:%M"))
)

user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(150)),
    Column("is_admin", Boolean, default=False),
    Column("parameter_id", Integer, default=0),
    Column("enabled", Boolean, default=False),
    Column("password", String(1500)),
    Column("created_at", String(50), default=dt.now().strftime("%Y-%m-%d %H:%M")),
    Column("updated_at", String(50), default=dt.now().strftime("%Y-%m-%d %H:%M"))
)
 
operationHistoryList = Table(
    "operationHistoryList",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", String(150)),
    Column("name",String(150)),
) 

operationHistoryData = Table(
    "operationHistoryData",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", String(150)),
    Column("name",String(150)),
    Column("title", String(150)),
    Column("category", String(150)),
    Column("value",String(150)),
    Column("type", String(150)),
) 

# Databases query builder

database = Database(DATABASE_URL)
