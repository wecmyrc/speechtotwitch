import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import json
import collections


import db.settings
import db.channels


def channels_form():
    error = False

    db_error, channels_entries_on_page = db.settings.channels_entries_on_page()
    if db_error:
        error = True
        channels_entries_on_page = 10

    db_error, channels_pages = db.channels.channels_pagination_pages(
        "", channels_entries_on_page
    )
    if db_error:
        error = True
        channels_pages = 1

    db_error, channels_entries = db.channels.channels_entries(
        "", 1, channels_entries_on_page
    )
    if db_error:
        error = True
        channels_entries = list()

    add_entry_title = dmc.Stack(
        [
            dmc.Text(
                "Добавить новую запись",
                style={"fontSize": 40},
            ),
        ],
        gap="md",
    )

    add_entry_inputs = dmc.Stack(
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
                            id="channels_page_add_entry_name_input",
                            label="Название канала",
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
                            id="channels_page_add_entry_tag_input",
                            label="Тег",
                            size="md",
                        ),
                        span="auto",
                    ),
                ],
                align="flex-end",
            ),
            dmc.Button(
                id="channels_page_add_entry_button",
                children="Добавить запись",
                disabled=True,
                size="md",
            ),
        ],
        gap="md",
    )

    my_entries_title = dmc.Stack(
        [
            dmc.Group(
                [
                    dmc.Text(
                        "Мои записи",
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
                                    id="channels_page_save_changes_button",
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
                id="channels_page_search_input",
                placeholder="Поиск",
                size="md",
                rightSection=dmc.ActionIcon(
                    id="channels_page_search_input_clear_action",
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

    my_entries_controls = dmc.Group(
        [
            dmc.NumberInput(
                id="channels_page_entries_on_page_input",
                label="Количество записей на странице",
                value=channels_entries_on_page,
                min=1,
                step=1,
                size="md",
                w=300,
            ),
            dmc.Pagination(
                id="channels_page_pagination",
                total=channels_pages,
                siblings=2,
                value=1,
                size="md",
            ),
            dmc.Button(
                id="channels_page_delete_all_entries_button",
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

    my_entries_content = dmc.Stack(
        id="channels_page_entries_list",
        children=channels_entries_list(channels_entries),
        gap="xs",
    )

    channels_form = dmc.Stack(
        [
            add_entry_title,
            add_entry_inputs,
            dmc.Divider(variant="solid", size="xl"),
            my_entries_title,
            my_entries_controls,
            my_entries_content,
        ],
        gap="md",
    )

    return (
        error,
        channels_form,
    )


@dash.callback(
    dash.Output("channels_page_add_entry_button", "disabled"),
    dash.Input("channels_page_add_entry_name_input", "value"),
)
def handle_add_entry_inputs(name_value):
    if name_value:
        return False
    else:
        return True


@dash.callback(
    dash.Output("channels_page_search_input", "value"),
    dash.Input("channels_page_search_input_clear_action", "n_clicks"),
    prevent_initial_call=True,
)
def handle_search_input_clear_action(n_clicks):
    patched_search_input_value = dash.Patch()

    if dash.callback_context.triggered_id == "channels_page_search_input_clear_action":
        patched_search_input_value = ""

    return patched_search_input_value


@dash.callback(
    dash.Output("channels_page_entries_list", "children"),
    dash.Output("channels_page_pagination", "total"),
    dash.Output("channels_page_pagination", "value"),
    dash.Output("channels_page_already_exist_modal", "opened"),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("channels_page_add_entry_button", "n_clicks"),
    dash.Input("channels_page_search_input", "value"),
    dash.Input("channels_page_pagination", "value"),
    dash.Input("channels_page_entries_on_page_input", "value"),
    dash.Input(
        {
            "type": "channels_page_channels_entries_list_item_delete_button",
            "index": dash.ALL,
        },
        "n_clicks",
    ),
    dash.Input("channels_page_delete_all_entries_button", "n_clicks"),
    dash.State("channels_page_add_entry_name_input", "value"),
    dash.State("channels_page_add_entry_tag_input", "value"),
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
    add_entry_button,
    search_input_value,
    pagination_value,
    entries_on_page_value,
    delete_entry_buttons,
    delete_all_entries_button,
    name_value,
    tag_value,
    dummy_indexes,
):
    error = False

    new_entries_list = None
    new_pagination_total = None
    new_already_exist_modal_opened = None

    if dash.callback_context.triggered_id == "channels_page_entries_on_page_input":
        if db.settings.set_channels_entries_on_page(entries_on_page_value)[0]:
            error = True

    if 1 in delete_entry_buttons:
        rowid = dummy_indexes[delete_entry_buttons.index(1)]
        if db.channels.delete_channels_entry(rowid)[0]:
            error = True

    if dash.callback_context.triggered_id == "channels_page_delete_all_entries_button":
        if db.channels.delete_all_channels_entries()[0]:
            error = True

    if dash.callback_context.triggered_id == "channels_page_add_entry_button":
        db_error, is_channels_entry_exists = db.channels.is_channels_entry_exists(
            name_value.lower()
        )
        if db_error:
            error = True

        elif is_channels_entry_exists:
            new_already_exist_modal_opened = True

        elif not is_channels_entry_exists:
            if db.channels.add_channels_entry(
                name_value.lower(),
                tag_value,
            )[0]:
                error = True

    db_error, result = db.channels.channels_entries(
        search_input_value,
        pagination_value,
        entries_on_page_value,
    )
    if db_error:
        error = True
    else:
        new_entries_list = channels_entries_list(result)

    if len(result) == 0 and pagination_value != 1:
        pagination_value = 1

        db_error, result = db.channels.channels_entries(
            search_input_value,
            pagination_value,
            entries_on_page_value,
        )
        if db_error:
            error = True
        else:
            new_entries_list = channels_entries_list(result)

    db_error, result = db.channels.channels_pagination_pages(
        search_input_value,
        entries_on_page_value,
    )
    if db_error:
        error = True
    else:
        new_pagination_total = result

    return (
        new_entries_list,
        new_pagination_total,
        pagination_value,
        new_already_exist_modal_opened,
        not error,
    )


@dash.callback(
    dash.Output("base_page_toggle_twitch_button", "disabled", allow_duplicate=True),
    dash.Output("base_page_toggle_twitch_button", "color", allow_duplicate=True),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input(
        {
            "type": "channels_page_channels_entries_list_item_delete_button",
            "index": dash.ALL,
        },
        "n_clicks",
    ),
    dash.State(
        {
            "type": "channels_page_channels_entries_list_item_name_input",
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
def check_channel_in_use_on_delete(
    delete_entry_buttons, name_inputs_values, dummy_indexes
):
    error = False

    # [note] this callback fires when button didnt click

    patched_toggle_twitch_button_disabled = dash.Patch()
    patched_toggle_twitch_button_color = dash.Patch()

    if 1 in delete_entry_buttons:
        db_error, current_channel_in_use = db.settings.channel_in_use()
        if db_error:
            error = True
            current_channel_in_use = None

        deleted_name = name_inputs_values[delete_entry_buttons.index(1)]

        if current_channel_in_use == deleted_name:
            db_error = db.settings.set_channel_in_use(None)[0]
            if db_error:
                error = True

            db_error = db.settings.set_twitch_on(False)[0]
            if db_error:
                error = True

    db_error, current_channel_in_use = db.settings.channel_in_use()
    if db_error:
        error = True
        twitch_on = False

    if not current_channel_in_use:
        patched_toggle_twitch_button_disabled = True
        patched_toggle_twitch_button_color = "red"

    return (
        patched_toggle_twitch_button_disabled,
        patched_toggle_twitch_button_color,
        not error,
    )


def channels_entries_list(data):
    channels_entries_list = [
        channels_entries_list_item(data[i]) for i in range(len(data))
    ]

    return channels_entries_list


def channels_entries_list_item(data):
    list_item = dmc.Card(
        children=[
            dmc.Grid(
                [
                    dmc.GridCol(
                        dmc.TextInput(
                            id={
                                "type": "channels_page_channels_entries_list_item_name_input",
                                "index": data["rowid"],
                            },
                            value=data["name"],
                            label="Название канала",
                            placeholder="forsen",
                            size="md",
                        ),
                        span="auto",
                    ),
                    dmc.GridCol(
                        dmc.TextInput(
                            id={
                                "type": "channels_page_channels_entries_list_item_tag_input",
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
                                "type": "channels_page_channels_entries_list_item_delete_button",
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
    dash.Output("channels_page_changes_saved_success_modal", "opened"),
    dash.Output("channels_page_changes_saved_failure_modal", "opened"),
    dash.Output(
        "channels_page_changes_saved_failure_modal_additional_info", "children"
    ),
    dash.Input("channels_page_save_changes_button", "n_clicks"),
    dash.State(
        {
            "type": "channels_page_channels_entries_list_item_name_input",
            "index": dash.ALL,
        },
        "value",
    ),
    dash.State(
        {
            "type": "channels_page_channels_entries_list_item_tag_input",
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
    name_inputs_values,
    tag_inputs_values,
    dummy_indexes,
):
    error = False

    name_inputs_values[:] = [a.lower() for a in name_inputs_values]

    if dash.callback_context.triggered_id == "channels_page_save_changes_button":
        if str() in name_inputs_values:
            additional_info = dmc.Stack(
                [
                    dmc.Text("Изменения не были сохранены"),
                    dmc.Text("Не заполнены все обязательные поля (название канала)"),
                ]
            )

            return (
                False,
                True,
                additional_info,
            )

        if len(name_inputs_values) != len(set(name_inputs_values)):
            duplicates = [
                item
                for item, count in collections.Counter(name_inputs_values).items()
                if count > 1
            ]

            additional_info = dmc.Stack(
                [
                    dmc.Text("Изменения не были сохранены"),
                    dmc.Text("Дубликаты в начальных формах:"),
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
                name_inputs_values[i],
                tag_inputs_values[i],
                dummy_indexes[i],
            )
            for i in range(len(name_inputs_values))
        ]
        if db.channels.update_channels_entries(data)[0]:
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


def channels_page():
    error = False

    db_error, channels_form_content = channels_form()
    if db_error:
        error = True
        channels_form_content = None

    error_modal = dmc.Modal(
        id="channels_page_already_exist_modal",
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
        id="channels_page_changes_saved_success_modal",
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
        id="channels_page_changes_saved_failure_modal",
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
            id="channels_page_changes_saved_failure_modal_additional_info",
        ),
        centered=True,
        opened=False,
    )

    channels_page = dash.html.Div(
        [
            dash.dcc.Location("channels_page_url"),
            error_modal,
            changes_saved_success_modal,
            changes_saved_failure_modal,
            channels_form_content,
        ]
    )

    return (
        error,
        channels_page,
    )
