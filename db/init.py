import pathlib

from db.base import db_file

import db.blacklist as bl
import db.channels as ch
import db.dict as di
import db.keys as ke
import db.messages as me
import db.settings as se
import db.whitelist as wh


def is_db_exists():
    return pathlib.Path(db_file()).is_file()


def init_db():
    first_run = not is_db_exists()

    error_list = list()

    error_list.append(bl.init(first_run))
    error_list.append(ch.init(first_run))
    error_list.append(di.init(first_run))
    error_list.append(ke.init(first_run))
    error_list.append(me.init(first_run))
    error_list.append(se.init(first_run))
    error_list.append(wh.init(first_run))

    return (
        True in error_list,
        db_file(),
    )
