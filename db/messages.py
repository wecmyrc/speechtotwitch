import math

from db.base import db_connect, try_query
from db.settings import messages_entries_limit


def init(first_run):
    error = False

    with db_connect() as cursor:
        query = """
            CREATE VIRTUAL TABLE IF NOT EXISTS Messages USING fts4(
                datetime TIMESTAMP,
                int_datetime INTEGER,
                text TEXT,
                username TEXT,
                channel TEXT,
                is_sent BOOL,
                tokenize=unicode61
            )
        """

        error = (
            error
            or try_query(
                query=query,
                execute=cursor.execute,
            )[0]
        )

    return error


def count_all_messages():
    with db_connect() as cursor:
        query = """
            SELECT COUNT(*) as amount FROM Messages
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (result[0], result[1]["amount"])


def handle_messages_limit():
    error = False

    db_error, limit = messages_entries_limit()
    if db_error:
        error = True
        limit = 100

    db_error, all_messages_amount = count_all_messages()
    if db_error:
        error = True
        all_messages_amount = 100

    if error:
        return (True, None)

    if int(limit) < int(all_messages_amount):
        with db_connect() as cursor:
            query = """
                DELETE FROM Messages WHERE rowid IN (SELECT rowid FROM Messages ORDER BY int_datetime LIMIT ?)
            """
            data = (all_messages_amount - limit,)

            result = try_query(
                query=query,
                execute=cursor.execute,
                data=data,
            )

            return result


def messages_pagination_pages(search_value, messages_on_page):
    with db_connect() as cursor:
        if search_value == "":
            query = """
                SELECT COUNT(*) AS amount FROM Messages
            """
            data = tuple()

        else:
            search_value += "*"
            query = """
                SELECT COUNT(*) AS amount FROM Messages WHERE Messages MATCH ?
            """
            data = (search_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
            data=data,
        )

        if messages_on_page == 0:
            messages_on_page = 10

        return (
            result[0],
            math.ceil(float(result[1]["amount"]) / float(messages_on_page)),
        )


def messages_entries_page_rowids(search_value, active_page, messages_on_page):
    with db_connect() as cursor:
        if search_value == "":
            query = """
                SELECT rowid FROM Messages ORDER BY int_datetime DESC LIMIT ? OFFSET ?
            """
            data = (
                messages_on_page,
                (active_page - 1) * messages_on_page,
            )
        else:
            search_value += "*"
            query = """
                SELECT rowid FROM Messages WHERE Messages MATCH ? ORDER BY int_datetime DESC LIMIT ? OFFSET ?
            """
            data = (
                search_value,
                messages_on_page,
                (active_page - 1) * messages_on_page,
            )

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchall,
            data=data,
        )

        processed_result = [r["rowid"] for r in result[1]]

        return (result[0], processed_result)


def messages_entries(username, channel, search_value, active_page, messages_on_page):
    with db_connect() as cursor:
        if username and not channel:
            query = """
                SELECT rowid,* FROM Messages WHERE username = ? ORDER BY int_datetime DESC LIMIT ?
            """
            data = (
                username,
                messages_on_page,
            )

        elif not username and channel:
            query = """
                SELECT rowid,* FROM Messages WHERE channel = ? ORDER BY int_datetime DESC LIMIT ?
            """
            data = (
                channel,
                messages_on_page,
            )

        elif username and channel:
            query = """
                SELECT rowid,* FROM Messages WHERE username = ? AND channel = ? ORDER BY int_datetime DESC LIMIT ?
            """
            data = (
                username,
                channel,
                messages_on_page,
            )

        elif search_value == "":
            query = """
                SELECT rowid,* FROM Messages ORDER BY int_datetime DESC LIMIT ? OFFSET ?
            """
            data = (
                messages_on_page,
                (active_page - 1) * messages_on_page,
            )

        else:
            search_value += "*"
            query = """
                SELECT rowid,* FROM Messages WHERE Messages MATCH ? ORDER BY int_datetime DESC LIMIT ? OFFSET ?
            """
            data = (
                search_value,
                messages_on_page,
                (active_page - 1) * messages_on_page,
            )

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchall,
            data=data,
        )

        return result


def zero_left(string):
    if len(string) == 1:
        string = "0" + string
    return string


def add_messages_entry(datetime, text, username, channel, is_sent):
    with db_connect() as cursor:
        str_year = str(datetime.year)
        str_month = zero_left(str(datetime.month))
        str_day = zero_left(str(datetime.day))
        str_hour = zero_left(str(datetime.hour))
        str_minute = zero_left(str(datetime.minute))
        str_second = zero_left(str(datetime.second))

        int_datetime = int(
            str_year + str_month + str_day + str_hour + str_minute + str_second
        )

        datetime = datetime.strftime("%d.%m.%Y %H:%M:%S")

        query = """
            INSERT INTO Messages(
                datetime,
                int_datetime,
                text,
                username,
                channel,
                is_sent
            ) VALUES (
                ?, ?, ?, ?, ?, ?
            )
        """
        data = (
            datetime,
            int_datetime,
            text,
            username,
            channel,
            is_sent,
        )

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return result


def delete_messages_entry(rowid):
    with db_connect() as cursor:
        query = """
            DELETE FROM Messages WHERE rowid=?
        """
        data = (rowid,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return result


def delete_all_messages_entries():
    with db_connect() as cursor:
        query = """
            DELETE FROM Messages
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
        )

        return result
