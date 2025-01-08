# NOTE in future add info log level for each function and add log-level option

from db.base import db_connect, try_query


def init(first_run):
    error = False

    with db_connect() as cursor:
        query = """
            CREATE TABLE IF NOT EXISTS Settings(
                id INTEGER PRIMARY KEY CHECK (id = 1),
                version TEXT NOT NULL,
                mic_on BOOL NOT NULL,
                twitch_on BOOL NOT NULL,
                username_in_use TEXT,
                channel_in_use TEXT,
                dark_theme BOOL NOT NULL,
                keys_entries_on_page INTEGER NOT NULL,
                dict_entries_on_page INTEGER NOT NULL,
                whitelist_entries_on_page INTEGER NOT NULL,
                blacklist_entries_on_page INTEGER NOT NULL,
                channels_entries_on_page INTEGER NOT NULL,
                messages_entries_on_page INTEGER NOT NULL,
                messages_entries_limit INTEGER NOT NULL,
                last_messages_entries_on_page INTEGER NOT NULL,
                capital_letter BOOL NOT NULL,
                caps_lock BOOL NOT NULL,
                use_dict BOOL NOT NULL,
                use_whitelist BOOL NOT NULL,
                use_blacklist BOOL NOT NULL,
                armed_to_the_teeth BOOL NOT NULL,
                open_browser_on_startup BOOL NOT NULL
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
            init_values = [
                {"column": "version", "value": "2.0.0-beta-0"},
                {"column": "mic_on", "value": False},
                {"column": "twitch_on", "value": False},
                {"column": "username_in_use", "value": None},
                {"column": "channel_in_use", "value": None},
                {"column": "dark_theme", "value": True},
                {"column": "keys_entries_on_page", "value": 10},
                {"column": "dict_entries_on_page", "value": 10},
                {"column": "whitelist_entries_on_page", "value": 10},
                {"column": "blacklist_entries_on_page", "value": 10},
                {"column": "channels_entries_on_page", "value": 10},
                {"column": "messages_entries_on_page", "value": 10},
                {"column": "messages_entries_limit", "value": 1000},
                {"column": "last_messages_entries_on_page", "value": 10},
                {"column": "capital_letter", "value": False},
                {"column": "caps_lock", "value": False},
                {"column": "use_dict", "value": True},
                {"column": "use_whitelist", "value": False},
                {"column": "use_blacklist", "value": False},
                {"column": "armed_to_the_teeth", "value": False},
                {"column": "open_browser_on_startup", "value": True},
            ]

            init_query_part_1 = "INSERT INTO Settings("
            init_query_part_2 = "VALUES ("
            values_list = list()

            for a in range(0, len(init_values)):
                if a == len(init_values) - 1:
                    init_query_part_1 += init_values[a]["column"] + ") "
                    init_query_part_2 += "?)"

                else:
                    init_query_part_1 += init_values[a]["column"] + ", "
                    init_query_part_2 += "?, "

                values_list.append(init_values[a]["value"])

            init_query = init_query_part_1 + init_query_part_2
            data = tuple(values_list)
            error = (
                error
                or try_query(
                    query=init_query,
                    execute=cursor.execute,
                    data=data,
                )[0]
            )

    return error


def restore_settings():
    error = False

    db_error, attt = armed_to_the_teeth()
    if db_error:
        error = True
        attt = False

    if not attt:
        db_error = set_mic_on(False)[0]
        if db_error:
            error = True

        db_error = set_twitch_on(False)[0]
        if db_error:
            error = True

        db_error = set_username_in_use(None)[0]
        if db_error:
            error = True

        db_error = set_channel_in_use(None)[0]
        if db_error:
            error = True

    return (
        error,
        None,
    )


def settings():
    with db_connect() as cursor:
        query = """
            SELECT * FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return result


def set_mic_on(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET mic_on = ? WHERE id = 1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)  # NOTE in every set function return new_value


def mic_on():
    with db_connect() as cursor:
        query = """
            SELECT mic_on FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["mic_on"],
        )


def toggle_mic():
    mic_error, result = mic_on()
    if mic_error:
        return (
            True,
            None,
        )

    return set_mic_on(not result)


def twitch_on():
    with db_connect() as cursor:
        query = """
            SELECT twitch_on FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["twitch_on"],
        )


def toggle_twitch():
    mic_error, result = twitch_on()

    if mic_error:
        return (
            True,
            None,
        )

    return set_twitch_on(not result)


def set_twitch_on(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET twitch_on = ? WHERE id = 1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def username_in_use():
    with db_connect() as cursor:
        query = """
            SELECT username_in_use FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["username_in_use"],
        )


def set_username_in_use(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET username_in_use = ? WHERE id = 1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def channel_in_use():
    with db_connect() as cursor:
        query = """
            SELECT channel_in_use FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["channel_in_use"],
        )


