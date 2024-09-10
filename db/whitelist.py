import math

from db.base import db_connect, try_query


def init(first_run):
    error = False

    with db_connect() as cursor:
        query = """
            CREATE VIRTUAL TABLE IF NOT EXISTS Whitelist USING fts4(
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


def whitelist_pagination_pages(search_value, whitelist_entries_on_page):
    with db_connect() as cursor:
        if search_value == "":
            query = """
                SELECT COUNT(*) AS amount FROM Whitelist
            """
            data = tuple()

        else:
            search_value += "*"
            query = """
                SELECT COUNT(*) AS amount FROM Whitelist WHERE Whitelist MATCH ?
            """
            data = (search_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
            data=data,
        )

        if whitelist_entries_on_page == 0:
            whitelist_entries_on_page = 10

        return (
            result[0],
            math.ceil(float(result[1]["amount"]) / float(whitelist_entries_on_page)),
        )


def all_whitelist_entries():
    with db_connect() as cursor:
        query = """
            SELECT rowid,* FROM Whitelist
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchall,
        )

        return result


def whitelist_entries(search_value, active_page, whitelist_entries_on_page):
    with db_connect() as cursor:
        if search_value == "":
            query = """
                SELECT rowid,* FROM Whitelist LIMIT ? OFFSET ?
            """
            data = (
                whitelist_entries_on_page,
                (active_page - 1) * whitelist_entries_on_page,
            )

        else:
            search_value += "*"
            query = """
                SELECT rowid,* FROM Whitelist WHERE Whitelist MATCH ? LIMIT ? OFFSET ?
            """
            data = (
                search_value,
                whitelist_entries_on_page,
                (active_page - 1) * whitelist_entries_on_page,
            )

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchall,
            data=data,
        )

        return result


def is_whitelist_entry_exists(initial):
    with db_connect() as cursor:
        query = """
            SELECT COUNT(*) AS amount FROM Whitelist WHERE initial = ?
        """
        data = (initial,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
            data=data,
        )

        return (result[0], result[1]["amount"] != 0)


def add_whitelist_entry(initial, tag):
    with db_connect() as cursor:
        query = """
            INSERT INTO Whitelist(
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


def delete_whitelist_entry(rowid):
    with db_connect() as cursor:
        query = """
            DELETE FROM Whitelist WHERE rowid=?
        """
        data = (rowid,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return result


def delete_all_whitelist_entries():
    with db_connect() as cursor:
        query = """
            DELETE FROM Whitelist
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
        )

        return result


def update_whitelist_entries(data):
    with db_connect() as cursor:
        query = """
            UPDATE Whitelist SET initial = ?, tag = ? WHERE rowid = ?
        """

        result = try_query(
            query=query,
            execute=cursor.executemany,
            data=data,
        )

        return result
