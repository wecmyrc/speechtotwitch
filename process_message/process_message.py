def process_message(
    message,
    settings,
    blacklist_entries,
    whitelist_entries,
    dict_entries,
):
    message = message.lower()

    final_parts = list()

    if message.find("\n") != -1:
        for part in message.split("\n"):
            final_parts.append(
                apply_settings(
                    message=part,
                    settings=settings,
                    blacklist_entries=blacklist_entries,
                    whitelist_entries=whitelist_entries,
                    dict_entries=dict_entries,
                )
            )

        return "\n".join(final_parts)

    return apply_settings(
        message=message,
        settings=settings,
        blacklist_entries=blacklist_entries,
        whitelist_entries=whitelist_entries,
        dict_entries=dict_entries,
    )


def apply_settings(
    message,
    settings,
    blacklist_entries,
    whitelist_entries,
    dict_entries,
):
    if (
        message == None or message == "" or message == str()
    ):  # NOTE maybe simply if not message?
        return message

    if settings["use_blacklist"]:
        message = apply_blacklist(message, blacklist_entries)

    if settings["use_whitelist"]:
        message = apply_whitelist(message, whitelist_entries)

    if settings["use_dict"]:
        message = apply_dict(message, dict_entries)

    if settings["capital_letter"]:
        message = apply_capital_letter(message)

    if settings["caps_lock"]:
        message = apply_caps_lock(message)

    return message


def apply_capital_letter(message):
    return message.capitalize()


def apply_caps_lock(message):
    return message.upper()


def apply_dict(message, dict_entries):
    message_parts = message.split(" ")

    glued_indexes = list()

    for entry in dict_entries:
        for i in range(len(message_parts)):
            if message_parts[i] == entry["initial"]:
                message_parts[i] = entry["final"]

                if entry["is_glued"]:
                    glued_indexes.append(i)

            if len(entry["initial"].split(" ")) != 0:
                initial_parts = entry["initial"].split(" ")

                check = False
                for j in range(len(initial_parts)):
                    if i + j >= len(message_parts):
                        check = True
                        break

                    if message_parts[i + j] != initial_parts[j]:
                        check = True
                        break

                if not check:
                    message_parts[i] = entry["final"]

                    if entry["is_glued"]:
                        glued_indexes.append(i)

                    for k in range(i + 1, i + len(initial_parts)):
                        message_parts[k] = ""

    list.sort(glued_indexes, reverse=True)

    while "" in message_parts:
        index = message_parts.index("")

        for i in range(len(glued_indexes)):
            if glued_indexes[i] > index:
                glued_indexes[i] = glued_indexes[i] - 1

        message_parts.remove("")

    for i in glued_indexes:
        if i > 0:
            message_parts[i - 1] = message_parts[i - 1] + message_parts[i]
            message_parts[i] = ""

    while "" in message_parts:
        message_parts.remove("")

    return " ".join(message_parts)


def apply_whitelist(message, whitelist_entries):
    message_parts = message.split(" ")

    allowed_words = list()

    for entry in whitelist_entries:
        for i in range(len(message_parts)):
            if message_parts[i] == entry["initial"]:
                allowed_words.append(message_parts[i])
                message_parts[i] = ""

            if len(entry["initial"].split(" ")) != 0:
                initial_parts = entry["initial"].split(" ")

                check = False
                for j in range(len(initial_parts)):
                    if i + j >= len(message_parts):
                        check = True
                        break

                    if message_parts[i + j] != initial_parts[j]:
                        check = True
                        break

                if not check:
                    allowed_words.append(message_parts[i])
                    message_parts[i] = ""

    return " ".join(allowed_words)


def apply_blacklist(message, blacklist_entries):
    message_parts = message.split(" ")

    for entry in blacklist_entries:
        for i in range(len(message_parts)):
            if message_parts[i] == entry["initial"]:
                message_parts[i] = ""

            if len(entry["initial"].split(" ")) != 0:
                initial_parts = entry["initial"].split(" ")

                check = False
                for j in range(len(initial_parts)):
                    if i + j >= len(message_parts):
                        check = True
                        break

                    if message_parts[i + j] != initial_parts[j]:
                        check = True
                        break

                if not check:
                    message_parts[i] = ""

    while "" in message_parts:
        message_parts.remove("")

    return " ".join(message_parts)
