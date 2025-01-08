# NOTE add db encryption and password access

import os
import sys
import pathlib
import sqlite3
import logging
import traceback
from contextlib import contextmanager

from base_logger.base_logger import logger


def db_file():
    db_path = str()
    db_file = str()

    try:
        if sys.platform == "win32":
            if getattr(sys, "frozen", False):
                db_path = os.path.dirname(sys.executable)
            else:
                db_path = os.path.dirname(__file__)

            db_file = os.path.join(db_path, "stt.db")

        elif sys.platform.startswith("linux"):
            db_path = str(pathlib.Path.home()) + "/.stt"
            pathlib.Path(db_path).mkdir(mode=0o777, parents=True, exist_ok=True)
            db_file = db_path + "/stt.db"

    except Exception as e:
        error = "".join(traceback.format_exc())
        logger.critical(error, stack_info=True)
        print(error)

    return db_file


@contextmanager
def db_connect():
    connection = sqlite3.connect(db_file())
    connection.row_factory = lambda c, r: dict(
        [(col[0], r[idx]) for idx, col in enumerate(c.description)]
    )

    try:
        cursor = connection.cursor()
        yield cursor

    except sqlite3.Error as e:
        connection.rollback()
        error = "".join(traceback.format_exc())
        logger.critical(error, stack_info=True)
        print(error)

    except Exception as e:
        error = "".join(traceback.format_exc())
        logger.critical(error, stack_info=True)
        print(error)

    else:
        connection.commit()

    finally:
        connection.close()


def try_query(query, execute, fetch=None, data=tuple()):
    result = None

    try:
        execute(query, data)

        if fetch:
            result = fetch()

    except sqlite3.Error as e:
        error = "".join(traceback.format_exc())
        logger.critical(error, stack_info=True)
        print(error)
        return (True, result)  # 1 on error

    else:
        return (False, result)  # 0 on success
