import math

from db.base import db_connect, try_query


def init(first_run):
    error = False

    with db_connect() as cursor:
        query = """
            CREATE VIRTUAL TABLE IF NOT EXISTS Channels USING fts4(
                name TEXT,
                tag TEXT,
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


def channels_pagination_pages(search_value, channels_entries_on_page):
    with db_connect() as cursor:
        if search_value == "":
            query = """
                SELECT COUNT(*) AS amount FROM Channels
            """
            data = tuple()

        else:
            search_value += "*"
            query = """
                SELECT COUNT(*) AS amount FROM Channels WHERE Channels MATCH ?
            """
            data = (search_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
            data=data,
        )

        if channels_entries_on_page == 0:
            channels_entries_on_page = 10

        return (
            result[0],
            math.ceil(float(result[1]["amount"]) / float(channels_entries_on_page)),
        )


def channels_entries_names():
    with db_connect() as cursor:
        query = """
            SELECT name FROM Channels
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchall,
        )

        return result


def channels_entries(search_value, active_page, channels_entries_on_page):
    with db_connect() as cursor:
        if search_value == "":
            query = """
                SELECT rowid,* FROM Channels LIMIT ? OFFSET ?
            """
            data = (
                channels_entries_on_page,
                (active_page - 1) * channels_entries_on_page,
            )

        else:
            search_value += "*"
            query = """
                SELECT rowid,* FROM Channels WHERE Channels MATCH ? LIMIT ? OFFSET ?
            """
            data = (
                search_value,
                channels_entries_on_page,
                (active_page - 1) * channels_entries_on_page,
            )

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchall,
            data=data,
        )

        return result


def is_channels_entry_exists(name):
    with db_connect() as cursor:
        query = """
            SELECT COUNT(*) AS amount FROM Channels WHERE name = ?
        """
        data = (name,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
            data=data,
        )

        return (result[0], result[1]["amount"] != 0)


def add_channels_entry(name, tag):
    with db_connect() as cursor:
        query = """
            INSERT INTO Channels(
                name,
                tag
            ) VALUES (
                ?, ?
            )
        """
        data = (
            name.lower(),
            tag,
        )

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return result


def delete_channels_entry(rowid):
    with db_connect() as cursor:
        query = """
            DELETE FROM Channels WHERE rowid=?
        """
        data = (rowid,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return result


def delete_all_channels_entries():
    with db_connect() as cursor:
        query = """
            DELETE FROM Channels
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
        )

        return result


def update_channels_entries(data):
    with db_connect() as cursor:
        query = """
            UPDATE Channels SET name = ?, tag = ? WHERE rowid = ?
        """

        result = try_query(
            query=query,
            execute=cursor.executemany,
            data=data,
        )

        return result
