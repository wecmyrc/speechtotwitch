import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import json
import collections


import db.settings
import db.keys


def keys_form():
    error = False

    db_error, keys_entries_on_page = db.settings.keys_entries_on_page()
    if db_error:
        error = True
        keys_entries_on_page = 10

    db_error, keys_pagination_pages = db.keys.keys_pagination_pages(
        "", keys_entries_on_page
    )
    if db_error:
        error = True
        keys_pagination_pages = 1

    db_error, keys_entries = db.keys.keys_entries("", 1, keys_entries_on_page)
    if db_error:
        error = True
        keys_entries = list()

    add_key_title = dmc.Stack(
        [
            dmc.Text(
                "Добавить новый ключ",
                style={"fontSize": 40},
            ),
        ],
        gap="md",
    )

    add_key_inputs = dmc.Stack(
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
                                                "Не ссылка",
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
                        dmc.TextInput(
                            id="keys_page_add_key_username_input",
                            label="Имя пользователя",
                            placeholder="forsen",
                            size="md",
                            required=True,
                        ),
                        span="auto",
                    ),
                ],
                align="flex-end",
            ),
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
                                                "Получить OAuth можно ",
                                                dmc.Anchor(
                                                    children="тут",
                                                    href="https://twitchapps.com/tmi/",
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
                        dmc.PasswordInput(
                            id="keys_page_add_key_oauth_input",
                            label="OAuth",
                            placeholder="oauth:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            size="md",
                            required=True,
                        ),
                        span="auto",
                    ),
                ],
                align="flex-end",
            ),
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
                                                "Помогает при поиске. Можно не указывать",
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
                        dmc.TextInput(
                            id="keys_page_add_key_tag_input",
                            label="Тег",
                            size="md",
                        ),
                        span="auto",
                    ),
                ],
                align="flex-end",
            ),
            dmc.Button(
                id="keys_page_add_key_button",
                children="Добавить ключ",
                disabled=True,
                size="md",
            ),
        ],
        gap="md",
    )

    my_keys_title = dmc.Stack(
        [
            dmc.Group(
                [
                    dmc.Text(
                        "Мои ключи",
                        style={"fontSize": 40},
                    ),
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
                                                        "Внесенные изменения в существующие записи сохраняются только после нажатия кнопки",
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
                                dmc.Button(
                                    id="keys_page_save_changes_button",
                                    children="Сохранить изменения",
                                    size="md",
                                    color="green",
                                    w=300,
                                    leftSection=DashIconify(
                                        icon="bx:save",
                                        height=20,
                                    ),
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
                id="keys_page_search_input",
                placeholder="Поиск",
                size="md",
                rightSection=dmc.ActionIcon(
                    id="keys_page_search_input_clear_action",
                    children=DashIconify(
                        icon="jam:delete",
                        height=20,
                    ),
                    variant="transparent",
                    size="xl",
                ),
            ),
        ]
    )

    my_keys_controls = dmc.Group(
        [
            dmc.NumberInput(
                id="keys_page_keys_on_page_input",
                label="Количество записей на странице",
                value=keys_entries_on_page,
                min=1,
                step=1,
                size="md",
                w=300,
            ),
            dmc.Pagination(
                id="keys_page_pagination",
                total=keys_pagination_pages,
                siblings=2,
                value=1,
                size="md",
            ),
            dmc.Button(
                id="keys_page_delete_all_keys_entries_button",
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

    my_keys_content = dmc.Stack(
        id="keys_page_keys_list",
        children=keys_list(keys_entries),
        gap="xs",
    )

    key_form = dmc.Stack(
        [
            add_key_title,
            add_key_inputs,
            dmc.Divider(variant="solid", size="xl"),
            my_keys_title,
            my_keys_controls,
            my_keys_content,
        ],
        gap="md",
    )

    return (
        error,
        key_form,
    )


@dash.callback(
    dash.Output("keys_page_add_key_button", "disabled"),
    dash.Input("keys_page_add_key_username_input", "value"),
    dash.Input("keys_page_add_key_oauth_input", "value"),
)
def handle_add_key_inputs(username_value, oauth_value):
    if username_value and oauth_value:
        return False
    else:
        return True


@dash.callback(
    dash.Output("keys_page_search_input", "value"),
    dash.Input("keys_page_search_input_clear_action", "n_clicks"),
    prevent_initial_call=True,
)
def handle_search_input_clear_action(n_clicks):
    patched_search_input_value = dash.Patch()

    if dash.callback_context.triggered_id == "keys_page_search_input_clear_action":
        patched_search_input_value = ""

    return patched_search_input_value


# NOTE seriously rewrite this piece of garbage with multiple callbacks and allow_duplicate


@dash.callback(
    dash.Output("keys_page_keys_list", "children"),
    dash.Output("keys_page_pagination", "total"),
    dash.Output("keys_page_pagination", "value"),
    dash.Output("keys_page_already_exist_modal", "opened"),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("keys_page_add_key_button", "n_clicks"),
    dash.Input("keys_page_search_input", "value"),
    dash.Input("keys_page_pagination", "value"),
    dash.Input("keys_page_keys_on_page_input", "value"),
    dash.Input(
        {
            "type": "keys_page_keys_list_item_delete_button",
            "index": dash.ALL,
        },
        "n_clicks",
    ),
    dash.Input("keys_page_delete_all_keys_entries_button", "n_clicks"),
    dash.State("keys_page_add_key_username_input", "value"),
    dash.State("keys_page_add_key_oauth_input", "value"),
    dash.State("keys_page_add_key_tag_input", "value"),
    dash.State(
        {
            "type": "dummy_index_holder",
            "index": dash.ALL,
        },
        "children",
    ),
    prevent_initial_call=True,
)
def handle_add_key_button(
    add_key_n_clicks,
    search_input_value,
    pagination_value,
    entries_on_page_value,
    delete_key_buttons,
    delete_all_keys_button,
    username_value,
    oauth_value,
    tag_value,
    dummy_indexes,
):
    if type(entries_on_page_value) != int:
        entries_on_page_value = 10

    elif entries_on_page_value <= 0:
        entries_on_page_value = 10

    error = False

    patched_keys_list_children = dash.Patch()
    patched_pagination_total = dash.Patch()
    patched_pagination_value = dash.Patch()  # NOTE no need
    patched_already_exist_modal_opened = dash.Patch()

    if dash.callback_context.triggered_id == "keys_page_keys_on_page_input":
        if db.settings.set_keys_entries_on_page(entries_on_page_value)[0]:
            error = True

    if 1 in delete_key_buttons:
        rowid = dummy_indexes[delete_key_buttons.index(1)]
        if db.keys.delete_keys_entry(rowid)[0]:
            error = True

    if dash.callback_context.triggered_id == "keys_page_delete_all_keys_entries_button":
        if db.keys.delete_all_keys_entries()[0]:
            error = True

    if dash.callback_context.triggered_id == "keys_page_add_key_button":
        db_error, is_key_exist = db.keys.is_keys_entry_exists(username_value)
        if db_error:
            error = True

        elif is_key_exist:
            patched_already_exist_modal_opened = True

        elif not is_key_exist:
            if db.keys.add_keys_entry(username_value, oauth_value, tag_value)[0]:
                error = True

    db_error, result = db.keys.keys_entries(
        search_input_value,
        pagination_value,
        entries_on_page_value,
    )
    if db_error:
        error = True
    else:
        patched_keys_list_children = keys_list(result)

    if len(result) == 0 and pagination_value != 1:
        pagination_value = 1

        db_error, result = db.keys.keys_entries(
            search_input_value,
            pagination_value,
            entries_on_page_value,
        )
        if db_error:
            error = True
        else:
            patched_keys_list_children = keys_list(result)

    db_error, result = db.keys.keys_pagination_pages(
        search_input_value,
        entries_on_page_value,
    )
    if db_error:
        error = True
    else:
        patched_pagination_total = result

    return (
        patched_keys_list_children,
        patched_pagination_total,
        pagination_value,
        patched_already_exist_modal_opened,
        not error,
    )


# NOTE add modal with message that key was in use
@dash.callback(
    dash.Output("base_page_toggle_twitch_button", "disabled", allow_duplicate=True),
    dash.Output("base_page_toggle_twitch_button", "color", allow_duplicate=True),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input(
        {
            "type": "keys_page_keys_list_item_delete_button",
            "index": dash.ALL,
        },
        "n_clicks",
    ),
    dash.State(
        {
            "type": "keys_page_keys_list_item_username_input",
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
def check_key_in_use_on_delete(
    delete_entry_buttons, username_inputs_values, dummy_indexes
):
    error = False

    patched_toggle_twitch_button_disabled = dash.Patch()
    patched_toggle_twitch_button_color = dash.Patch()

    if 1 in delete_entry_buttons:
        db_error, current_username_in_use = db.settings.username_in_use()
        if db_error:
            error = True
            current_username_in_use = None

        deleted_username = username_inputs_values[delete_entry_buttons.index(1)]

        if current_username_in_use == deleted_username:
            db_error = db.settings.set_username_in_use(None)[0]
            if db_error:
                error = True

            db_error = db.settings.set_twitch_on(False)[0]
            if db_error:
                error = True

    db_error, current_username_in_use = db.settings.username_in_use()
    if db_error:
        error = True
        twitch_on = False

    if not current_username_in_use:
        patched_toggle_twitch_button_disabled = True
        patched_toggle_twitch_button_color = "red"

    return (
        patched_toggle_twitch_button_disabled,
        patched_toggle_twitch_button_color,
        not error,
    )


def keys_list(data):
    keys_list = [keys_list_item(data[i]) for i in range(len(data))]

    return keys_list


def keys_list_item(data):
    list_item = dmc.Card(
        children=[
            dmc.Grid(
                [
                    dmc.GridCol(
                        dmc.TextInput(
                            id={
                                "type": "keys_page_keys_list_item_username_input",
                                "index": data["rowid"],
                            },
                            value=data["username"],
                            label="Имя пользователя",
                            placeholder="forsen",
                            size="md",
                        ),
                        span=3,
                    ),
                    dmc.GridCol(
                        dmc.PasswordInput(
                            id={
                                "type": "keys_page_keys_list_item_oauth_input",
                                "index": data["rowid"],
                            },
                            value=data["oauth"],
                            label="OAuth",
                            placeholder="oauth:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            size="md",
                        ),
                        span="auto",
                    ),
                    dmc.GridCol(
                        dmc.TextInput(
                            id={
                                "type": "keys_page_keys_list_item_tag_input",
                                "index": data["rowid"],
                            },
                            value=data["tag"],
                            label="Тег",
                            size="md",
                        ),
                        span=2,
                    ),
                    dmc.GridCol(
                        dmc.ActionIcon(
                            id={
                                "type": "keys_page_keys_list_item_delete_button",
                                "index": data["rowid"],
                            },
                            children=DashIconify(
                                icon="radix-icons:cross-circled",
                                width=26,
                            ),
                            size="lg",
                            color="red",
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
        withBorder=True,
        radius="md",
        padding="xs",
    )

    return list_item


@dash.callback(
    dash.Output("keys_page_changes_saved_success_modal", "opened"),
    dash.Output("keys_page_changes_saved_failure_modal", "opened"),
    dash.Output("keys_page_changes_saved_failure_modal_additional_info", "children"),
    dash.Input("keys_page_save_changes_button", "n_clicks"),
    dash.State(
        {
            "type": "keys_page_keys_list_item_username_input",
            "index": dash.ALL,
        },
        "value",
    ),
    dash.State(
        {
            "type": "keys_page_keys_list_item_oauth_input",
            "index": dash.ALL,
        },
        "value",
    ),
    dash.State(
        {
            "type": "keys_page_keys_list_item_tag_input",
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
def handle_save_changes(
    save_changes_button,
    username_inputs_values,
    oauth_inputs_values,
    tag_inputs_values,
    dummy_indexes,
):
    error = False

    username_inputs_values[:] = [a.lower() for a in username_inputs_values]

    if dash.callback_context.triggered_id == "keys_page_save_changes_button":
        if str() in username_inputs_values or str() in oauth_inputs_values:
            additional_info = dmc.Stack(
                [
                    dmc.Text("Изменения не были сохранены"),
                    dmc.Text(
                        "Не заполнены все обязательные поля (имя пользователя, oauth)"
                    ),
                ]
            )

            return (
                False,
                True,
                additional_info,
            )

        if len(username_inputs_values) != len(set(username_inputs_values)):
            duplicates = [
                item
                for item, count in collections.Counter(username_inputs_values).items()
                if count > 1
            ]

            additional_info = dmc.Stack(
                [
                    dmc.Text("Изменения не были сохранены"),
                    dmc.Text("Дубликаты в именах пользователей:"),
                    dmc.List([dmc.ListItem(item) for item in duplicates]),
                ]
            )

            return (
                False,
                True,
                additional_info,
            )

        data = [
            (
                username_inputs_values[i],
                oauth_inputs_values[i],
                tag_inputs_values[i],
                dummy_indexes[i],
            )
            for i in range(len(username_inputs_values))
        ]
        if db.keys.update_keys_entries(data)[0]:
            error = True

        additional_info = dmc.Stack(
            [
                dmc.Text("Изменения не были сохранены"),
                dmc.Text("Ошибка при записи в базу данных. Проверь логи"),
            ]
        )

        return (
            not error,
            error,
            additional_info,
        )

    return (
        False,
        False,
        None,
    )


def keys_page():
    error = False

    db_error, keys_form_content = keys_form()
    if db_error:
        error = True
        keys_form_content = None

    error_modal = dmc.Modal(
        id="keys_page_already_exist_modal",
        title=dmc.Group(
            [
                dmc.ThemeIcon(
                    children=DashIconify(
                        icon="bx:error-circle",
                        width=32,
                        color="orange",
                    ),
                    variant="transparent",
                ),
                dmc.Text(
                    children="Внимание!",
                ),
            ],
        ),
        children=dmc.Text("Такая запись уже существует"),
        centered=True,
        opened=False,
    )

    changes_saved_success_modal = dmc.Modal(
        id="keys_page_changes_saved_success_modal",
        title=dmc.Group(
            [
                dmc.ThemeIcon(
                    children=DashIconify(
                        icon="bx:bx-wink-smile",
                        width=32,
                        color="green",
                    ),
                    variant="transparent",
                ),
                dmc.Text(
                    children="Успешно!",
                ),
            ],
        ),
        children=dmc.Text("Изменения сохранены"),
        centered=True,
        opened=False,
    )

    changes_saved_failure_modal = dmc.Modal(
        id="keys_page_changes_saved_failure_modal",
        title=dmc.Group(
            [
                dmc.ThemeIcon(
                    children=DashIconify(
                        icon="bx:sad",
                        width=32,
                        color="red",
                    ),
                    variant="transparent",
                ),
                dmc.Text(
                    children="Ошибка!",
                ),
            ],
        ),
        children=dmc.Stack(
            id="keys_page_changes_saved_failure_modal_additional_info",
        ),
        centered=True,
        opened=False,
    )

    keys_page = dash.html.Div(
        [
            dash.dcc.Location("keys_page_url"),
            error_modal,
            changes_saved_success_modal,
            changes_saved_failure_modal,
            keys_form_content,
        ]
    )

    return (
        error,
        keys_page,
    )
