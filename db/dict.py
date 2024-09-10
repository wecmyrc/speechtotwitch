import math

from db.base import db_connect, try_query


def init(first_run):
    error = False

    with db_connect() as cursor:
        query = """
            CREATE VIRTUAL TABLE IF NOT EXISTS Dict USING fts4(
                initial TEXT,
                final TEXT,
                tag TEXT,
                is_glued BOOL
            )
        """

        error = (
            error
            or try_query(
                query=query,
                execute=cursor.execute,
            )[0]
        )

        if first_run:
            default_dict = [
                ("запятая", ",", "Знаки препинания", True),
                ("точка", ".", "Знаки препинания", True),
                ("знак вопроса", "?", "Знаки препинания", True),
                ("знак восклицания", "!", "Знаки препинания", True),
                ("лягушка", "🐸", "Emojis", False),
                ("орангутанг", "🦧", "Emojis", False),
                ("горилла", "🦍", "Emojis", False),
                ("попугай", "🦜", "Emojis", False),
                ("гоблин", "👺", "Emojis", False),
                ("машет рукой", "👋", "Emojis", False),
                ("рука на тебя", "🫵", "Emojis", False),
                ("рука победы", "✌️", "Emojis", False),
                ("аплодисменты", "👏", "Emojis", False),
                ("люблю тебя знак", "🤟", "Emojis", False),
                ("рукопожатие", "🤝", "Emojis", False),
                ("яйцо", "🥚", "Emojis", False),
                ("библия", "BibleThump", "GlobalEmotes", False),
                ("четыре голова", "4Head", "GlobalEmotes", False),
                ("жаба", "OSFrog", "GlobalEmotes", False),
                ("квадратная голова", "PunchTrees", "GlobalEmotes", False),
            ]
            query = """
                INSERT INTO Dict(
                    initial,
                    final,
                    tag,
                    is_glued
                ) VALUES (
                    ?, ?, ?, ?
                )
            """
            data = default_dict

            error = (
                error
                or try_query(
                    query=query,
                    execute=cursor.executemany,
                    data=data,
                )[0]
            )

    return error


def add_dict_entry(initial, final, is_glued, tag):
    with db_connect() as cursor:
        query = """
            INSERT INTO Dict(
                initial,
                final,
                is_glued,
                tag
            ) VALUES (
                ?, ?, ?, ?
            )
        """
        data = (
            initial.lower(),
            final,
            is_glued,
            tag,
        )

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

    return result


def delete_dict_entry(rowid):
    with db_connect() as cursor:
        query = """
            DELETE FROM Dict WHERE rowid=?
        """
        data = (rowid,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

    return result


def delete_all_dict_entries():
    with db_connect() as cursor:
        query = """
            DELETE FROM Dict
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
        )

    return result


def all_dict_entries():
    with db_connect() as cursor:
        query = """
            SELECT rowid,* FROM Dict
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchall,
        )

        return result


def dict_entries(search_value, active_page, dict_entries_on_page):
    with db_connect() as cursor:
        if search_value == "":
            query = """
                SELECT rowid,* FROM Dict LIMIT ? OFFSET ?
            """
            data = (
                dict_entries_on_page,
                (active_page - 1) * dict_entries_on_page,
            )

        else:
            search_value += "*"
            query = """
                SELECT rowid,* FROM Dict WHERE Dict MATCH ? LIMIT ? OFFSET ?
            """
            data = (
                search_value,
                dict_entries_on_page,
                (active_page - 1) * dict_entries_on_page,
            )

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchall,
            data=data,
        )

    return result


def is_dict_entry_exists(initial):
    with db_connect() as cursor:
        query = """
            SELECT COUNT(*) AS amount FROM Dict WHERE initial = ?
        """
        data = (initial,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
            data=data,
        )

    return (result[0], result[1]["amount"] != 0)


def update_dict_entries(data):
    with db_connect() as cursor:
        query = """
            UPDATE Dict SET initial = ?, final = ?, tag = ?, is_glued = ? WHERE rowid = ?
        """

        result = try_query(
            query=query,
            execute=cursor.executemany,
            data=data,
        )

    return result


def dict_pagination_pages(search_value, dict_entries_on_page):
    with db_connect() as cursor:
        if search_value == "":
            query = """
                SELECT COUNT(*) AS amount FROM Dict
            """
            data = tuple()

        else:
            search_value += "*"
            query = """
                SELECT COUNT(*) AS amount FROM Dict WHERE Dict MATCH ?
            """
            data = (search_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
            data=data,
        )

        # [note] probably rewrite this in future
        if dict_entries_on_page == 0:
            dict_entries_on_page = 10

        return (
            result[0],
            math.ceil(float(result[1]["amount"]) / float(dict_entries_on_page)),
        )
