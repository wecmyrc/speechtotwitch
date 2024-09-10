import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify


import process_message.process_message as process_message
import db.settings


def settings_form():
    error = False

    db_error, capital_letter = db.settings.capital_letter()
    if db_error:
        error = True
        capital_letter = False

    db_error, caps_lock = db.settings.caps_lock()
    if db_error:
        error = True
        caps_lock = False

    db_error, use_dict = db.settings.use_dict()
    if db_error:
        error = True
        use_dict = False

    db_error, use_whitelist = db.settings.use_whitelist()
    if db_error:
        error = True
        use_whitelist = False

    db_error, use_blacklist = db.settings.use_blacklist()
    if db_error:
        error = True
        use_blacklist = False

    db_error, open_browser_on_startup = db.settings.open_browser_on_startup()
    if db_error:
        error = True
        open_browser_on_startup = True

    db_error, dark_theme = db.settings.dark_theme()
    if db_error:
        error = True
        dark_theme = True

    db_error, armed_to_the_teeth = db.settings.armed_to_the_teeth()
    if db_error:
        error = True
        armed_to_the_teeth = False

    test_message = dmc.Stack(
        [
            dmc.Text(
                "Проверить сообщение",
                style={"fontSize": 40},
            ),
            dmc.Textarea(
                id="settings_page_test_message_initial_textarea",
                label="Исходная форма",
                autosize=True,
                minRows=2,
                maxRows=4,
                size="md",
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
                                                "Проверить работу обработки сообщений. Исходная форма - текст сообщения, сказанного в микрофон. Конечная форма - текст который будет отправлен в чат. ",
                                                dmc.Anchor(
                                                    children="Настройки",
                                                    href="/settings",
                                                ),
                                                " влияют на обработку исходной формы",
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
                            id="settings_page_test_message_button",
                            children="Проверить",
                            size="md",
                            fullWidth=True,
                        ),
                        span="auto",
                    ),
                ],
                align="flex-end",
            ),
            dmc.Textarea(
                id="settings_page_test_message_final_textarea",
                label="Конечная форма",
                autosize=True,
                minRows=2,
                maxRows=4,
                size="md",
            ),
        ],
        gap="md",
    )

    message_settings = dmc.Stack(
        [
            dmc.Text(
                "Отправка сообщений",
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
                                                "Первая буква сообщения - заглавная",
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
                        dmc.Switch(
                            id="settings_page_capital_letter_switch",
                            size="md",
                            label="Заглавная буква",
                            checked=capital_letter,
                        ),
                        span="auto",
                    ),
                ],
                align="center",
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
                                                "Все буквы сообщения в верхнем регистре",
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
                        dmc.Switch(
                            id="settings_page_caps_lock_switch",
                            size="md",
                            label="CAPS LOCK",
                            checked=caps_lock,
                        ),
                        span="auto",
                    ),
                ],
                align="center",
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
                                                "Замена слов согласно ",
                                                dmc.Anchor(
                                                    children="словарю",
                                                    href="/dict",
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
                        dmc.Switch(
                            id="settings_page_use_dict_switch",
                            size="md",
                            label="Использовать словарь",
                            checked=use_dict,
                        ),
                        span="auto",
                    ),
                ],
                align="center",
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
                                                "Слова, не указанные в ",
                                                dmc.Anchor(
                                                    children="белом списке",
                                                    href="/whitelist",
                                                ),
                                                ", удаляются из сообщения",
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
                        dmc.Switch(
                            id="settings_page_use_whitelist_switch",
                            size="md",
                            label="Использовать белый список",
                            checked=use_whitelist,
                        ),
                        span="auto",
                    ),
                ],
                align="center",
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
                                                "Слова, указанные в ",
                                                dmc.Anchor(
                                                    children="черном списке",
                                                    href="/blacklist",
                                                ),
                                                ", удаляются из сообщения",
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
                        dmc.Switch(
                            id="settings_page_use_blacklist_switch",
                            size="md",
                            label="Использовать черный список",
                            checked=use_blacklist,
                        ),
                        span="auto",
                    ),
                ],
                align="center",
            ),
        ],
        gap="md",
    )

    interface_settings = dmc.Stack(
        [
            dmc.Text(
                "Интерфейс",
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
                                                "Тема при запуске программы",
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
                        dmc.Switch(
                            id="settings_page_dark_theme_switch",
                            size="md",
                            label="Тёмная тема",
                            checked=dark_theme,
                        ),
                        span="auto",
                    ),
                ],
                align="center",
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
                                                "Автоматически открывается страница программы",
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
                        dmc.Switch(
                            id="settings_page_open_browser_on_startup_switch",
                            size="md",
                            label="Открывать браузер при запуске",
                            checked=open_browser_on_startup,
                        ),
                        span="auto",
                    ),
                ],
                align="center",
            ),
        ],
        gap="md",
    )

    ikwiad_settings = dmc.Stack(
        [
            dmc.Text(
                "Я знаю что делаю",
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
                                                "Сохранение текущего статуса микрофона, отправки сообщений в twitch, а также выбранных пользователя и канала при выключении программы",
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
                        dmc.Switch(
                            id="settings_page_armed_to_the_teeth_switch",
                            size="md",
                            label="Armed to the teeth",
                            checked=armed_to_the_teeth,
                        ),
                        span="auto",
                    ),
                ],
                align="center",
            ),
        ],
        gap="md",
    )

    settings_form = dmc.Stack(
        [
            test_message,
            dmc.Divider(variant="solid", size="xl"),
            message_settings,
            dmc.Divider(variant="solid", size="xl"),
            interface_settings,
            dmc.Divider(variant="solid", size="xl"),
            ikwiad_settings,
        ]
    )

    return (
        error,
        settings_form,
    )


