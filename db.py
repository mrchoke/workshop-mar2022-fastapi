import json
from datetime import date, datetime, time
from decimal import Decimal

from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from settings import cfg


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, time):
        return obj.strftime("%H:%M")
    raise TypeError("Type %s not serializable" % type(obj))


DATABASE_URL = f"postgresql://{cfg.DB_USERNAME}:{cfg.DB_PASSWORD}@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}"

engine = None
database = None

try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
        json_serializer=lambda obj: json.dumps(
            obj, ensure_ascii=False, default=json_serial),
        isolation_level="AUTOCOMMIT",
        pool_size=3,
        connect_args={}
    )

except Exception as e:
    print(str(e), flush=True)

try:
    database = Database(
        DATABASE_URL, force_rollback=False, min_size=5, max_size=20)
    database._backend._dialect._json_serializer = lambda obj: json.dumps(
        obj, ensure_ascii=False, default=json_serial)
except Exception as e:
    print(str(e), flush=True)


Base: DeclarativeMeta = declarative_base()

db: Database = database


def init_db():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(str(e), flush=True)
        raise str(e)
