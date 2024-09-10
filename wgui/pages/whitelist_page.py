import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

import json
import collections


import db.settings
import db.whitelist


def whitelist_form():
    error = False

    db_error, whitelist_entries_on_page = db.settings.whitelist_entries_on_page()
    if db_error:
        error = True
        whitelist_entries_on_page = 10

    db_error, whitelist_pagination_pages = db.whitelist.whitelist_pagination_pages(
        "", whitelist_entries_on_page
    )
    if db_error:
        error = True
        whitelist_pagination_pages = 1

    db_error, whitelist_entries = db.whitelist.whitelist_entries(
        "", 1, whitelist_entries_on_page
    )
    if db_error:
        error = True
        whitelist_entries = list()

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
                                                "Последовательность слов, разделенных пробелами. При добавлении записи автоматически переводится в нижний регистр"
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
                            id="whitelist_page_add_entry_initial_input",
                            label="Исходная форма",
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
                                                "Помогает при поиске. Можно не указывать"
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
                            id="whitelist_page_add_entry_tag_input",
                            label="Тег",
                            size="md",
                        ),
                        span="auto",
                    ),
                ],
                align="flex-end",
            ),
            dmc.Button(
                id="whitelist_page_add_entry_button",
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
                                    id="whitelist_page_save_changes_button",
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
                id="whitelist_page_search_input",
                placeholder="Поиск",
                size="md",
                rightSection=dmc.ActionIcon(
                    id="whitelist_page_search_input_clear_action",
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
                id="whitelist_page_entries_on_page_input",
                label="Количество записей на странице",
                value=whitelist_entries_on_page,
                min=1,
                step=1,
                size="md",
                w=300,
            ),
            dmc.Pagination(
                id="whitelist_page_pagination",
                total=whitelist_pagination_pages,
                siblings=2,
                value=1,
                size="md",
            ),
            dmc.Button(
                id="whitelist_page_delete_all_entries_button",
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
        id="whitelist_page_entries_list",
        children=whitelist_entries_list(whitelist_entries),
        gap="xs",
    )

    whitelist_form = dmc.Stack(
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
        whitelist_form,
    )


@dash.callback(
    dash.Output("whitelist_page_add_entry_button", "disabled"),
    dash.Input("whitelist_page_add_entry_initial_input", "value"),
)
def handle_add_entry_inputs(initial_value):
    if initial_value:
        return False
    else:
        return True


@dash.callback(
    dash.Output("whitelist_page_search_input", "value"),
    dash.Input("whitelist_page_search_input_clear_action", "n_clicks"),
    prevent_initial_call=True,
)
def handle_search_input_clear_action(n_clicks):
    patched_search_input_value = dash.Patch()

    if dash.callback_context.triggered_id == "whitelist_page_search_input_clear_action":
        patched_search_input_value = ""

    return patched_search_input_value


@dash.callback(
    dash.Output("whitelist_page_entries_list", "children"),
    dash.Output("whitelist_page_pagination", "total"),
    dash.Output("whitelist_page_pagination", "value"),
    dash.Output("whitelist_page_already_exist_modal", "opened"),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("whitelist_page_add_entry_button", "n_clicks"),
    dash.Input("whitelist_page_search_input", "value"),
    dash.Input("whitelist_page_pagination", "value"),
    dash.Input("whitelist_page_entries_on_page_input", "value"),
    dash.Input(
        {
            "type": "whitelist_page_whitelist_entries_list_item_delete_button",
            "index": dash.ALL,
        },
        "n_clicks",
    ),
    dash.Input("whitelist_page_delete_all_entries_button", "n_clicks"),
    dash.State("whitelist_page_add_entry_initial_input", "value"),
    dash.State("whitelist_page_add_entry_tag_input", "value"),
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
    initial_value,
    tag_value,
    dummy_indexes,
):
    error = False

    new_entries_list = None
    new_pagination_total = None
    new_already_exist_modal_opened = None

    if dash.callback_context.triggered_id == "whitelist_page_entries_on_page_input":
        if db.settings.set_whitelist_entries_on_page(entries_on_page_value)[0]:
            error = True

    if 1 in delete_entry_buttons:
        rowid = dummy_indexes[delete_entry_buttons.index(1)]
        if db.whitelist.delete_whitelist_entry(rowid)[0]:
            error = True

    if dash.callback_context.triggered_id == "whitelist_page_delete_all_entries_button":
        if db.whitelist.delete_all_whitelist_entries()[0]:
            error = True

    if dash.callback_context.triggered_id == "whitelist_page_add_entry_button":
        db_error, is_whitelist_entry_exists = db.whitelist.is_whitelist_entry_exists(
            initial_value.lower()
        )
        if db_error:
            error = True

        elif is_whitelist_entry_exists:
            new_already_exist_modal_opened = True

        elif not is_whitelist_entry_exists:
            if db.whitelist.add_whitelist_entry(
                initial_value.lower(),
                tag_value,
            )[0]:
                error = True

    db_error, result = db.whitelist.whitelist_entries(
        search_input_value,
        pagination_value,
        entries_on_page_value,
    )
    if db_error:
        error = True
    else:
        new_entries_list = whitelist_entries_list(result)

    if len(result) == 0 and pagination_value != 1:
        pagination_value = 1

        db_error, result = db.whitelist.whitelist_entries(
            search_input_value,
            pagination_value,
            entries_on_page_value,
        )
        if db_error:
            error = True
        else:
            new_entries_list = whitelist_entries_list(result)

    db_error, result = db.whitelist.whitelist_pagination_pages(
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


def whitelist_entries_list(data):
    whitelist_entries_list = [
        whitelist_entries_list_item(data[i]) for i in range(len(data))
    ]

    return whitelist_entries_list


def whitelist_entries_list_item(data):
    list_item = dmc.Card(
        children=[
            dmc.Grid(
                [
                    dmc.GridCol(
                        dmc.TextInput(
                            id={
                                "type": "whitelist_page_whitelist_entries_list_item_initial_input",
                                "index": data["rowid"],
                            },
                            value=data["initial"],
                            label="Исходная форма",
                            size="md",
                        ),
                        span="auto",
                    ),
                    dmc.GridCol(
                        dmc.TextInput(
                            id={
                                "type": "whitelist_page_whitelist_entries_list_item_tag_input",
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
                                "type": "whitelist_page_whitelist_entries_list_item_delete_button",
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
    dash.Output("whitelist_page_changes_saved_success_modal", "opened"),
    dash.Output("whitelist_page_changes_saved_failure_modal", "opened"),
    dash.Output(
        "whitelist_page_changes_saved_failure_modal_additional_info", "children"
    ),
    dash.Input("whitelist_page_save_changes_button", "n_clicks"),
    dash.State(
        {
            "type": "whitelist_page_whitelist_entries_list_item_initial_input",
            "index": dash.ALL,
        },
        "value",
    ),
    dash.State(
        {
            "type": "whitelist_page_whitelist_entries_list_item_tag_input",
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
    initial_inputs_values,
    tag_inputs_values,
    dummy_indexes,
):
    error = False

    initial_inputs_values[:] = [a.lower() for a in initial_inputs_values]

    if dash.callback_context.triggered_id == "whitelist_page_save_changes_button":
        if str() in initial_inputs_values:
            additional_info = dmc.Stack(
                [
                    dmc.Text("Изменения не были сохранены"),
                    dmc.Text("Не заполнены все обязательные поля (исходная форма)"),
                ]
            )

            return (
                False,
                True,
                additional_info,
            )

        if len(initial_inputs_values) != len(set(initial_inputs_values)):
            duplicates = [
                item
                for item, count in collections.Counter(initial_inputs_values).items()
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
                initial_inputs_values[i],
                tag_inputs_values[i],
                dummy_indexes[i],
            )
            for i in range(len(initial_inputs_values))
        ]
        if db.whitelist.update_whitelist_entries(data)[0]:
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


def whitelist_page():
    error = False

    db_error, whitelist_form_content = whitelist_form()
    if db_error:
        error = True
        whitelist_form_content = None

    error_modal = dmc.Modal(
        id="whitelist_page_already_exist_modal",
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
        id="whitelist_page_changes_saved_success_modal",
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
        id="whitelist_page_changes_saved_failure_modal",
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
            id="whitelist_page_changes_saved_failure_modal_additional_info",
        ),
        centered=True,
        opened=False,
    )

    whitelist_page = dash.html.Div(
        [
            dash.dcc.Location("whitelist_page_url"),
            error_modal,
            changes_saved_success_modal,
            changes_saved_failure_modal,
            whitelist_form_content,
        ]
    )

    return (
        error,
        whitelist_page,
    )
