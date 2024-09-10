import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import json


import db.settings
import db.keys
import db.channels


def main_form():
    error = False

    db_error, keys_usernames = db.keys.keys_entries_usernames()
    if db_error:
        error = True
        keys_usernames = list()

    db_error, current_username_in_use = db.settings.username_in_use()
    if db_error:
        error = True
        current_username_in_use = None

    db_error, channels_names = db.channels.channels_entries_names()
    if db_error:
        error = True
        channels_names = list()

    db_error, current_channel_in_use = db.settings.channel_in_use()
    if db_error:
        error = True
        current_channel_in_use = None

    db_error, last_messages_entries_on_page = (
        db.settings.last_messages_entries_on_page()
    )
    if db_error:
        error = True
        last_messages_entries_on_page = 10

    db_error, last_messages_entries = db.messages.messages_entries(
        username=current_username_in_use,
        channel=current_channel_in_use,
        search_value="",
        active_page=1,
        messages_on_page=last_messages_entries_on_page,
    )
    if db_error:
        error = True
        last_messages_entries = list()

    select_title = dmc.Text(
        "Отправка сообщений",
        style={"fontSize": 40},
    )

    username_select = dmc.Stack(
        [
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        dmc.HoverCard(
                            children=[
                                dmc.HoverCardTarget(
                                    dmc.ThemeIcon(
                                        children=DashIconify(
                                            icon="bx:question-mark",
                                            width=32,
                                        ),
                                        variant="transparent",
                                    )
                                ),
                                dmc.HoverCardDropdown(
                                    [
                                        dmc.Text(
                                            children=[
                                                "Сообщения будут отправляться от выбранного пользователя. Добавить пользователя можно на странице ",
                                                dmc.Anchor(
                                                    children="ключей",
                                                    href="/keys",
                                                ),
                                            ],
                                        ),
                                    ]
                                ),
                            ],
                            withArrow=True,
                            zIndex=12000,
                        ),
                        span="content",
                    ),
                    dmc.GridCol(
                        dmc.Select(
                            id="main_page_select_username_select",
                            label="Имя пользователя",
                            data=[
                                {"value": item["username"], "label": item["username"]}
                                for item in keys_usernames
                            ],
                            value=current_username_in_use,
                            disabled=True if current_username_in_use else False,
                            size="md",
                            # [note] read about allowDeselect
                        ),
                        span="auto",
                    ),
                ],
                align="flex-end",
            ),
            dmc.Button(
                id="main_page_select_username_button",
                children=(
                    current_username_in_use
                    if current_username_in_use
                    else "Подтвердить"
                ),
                color="green" if current_username_in_use else "blue",
                size="md",
            ),
        ]
    )

    channel_select = dmc.Stack(
        [
            dmc.Grid(
                [
                    dmc.GridCol(
                        dmc.HoverCard(
                            children=[
                                dmc.HoverCardTarget(
                                    dmc.ThemeIcon(
                                        children=DashIconify(
                                            icon="bx:question-mark",
                                            width=32,
                                        ),
                                        variant="transparent",
                                    )
                                ),
                                dmc.HoverCardDropdown(
                                    [
                                        dmc.Text(
                                            children=[
                                                "Канал, в чат которого будут отправляться сообщения. Добавить канал можно на странице ",
                                                dmc.Anchor(
                                                    children="каналов",
                                                    href="/channels",
                                                ),
                                            ],
                                        ),
                                    ]
                                ),
                            ],
                            withArrow=True,
                            zIndex=12000,
                        ),
                        span="content",
                    ),
                    dmc.GridCol(
                        dmc.Select(
                            id="main_page_select_channel_select",
                            label="Канал",
                            data=[
                                {"value": item["name"], "label": item["name"]}
                                for item in channels_names
                            ],
                            value=current_channel_in_use,
                            disabled=True if current_channel_in_use else False,
                            size="md",
                        ),
                        span="auto",
                    ),
                ],
                align="flex-end",
            ),
            dmc.Button(
                id="main_page_select_channel_button",
                children=(
                    current_channel_in_use if current_channel_in_use else "Подтвердить"
                ),
                color="green" if current_channel_in_use else "blue",
                size="md",
            ),
        ]
    )

    select_group = dmc.Group(
        [
            username_select,
            channel_select,
        ],
        grow=True,
    )

    last_messages_title = dmc.Group(
        [
            dmc.Text(
                "Последние сообщения",
                style={"fontSize": 40},
            ),
            dmc.NumberInput(
                id="main_page_last_messages_on_page_input",
                label="Количество записей на странице",
                value=last_messages_entries_on_page,
                min=1,
                step=1,
                size="md",
                w=300,
            ),
        ],
        justify="space-between",
    )

    last_messages_content = dmc.Stack(
        id="main_page_last_messages_list",
        children=last_messages_list(last_messages_entries),
        gap="xs",
    )

    main_form = dmc.Stack(
        [
            select_title,
            select_group,
            dmc.Divider(variant="solid", size="xl"),
            last_messages_title,
            last_messages_content,
        ],
        gap="md",
    )

    return (
        error,
        main_form,
    )


