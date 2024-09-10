import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import json
import datetime


import db.settings
import db.messages


def messages_form():
    error = False

    db_error, messages_entries_limit = db.settings.messages_entries_limit()
    if db_error:
        error = True
        messages_entries_limit = 1000

    db_error, messages_entries_on_page = db.settings.messages_entries_on_page()
    if db_error:
        error = True
        messages_entries_on_page = 10

    db_error, messages_pagination_pages = db.messages.messages_pagination_pages(
        "", messages_entries_on_page
    )
    if db_error:
        error = True
        messages_pagination_pages = 1

    db_error, messages_entries = db.messages.messages_entries(
        username=None,
        channel=None,
        search_value="",
        active_page=1,
        messages_on_page=messages_entries_on_page,
    )
    if db_error:
        error = True
        messages_entries = list()

    title = dmc.Stack(
        [
            dmc.Group(
                [
                    dmc.Text(
                        "Мои сообщения",
                        style={"fontSize": 40},
                    ),
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
                                                        "Старые сообщения будут удаляться",
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
                                dmc.Group(
                                    [
                                        dmc.Text("Хранить не более"),
                                        dmc.NumberInput(
                                            id="messages_page_messages_limit_input",
                                            value=messages_entries_limit,
                                            min=0,
                                            step=1,
                                            size="md",
                                            w=300,
                                        ),
                                        dmc.ActionIcon(
                                            id="messages_page_messages_limit_save_button",
                                            children=DashIconify(
                                                icon="bx:check",
                                                height=26,
                                            ),
                                            color="green",
                                            size="xl",
                                        ),
                                    ]
                                ),
                                span="content",
                            ),
                        ],
                        align="flex-end",
                    ),
                ],
                justify="space-between",
            ),
            dmc.TextInput(
                id="messages_page_search_input",
                placeholder="Поиск",
                size="md",
                rightSection=dmc.ActionIcon(
                    id="messages_page_search_input_clear_action",
                    children=DashIconify(
                        icon="jam:delete",
                        height=20,
                    ),
                    variant="transparent",
                    size="xl",
                ),
            ),
        ],
        gap="md",
    )

    controls = dmc.Group(
        [
            dmc.NumberInput(
                id="messages_page_messages_on_page_input",
                label="Количество записей на странице",
                value=messages_entries_on_page,
                min=1,
                step=1,
                size="md",
                w=300,
            ),
            dmc.Pagination(
                id="messages_page_pagination",
                total=messages_pagination_pages,
                siblings=2,
                value=1,
                size="md",
            ),
            dmc.Button(
                id="messages_page_delete_all_messages_button",
                children="Удалить всё",
                size="md",
                color="red",
                w=300,
                leftSection=DashIconify(
                    icon="mingcute:delete-2-line",
                    height=20,
                ),
            ),
        ],
        justify="space-between",
    )

    content = dmc.Stack(
        id="messages_page_messages_list",
        children=messages_list(messages_entries),
        gap="xs",
    )

    messages_form = dmc.Stack(
        [
            title,
            controls,
            content,
        ],
        gap="md",
    )

    return (
        error,
        messages_form,
    )


@dash.callback(
    dash.Output("messages_page_search_input", "value"),
    dash.Input("messages_page_search_input_clear_action", "n_clicks"),
    prevent_initial_call=True,
)
def handle_search_input_clear_action(n_clicks):
    patched_search_input_value = dash.Patch()

    if dash.callback_context.triggered_id == "messages_page_search_input_clear_action":
        patched_search_input_value = ""

    return patched_search_input_value


def messages_list(data):
    messages_list = [messages_list_item(data[i]) for i in range(len(data))]

    return messages_list


def messages_list_item(data):
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
                            value=data["username"] if data["username"] else "",
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
                    dmc.GridCol(
                        dmc.Group(
                            dmc.ActionIcon(
                                id={
                                    "type": "messages_page_messages_list_delete_button",
                                    "index": data["rowid"],
                                },
                                children=DashIconify(
                                    icon="radix-icons:cross-circled",
                                    width=26,
                                ),
                                size="lg",
                                color="red",
                            ),
                        ),
                        span="content",
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
        # [note] style={"backgroundColor": "#ff8787"},
        withBorder=True,
        radius="md",
        padding="xs",
    )

    return list_item


