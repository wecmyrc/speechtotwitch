import math

from db.base import db_connect, try_query


def init(first_run):
    error = False

    with db_connect() as cursor:
        query = """
            CREATE VIRTUAL TABLE IF NOT EXISTS Keys USING fts4(
                username TEXT,
                oauth TEXT,
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


def add_keys_entry(username, oauth, tag):
    with db_connect() as cursor:
        query = """
            INSERT INTO Keys(
                username,
                oauth,
                tag
            ) VALUES (
                ?, ?, ?
            )
        """
        data = (
            username,
            oauth,
            tag,
        )

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return result


def delete_keys_entry(rowid):
    with db_connect() as cursor:
        query = """
            DELETE FROM Keys WHERE rowid = ?
        """
        data = (rowid,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return result


def delete_all_keys_entries():
    with db_connect() as cursor:
        query = """
            DELETE FROM Keys
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
        )

        return result


def keys_entries_usernames():
    with db_connect() as cursor:
        query = """
            SELECT username FROM Keys
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchall,
        )

        return result


def keys_entries(search_value, active_page, keys_on_page):
    with db_connect() as cursor:
        if search_value == "":
            query = """
                SELECT rowid,* FROM Keys LIMIT ? OFFSET ?
            """
            data = (
                keys_on_page,
                (active_page - 1) * keys_on_page,
            )
        else:
            search_value += "*"
            query = """
                SELECT rowid,* FROM Keys WHERE Keys MATCH ? LIMIT ? OFFSET ?
            """
            data = (
                search_value,
                keys_on_page,
                (active_page - 1) * keys_on_page,
            )

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchall,
            data=data,
        )

        return result


# NOTE previously was check for username and oauth
def is_keys_entry_exists(username):
    with db_connect() as cursor:
        query = """
            SELECT COUNT(*) AS amount FROM Keys WHERE username=?
        """
        data = (username,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
            data=data,
        )

        return (result[0], result[1]["amount"] != 0)


def update_keys_entries(data):
    with db_connect() as cursor:
        query = """
            UPDATE Keys SET username = ?, oauth = ?, tag = ? WHERE rowid = ?
        """

        result = try_query(
            query=query,
            execute=cursor.executemany,
            data=data,
        )

        return result


def keys_pagination_pages(search_value, keys_on_page):
    with db_connect() as cursor:
        if search_value == "":
            query = """
                SELECT COUNT(*) AS amount FROM Keys
            """
            data = tuple()

        else:
            search_value += "*"
            query = """
                SELECT COUNT(*) AS amount FROM Keys WHERE Keys MATCH ?
            """
            data = (search_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
            data=data,
        )

        if keys_on_page == 0:
            keys_on_page = 10

        return (
            result[0],
            math.ceil(float(result[1]["amount"]) / float(keys_on_page)),
        )


def oauth(username):
    with db_connect() as cursor:
        query = """
            SELECT oauth FROM Keys WHERE username = ?
        """
        data = (username,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
            data=data,
        )

        return (result[0], result[1]["oauth"])