def set_channel_in_use(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET channel_in_use = ? WHERE id = 1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def set_dark_theme(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET dark_theme=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def dark_theme():
    with db_connect() as cursor:
        query = """
            SELECT dark_theme FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["dark_theme"],
        )


def toggle_dark_theme():
    db_error, result = dark_theme()
    if db_error:
        return (
            True,
            None,
        )

    return set_dark_theme(not result)


def keys_entries_on_page():
    with db_connect() as cursor:
        query = """
            SELECT keys_entries_on_page FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["keys_entries_on_page"],
        )


def set_keys_entries_on_page(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET keys_entries_on_page=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def dict_entries_on_page():
    with db_connect() as cursor:
        query = """
            SELECT dict_entries_on_page FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["dict_entries_on_page"],
        )


def set_dict_entries_on_page(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET dict_entries_on_page=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def messages_entries_on_page():
    with db_connect() as cursor:
        query = """
            SELECT messages_entries_on_page FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["messages_entries_on_page"],
        )


def set_messages_entries_on_page(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET messages_entries_on_page=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def messages_entries_limit():
    with db_connect() as cursor:
        query = """
            SELECT messages_entries_limit FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["messages_entries_limit"],
        )


def set_messages_entries_limit(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET messages_entries_limit=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def whitelist_entries_on_page():
    with db_connect() as cursor:
        query = """
            SELECT whitelist_entries_on_page FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["whitelist_entries_on_page"],
        )


def set_whitelist_entries_on_page(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET whitelist_entries_on_page=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def blacklist_entries_on_page():
    with db_connect() as cursor:
        query = """
            SELECT blacklist_entries_on_page FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["blacklist_entries_on_page"],
        )


def set_blacklist_entries_on_page(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET blacklist_entries_on_page=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def channels_entries_on_page():
    with db_connect() as cursor:
        query = """
            SELECT channels_entries_on_page FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["channels_entries_on_page"],
        )


def set_channels_entries_on_page(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET channels_entries_on_page=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def set_last_messages_entries_on_page(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET last_messages_entries_on_page=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def last_messages_entries_on_page():
    with db_connect() as cursor:
        query = """
            SELECT last_messages_entries_on_page FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["last_messages_entries_on_page"],
        )


def set_capital_letter(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET capital_letter=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def capital_letter():
    with db_connect() as cursor:
        query = """
            SELECT capital_letter FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["capital_letter"],
        )


def toggle_capital_letter():
    db_error, result = capital_letter()
    if db_error:
        return (
            True,
            None,
        )

    return set_capital_letter(not result)


def set_caps_lock(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET caps_lock=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def caps_lock():
    with db_connect() as cursor:
        query = """
            SELECT caps_lock FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["caps_lock"],
        )


def toggle_caps_lock():
    db_error, result = caps_lock()
    if db_error:
        return (
            True,
            None,
        )

    return set_caps_lock(not result)


def set_use_dict(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET use_dict=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def use_dict():
    with db_connect() as cursor:
        query = """
            SELECT use_dict FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["use_dict"],
        )


def toggle_use_dict():
    db_error, result = use_dict()
    if db_error:
        return (
            True,
            None,
        )

    return set_use_dict(not result)


def set_use_whitelist(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET use_whitelist=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def use_whitelist():
    with db_connect() as cursor:
        query = """
            SELECT use_whitelist FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["use_whitelist"],
        )


def toggle_use_whitelist():
    db_error, result = use_whitelist()
    if db_error:
        return (
            True,
            None,
        )

    return set_use_whitelist(not result)


def set_use_blacklist(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET use_blacklist=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def use_blacklist():
    with db_connect() as cursor:
        query = """
            SELECT use_blacklist FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["use_blacklist"],
        )


def toggle_use_blacklist():
    db_error, result = use_blacklist()
    if db_error:
        return (
            True,
            None,
        )

    return set_use_blacklist(not result)


def set_armed_to_the_teeth(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET armed_to_the_teeth=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def armed_to_the_teeth():
    with db_connect() as cursor:
        query = """
            SELECT armed_to_the_teeth FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["armed_to_the_teeth"],
        )


def toggle_armed_to_the_teeth():
    db_error, result = armed_to_the_teeth()
    if db_error:
        return (
            True,
            None,
        )

    return set_armed_to_the_teeth(not result)


def set_open_browser_on_startup(new_value):
    with db_connect() as cursor:
        query = """
            UPDATE Settings SET open_browser_on_startup=? WHERE id=1
        """
        data = (new_value,)

        result = try_query(
            query=query,
            execute=cursor.execute,
            data=data,
        )

        return (result[0], new_value)


def open_browser_on_startup():
    with db_connect() as cursor:
        query = """
            SELECT open_browser_on_startup FROM Settings
        """

        result = try_query(
            query=query,
            execute=cursor.execute,
            fetch=cursor.fetchone,
        )

        return (
            result[0],
            result[1] if result[0] else result[1]["open_browser_on_startup"],
        )


def toggle_open_browser_on_startup():
    db_error, result = open_browser_on_startup()
    if db_error:
        return (
            True,
            None,
        )

    return set_open_browser_on_startup(not result)