@dash.callback(
    dash.Output("messages_page_messages_list", "children"),
    dash.Output("messages_page_pagination", "total"),
    dash.Output("messages_page_pagination", "value"),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("messages_page_search_input", "value"),
    dash.Input(
        {
            "type": "messages_page_messages_list_delete_button",
            "index": dash.ALL,
        },
        "n_clicks",
    ),
    dash.Input("messages_page_delete_all_messages_button", "n_clicks"),
    dash.Input("messages_page_messages_on_page_input", "value"),
    dash.Input("messages_page_messages_limit_save_button", "n_clicks"),
    dash.Input("messages_page_interval", "n_intervals"),
    dash.Input("messages_page_pagination", "value"),
    dash.State("messages_page_messages_limit_input", "value"),
    dash.State(
        {
            "type": "messages_page_datetime_input",
            "index": dash.ALL,
        },
        "value",
    ),
    dash.State(
        {
            "type": "dummy_index_holder",
            "index": dash.ALL,
        },
        "children",
    ),
    prevent_initial_call=True,
)
def handle_buttons(
    search_input_value,
    delete_buttons_n_clicks,
    delete_all_button_n_clicks,
    messages_on_page_input_value,
    messages_limit_save_button,
    n_intervals,
    pagination_active_page,
    messages_limit_input_value,
    datetime_input_values,
    dummy_indexes,
):
    patched_messages_list = dash.Patch()
    patched_messages_pagination_total = dash.Patch()
    patched_messages_pagination_value = dash.Patch()

    error = False

    if dash.callback_context.triggered_id == "messages_page_search_input":
        db_error, result = db.messages.messages_pagination_pages(
            search_input_value,
            messages_on_page_input_value,
        )
        if db_error:
            error = True
        else:
            patched_messages_pagination_total = result

    if dash.callback_context.triggered_id == "messages_page_messages_on_page_input":
        db_error = db.settings.set_messages_entries_on_page(
            messages_on_page_input_value
        )[0]
        if db_error:
            error = True

    if dash.callback_context.triggered_id == "messages_page_messages_limit_save_button":
        db.settings.set_messages_entries_limit(messages_limit_input_value)
        db.messages.handle_messages_limit()

        db_error, result = db.messages.messages_pagination_pages(
            search_input_value,
            messages_on_page_input_value,
        )
        if db_error:
            error = True
        else:
            patched_messages_pagination_total = result

    if 1 in delete_buttons_n_clicks:
        rowid = dummy_indexes[delete_buttons_n_clicks.index(1)]
        db_error = db.messages.delete_messages_entry(rowid)[0]
        if db_error:
            error = True

    if dash.callback_context.triggered_id == "messages_page_delete_all_messages_button":
        db_error = db.messages.delete_all_messages_entries()[0]
        if db_error:
            error = True

    db_error, page_rowids = db.messages.messages_entries_page_rowids(
        search_input_value,
        pagination_active_page,
        messages_on_page_input_value,
    )
    if db_error:
        error = True
        page_rowids = list()

    if dummy_indexes != page_rowids:
        db_error, messages = db.messages.messages_entries(
            username=None,
            channel=None,
            search_value=search_input_value,
            active_page=pagination_active_page,
            messages_on_page=messages_on_page_input_value,
        )
        if db_error:
            error = True
        else:
            patched_messages_list = messages_list(messages)

        db_error, result = db.messages.messages_pagination_pages(
            search_input_value,
            messages_on_page_input_value,
        )
        if db_error:
            error = True
        else:
            patched_messages_pagination_total = result

    if len(datetime_input_values) == 0 and pagination_active_page != 1:
        patched_messages_pagination_value = 1

        db_error, messages = db.messages.messages_entries(
            username=None,
            channel=None,
            search_value=search_input_value,
            active_page=patched_messages_pagination_value,
            messages_on_page=messages_on_page_input_value,
        )
        if db_error:
            error = True
        else:
            patched_messages_list = messages_list(messages)

        db_error, result = db.messages.messages_pagination_pages(
            search_input_value,
            messages_on_page_input_value,
        )
        if db_error:
            error = True
        else:
            patched_messages_pagination_total = result

    return (
        patched_messages_list,
        patched_messages_pagination_total,
        patched_messages_pagination_value,
        not error,
    )


def messages_page():
    error = False

    db_error, messages_form_content = messages_form()
    if db_error:
        error = True
        messages_form_content = None

    messages_page = dash.html.Div(
        [
            dash.dcc.Location("messages_page_url"),
            dash.html.Div(id="messages_page_dummy_output", style={"display": "none"}),
            dash.dcc.Interval(
                id="messages_page_interval",
                interval=1000,
                n_intervals=0,
            ),
            messages_form_content,
        ]
    )

    return (
        error,
        messages_page,
    )