@dash.callback(
    dash.Output("settings_page_test_message_final_textarea", "value"),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("settings_page_test_message_button", "n_clicks"),
    dash.State("settings_page_test_message_initial_textarea", "value"),
    prevent_initial_call=True,
)
def handle_test_message_button(
    test_message_button,
    test_message_initial_textarea_value,
):
    error = False

    patched_test_message_final_textarea_children = dash.Patch()

    if dash.callback_context.triggered_id == "settings_page_test_message_button":
        db_error, settings = db.settings.settings()
        if db_error:
            error = True

        db_error, all_blacklist_entries = db.blacklist.all_blacklist_entries()
        if db_error:
            error = True

        db_error, all_whitelist_entries = db.whitelist.all_whitelist_entries()
        if db_error:
            error = True

        db_error, all_dict_entries = db.dict.all_dict_entries()
        if db_error:
            error = True

        if not error:
            patched_test_message_final_textarea_children = (
                process_message.process_message(
                    message=test_message_initial_textarea_value,
                    settings=settings,
                    blacklist_entries=all_blacklist_entries,
                    whitelist_entries=all_whitelist_entries,
                    dict_entries=all_dict_entries,
                )
            )

    return (
        patched_test_message_final_textarea_children,
        not error,
    )


@dash.callback(
    dash.Output("settings_page_capital_letter_switch", "checked"),
    dash.Output("settings_page_dummy_output", "children"),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("settings_page_capital_letter_switch", "checked"),
    prevent_initial_call=True,
)
def handle_capital_letter_switch(capital_letter_switch_checked):
    error = False

    patched_capital_letter_switch_checked = dash.Patch()

    if dash.callback_context.triggered_id == "settings_page_capital_letter_switch":
        db_error, new_value = db.settings.set_capital_letter(
            capital_letter_switch_checked
        )
        if db_error:
            error = True
        else:
            patched_capital_letter_switch_checked = new_value

    return (
        patched_capital_letter_switch_checked,
        None,
        not error,
    )


@dash.callback(
    dash.Output("settings_page_caps_lock_switch", "checked"),
    dash.Output("settings_page_dummy_output", "children", allow_duplicate=True),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("settings_page_caps_lock_switch", "checked"),
    prevent_initial_call=True,
)
def handle_caps_lock_switch(caps_lock_switch_checked):
    error = False

    patched_caps_lock_switch_checked = dash.Patch()

    if dash.callback_context.triggered_id == "settings_page_caps_lock_switch":
        db_error, new_value = db.settings.set_caps_lock(caps_lock_switch_checked)
        if db_error:
            error = True
        else:
            patched_caps_lock_switch_checked = new_value

    return (
        patched_caps_lock_switch_checked,
        None,
        not error,
    )


@dash.callback(
    dash.Output("settings_page_use_dict_switch", "checked"),
    dash.Output("settings_page_dummy_output", "children", allow_duplicate=True),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("settings_page_use_dict_switch", "checked"),
    prevent_initial_call=True,
)
def handle_use_dict_switch(use_dict_switch_checked):
    error = False

    patched_use_dict_switch_checked = dash.Patch()

    if dash.callback_context.triggered_id == "settings_page_use_dict_switch":
        db_error, new_value = db.settings.set_use_dict(use_dict_switch_checked)
        if db_error:
            error = True
        else:
            patched_use_dict_switch_checked = new_value

    return (
        patched_use_dict_switch_checked,
        None,
        not error,
    )


