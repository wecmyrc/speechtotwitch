import math

from db.base import db_connect, try_query


def init(first_run):
    error = False

    with db_connect() as cursor:
        query = """
            CREATE VIRTUAL TABLE IF NOT EXISTS Blacklist USING fts4(
                initial TEXT,
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


def blacklist_pagination_pages(search_value, blacklist_entries_on_page):
    with db_connect() as cursor:
        if search_value == "":
            query = """
                SELECT COUNT(*) AS amount FROM Blacklist
            """
            data = tuple()

        else:
            search_value += "*"
            query = """
                SELECT COUNT(*) AS amount FROM Blacklist WHERE Blacklist MATCH ?
            """
            data = (search_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
            data=data,
        )

        if blacklist_entries_on_page == 0:
            blacklist_entries_on_page = 10

        return (
            result[0],
            math.ceil(float(result[1]["amount"]) / float(blacklist_entries_on_page)),
        )


def all_blacklist_entries():
    with db_connect() as cursor:
        query = """
            SELECT rowid,* FROM Blacklist
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchall,
        )

        return result


def blacklist_entries(search_value, active_page, blacklist_entries_on_page):
    with db_connect() as cursor:
        if search_value == "":
            query = """
                SELECT rowid,* FROM Blacklist LIMIT ? OFFSET ?
            """
            data = (
                blacklist_entries_on_page,
                (active_page - 1) * blacklist_entries_on_page,
            )

        else:
            search_value += "*"
            query = """
                SELECT rowid,* FROM Blacklist WHERE Blacklist MATCH ? LIMIT ? OFFSET ?
            """
            data = (
                search_value,
                blacklist_entries_on_page,
                (active_page - 1) * blacklist_entries_on_page,
            )

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchall,
            data=data,
        )

        return result


def is_blacklist_entry_exists(initial):
    with db_connect() as cursor:
        query = """
            SELECT COUNT(*) AS amount FROM Blacklist WHERE initial = ?
        """
        data = (initial,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
            data=data,
        )

        return (result[0], result[1]["amount"] != 0)


def add_blacklist_entry(initial, tag):
    with db_connect() as cursor:
        query = """
            INSERT INTO Blacklist(
                initial,
                tag
            ) VALUES (
                ?, ?
            )
        """
        data = (
            initial.lower(),
            tag,
        )

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return result


def delete_blacklist_entry(rowid):
    with db_connect() as cursor:
        query = """
            DELETE FROM Blacklist WHERE rowid=?
        """
        data = (rowid,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return result


def delete_all_blacklist_entries():
    with db_connect() as cursor:
        query = """
            DELETE FROM Blacklist
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
        )

        return result


def update_blacklist_entries(data):
    with db_connect() as cursor:
        query = """
            UPDATE Blacklist SET initial = ?, tag = ? WHERE rowid = ?
        """

        result = try_query(
            query=query,
            execute=cursor.executemany,
            data=data,
        )

        return result