@dash.callback(
    dash.Output("main_page_last_messages_list", "children", allow_duplicate=True),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("main_page_last_messages_on_page_input", "value"),
    prevent_initial_call=True,
)
def handle_last_messages_entries_on_page_input(entries_on_page_value):
    if type(entries_on_page_value) != int:
        entries_on_page_value = 10

    elif entries_on_page_value <= 0:
        entries_on_page_value = 10

    patched_last_messages_list = dash.Patch()

    error = False

    if dash.callback_context.triggered_id == "main_page_last_messages_on_page_input":
        db_error = db.settings.set_last_messages_entries_on_page(entries_on_page_value)[
            0
        ]
        if db_error:
            error = True

        db_error, current_username_in_use = db.settings.username_in_use()
        if db_error:
            error = True
            current_username_in_use = None

        db_error, current_channel_in_use = db.settings.channel_in_use()
        if db_error:
            error = True
            current_channel_in_use = None

        db_error, last_messages_entries = db.messages.messages_entries(
            username=current_username_in_use,
            channel=current_channel_in_use,
            search_value="",
            active_page=1,
            messages_on_page=entries_on_page_value,
        )
        if db_error:
            error = True

        else:
            patched_last_messages_list = last_messages_list(last_messages_entries)

    return (
        patched_last_messages_list,
        not error,
    )


@dash.callback(
    dash.Output("main_page_last_messages_list", "children", allow_duplicate=True),
    dash.Input("main_page_interval", "n_intervals"),
    prevent_initial_call=True,
)
def handle_interval(n_intervals):
    error = False

    patched_last_messages_list = dash.Patch()

    if dash.callback_context.triggered_id == "main_page_interval":
        db_error, current_username_in_use = db.settings.username_in_use()
        if db_error:
            error = True
            current_username_in_use = None

        db_error, current_channel_in_use = db.settings.channel_in_use()
        if db_error:
            error = True
            current_channel_in_use = None

        db_error, last_messages_entries_on_page = (
            db.settings.last_messages_entries_on_page()
        )
        if db_error:
            error = True
            last_messages_entries_on_page = 10

        db_error, last_messages_entries = db.messages.messages_entries(
            username=current_username_in_use,
            channel=current_channel_in_use,
            search_value="",
            active_page=1,
            messages_on_page=last_messages_entries_on_page,
        )
        if db_error:
            error = True

        else:
            patched_last_messages_list = last_messages_list(last_messages_entries)

    return patched_last_messages_list