@dash.callback(
    dash.Output("settings_page_use_whitelist_switch", "checked"),
    dash.Output("settings_page_dummy_output", "children", allow_duplicate=True),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("settings_page_use_whitelist_switch", "checked"),
    prevent_initial_call=True,
)
def handle_use_whitelist_switch(use_whitelist_switch_checked):
    error = False

    patched_use_whitelist_switch_checked = dash.Patch()

    if dash.callback_context.triggered_id == "settings_page_use_whitelist_switch":
        db_error, new_value = db.settings.set_use_whitelist(
            use_whitelist_switch_checked
        )
        if db_error:
            error = True
        else:
            patched_use_whitelist_switch_checked = new_value

    return (
        patched_use_whitelist_switch_checked,
        None,
        not error,
    )


@dash.callback(
    dash.Output("settings_page_use_blacklist_switch", "checked"),
    dash.Output("settings_page_dummy_output", "children", allow_duplicate=True),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("settings_page_use_blacklist_switch", "checked"),
    prevent_initial_call=True,
)
def handle_use_blacklist_switch(use_blacklist_switch_checked):
    error = False

    patched_use_blacklist_switch_checked = dash.Patch()

    if dash.callback_context.triggered_id == "settings_page_use_blacklist_switch":
        db_error, new_value = db.settings.set_use_blacklist(
            use_blacklist_switch_checked
        )
        if db_error:
            error = True
        else:
            patched_use_blacklist_switch_checked = new_value

    return (
        patched_use_blacklist_switch_checked,
        None,
        not error,
    )


@dash.callback(
    dash.Output("settings_page_dark_theme_switch", "checked"),
    dash.Output("settings_page_dummy_output", "children", allow_duplicate=True),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("settings_page_dark_theme_switch", "checked"),
    prevent_initial_call=True,
)
def handle_dark_theme_switch(dark_theme_switch_checked):
    error = False

    patched_dark_theme_switch_checked = dash.Patch()

    if dash.callback_context.triggered_id == "settings_page_dark_theme_switch":
        db_error, new_value = db.settings.set_dark_theme(dark_theme_switch_checked)
        if db_error:
            error = True
        else:
            patched_dark_theme_switch_checked = new_value

    return (
        patched_dark_theme_switch_checked,
        None,
        not error,
    )


@dash.callback(
    dash.Output("settings_page_open_browser_on_startup_switch", "checked"),
    dash.Output("settings_page_dummy_output", "children", allow_duplicate=True),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("settings_page_open_browser_on_startup_switch", "checked"),
    prevent_initial_call=True,
)
def handle_open_browser_on_startup_switch(open_browser_on_startup_switch_checked):
    error = False

    patched_open_browser_on_startup_switch_checked = dash.Patch()

    if (
        dash.callback_context.triggered_id
        == "settings_page_open_browser_on_startup_switch"
    ):
        db_error, new_value = db.settings.set_open_browser_on_startup(
            open_browser_on_startup_switch_checked
        )
        if db_error:
            error = True
        else:
            patched_open_browser_on_startup_switch_checked = new_value

    return (
        patched_open_browser_on_startup_switch_checked,
        None,
        not error,
    )


@dash.callback(
    dash.Output("settings_page_armed_to_the_teeth_switch", "checked"),
    dash.Output("settings_page_dummy_output", "children", allow_duplicate=True),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("settings_page_armed_to_the_teeth_switch", "checked"),
    prevent_initial_call=True,
)
def handle_armed_to_the_teeth_switch(armed_to_the_teeth_switch_checked):
    error = False

    patched_armed_to_the_teeth_switch_checked = dash.Patch()

    if dash.callback_context.triggered_id == "settings_page_armed_to_the_teeth_switch":
        db_error, new_value = db.settings.set_armed_to_the_teeth(
            armed_to_the_teeth_switch_checked
        )
        if db_error:
            error = True
        else:
            patched_armed_to_the_teeth_switch_checked = new_value

    return (
        patched_armed_to_the_teeth_switch_checked,
        None,
        not error,
    )


def settings_page():
    error = False

    db_error, settings_form_content = settings_form()
    if db_error:
        error = True
        settings_form_content = None

    settings_page = dash.html.Div(
        [
            dash.dcc.Location("settings_page_url"),
            dash.html.Div(id="settings_page_dummy_output", style={"display": "none"}),
            settings_form_content,
        ]
    )

    return (
        error,
        settings_page,
    )