@dash.callback(
    dash.Output("main_page_select_username_button", "children"),
    dash.Output("main_page_select_username_button", "color"),
    dash.Output("main_page_select_username_select", "disabled"),
    dash.Output("main_page_select_channel_button", "children"),
    dash.Output("main_page_select_channel_button", "color"),
    dash.Output("main_page_select_channel_select", "disabled"),
    dash.Output("base_page_toggle_twitch_button", "disabled"),
    dash.Output("base_page_toggle_twitch_button", "color", allow_duplicate=True),
    dash.Output("main_page_last_messages_list", "children"),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("main_page_select_username_button", "n_clicks"),
    dash.State("main_page_select_username_select", "value"),
    dash.Input("main_page_select_channel_button", "n_clicks"),
    dash.State("main_page_select_channel_select", "value"),
    prevent_initial_call=True,
)
def handle_select_buttons(
    select_username_button,
    select_username_select_value,
    select_channel_button,
    select_channel_select_value,
):
    error = False

    patched_select_username_button_children = dash.Patch()
    patched_select_username_button_color = dash.Patch()
    patched_select_username_select_disabled = dash.Patch()

    patched_select_channel_button_children = dash.Patch()
    patched_select_channel_button_color = dash.Patch()
    patched_select_channel_select_disabled = dash.Patch()

    patched_toggle_twitch_button_disabled = dash.Patch()
    patched_toggle_twitch_button_color = dash.Patch()

    patched_last_messages_list = dash.Patch()

    if dash.callback_context.triggered_id == "main_page_select_username_button":
        db_error, current_username_in_use = db.settings.username_in_use()
        if db_error:
            error = True
            current_username_in_use = None

        if current_username_in_use == None and select_username_select_value:
            db_error = db.settings.set_username_in_use(select_username_select_value)[0]
            if db_error:
                error = True

            patched_select_username_button_children = select_username_select_value
            patched_select_username_button_color = "green"
            patched_select_username_select_disabled = True

        else:
            db_error = db.settings.set_username_in_use(None)[0]
            if db_error:
                error = True

            patched_select_username_button_children = "Подтвердить"
            patched_select_username_button_color = "blue"
            patched_select_username_select_disabled = False

    if dash.callback_context.triggered_id == "main_page_select_channel_button":
        db_error, current_channel_in_use = db.settings.channel_in_use()
        if db_error:
            error = True
            current_channel_in_use = None

        if current_channel_in_use == None and select_channel_select_value:
            db_error = db.settings.set_channel_in_use(select_channel_select_value)[0]
            if db_error:
                error = True

            patched_select_channel_button_children = select_channel_select_value
            patched_select_channel_button_color = "green"
            patched_select_channel_select_disabled = True

        else:
            db_error = db.settings.set_channel_in_use(None)[0]
            if db_error:
                error = True

            patched_select_channel_button_children = "Подтвердить"
            patched_select_channel_button_color = "blue"
            patched_select_channel_select_disabled = False

    db_error, current_username_in_use = db.settings.username_in_use()
    if db_error:
        error = True
        current_username_in_use = None

    db_error, current_channel_in_use = db.settings.channel_in_use()
    if db_error:
        error = True
        current_channel_in_use = None

    db_error, last_messages_entries_on_page = (
        db.settings.last_messages_entries_on_page()
    )
    if db_error:
        error = True
        last_messages_entries_on_page = 10

    db_error, last_messages_entries = db.messages.messages_entries(
        username=current_username_in_use,
        channel=current_channel_in_use,
        search_value="",
        active_page=1,
        messages_on_page=last_messages_entries_on_page,
    )
    if db_error:
        error = True

    else:
        patched_last_messages_list = last_messages_list(last_messages_entries)

    if current_username_in_use and current_channel_in_use:
        patched_toggle_twitch_button_disabled = False

    else:
        db_error = db.settings.set_twitch_on(False)[0]

        if db_error:
            error = True
        else:
            patched_toggle_twitch_button_disabled = True
            patched_toggle_twitch_button_color = "red"

    return (
        patched_select_username_button_children,
        patched_select_username_button_color,
        patched_select_username_select_disabled,
        patched_select_channel_button_children,
        patched_select_channel_button_color,
        patched_select_channel_select_disabled,
        patched_toggle_twitch_button_disabled,
        patched_toggle_twitch_button_color,
        patched_last_messages_list,
        not error,
    )


def last_messages_list(data):
    last_messages_list = [last_messages_list_item(data[i]) for i in range(len(data))]

    return last_messages_list


def last_messages_list_item(data):
    list_item = dmc.Card(
        children=[
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        dmc.TextInput(
                            value=data["channel"] if data["channel"] else "",
                            size="md",
                        ),
                        span=1,
                    ),
                    dmc.GridCol(
                        dmc.ThemeIcon(
                            children=DashIconify(
                                icon=(
                                    "material-symbols:mail-rounded"
                                    if data["is_sent"]
                                    else "material-symbols:mail-off-rounded"
                                ),
                                width=32,
                                color="green" if data["is_sent"] else "red",
                            ),
                            variant="transparent",
                            size="xl",
                        ),
                        span="content",
                    ),
                    dmc.GridCol(
                        dmc.TextInput(
                            id={
                                "type": "messages_page_datetime_input",
                                "index": data["rowid"],
                            },
                            value=data["datetime"],
                            size="md",
                            w=180,
                        ),
                        span="content",
                    ),
                    dmc.GridCol(
                        dmc.TextInput(
                            value=(data["username"] if data["username"] else ""),
                            size="md",
                        ),
                        span=1,
                    ),
                    dmc.GridCol(
                        dmc.TextInput(
                            id={
                                "type": "messages_page_text_input",
                                "index": data["rowid"],
                            },
                            value=data["text"],
                            size="md",
                        ),
                        span="auto",
                    ),
                ],
                gutter="xs",
                align="center",
            ),
            dash.html.Div(
                id={
                    "type": "dummy_index_holder",
                    "index": data["rowid"],
                },
                children=data["rowid"],
                style={"display": "none"},
            ),
        ],
        withBorder=True,
        radius="md",
        padding="xs",
    )

    return list_item


def main_page():
    error = False

    db_error, main_form_content = main_form()
    if db_error:
        error = True
        main_form_content = None

    main_page = dash.html.Div(
        [
            dash.dcc.Location("main_page_url"),
            dash.dcc.Interval(
                id="main_page_interval",
                interval=1000,
                n_intervals=0,
            ),
            main_form_content,
        ]
    )

    return (
        error,
        main_page,
    )
