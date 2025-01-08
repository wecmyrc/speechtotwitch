import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify


import db.settings


from wgui.pages.main_page import main_page
from wgui.pages.keys_page import keys_page
from wgui.pages.dict_page import dict_page
from wgui.pages.messages_page import messages_page
from wgui.pages.whitelist_page import whitelist_page
from wgui.pages.blacklist_page import blacklist_page
from wgui.pages.channels_page import channels_page
from wgui.pages.settings_page import settings_page
from wgui.pages.not_found_page import not_found_page


def navbar(location):

    navbar_items_data = [
        {
            "title": "Главная",
            "icon": "bx:bx-home",
            "destination": "/",
        },
        {
            "title": "Сообщения",
            "icon": "bx:bx-message",
            "destination": "/messages",
        },
        {
            "title": "Каналы",
            "icon": "ant-design:twitch-outlined",
            "destination": "/channels",
        },
        {
            "title": "Ключи",
            "icon": "bx:bx-key",
            "destination": "/keys",
        },
        {
            "title": "Словарь",
            "icon": "bx:bx-book",
            "destination": "/dict",
        },
        {
            "title": "Белый список",
            "icon": "bx:bx-check-shield",
            "destination": "/whitelist",
        },
        {
            "title": "Черный список",
            "icon": "bx:bx-shield-x",
            "destination": "/blacklist",
        },
        {
            "title": "Настройки",
            "icon": "bx:bx-cog",
            "destination": "/settings",
        },
    ]

    navbar_items = [
        navbar_item(d["title"], d["icon"], d["destination"], location)
        for d in navbar_items_data
    ]

    navbar = dash.html.Div(navbar_items)

    return navbar


def navbar_item(title, icon, destination, location):
    item = dmc.NavLink(
        label=dmc.Text(title),
        leftSection=DashIconify(
            icon=icon,
            height=20,
        ),
        href=destination,
        active=True if location == destination else False,
    )

    return item


def content(location):
    if location == "/":
        return main_page()
    if location == "/keys":
        return keys_page()
    if location == "/dict":
        return dict_page()
    if location == "/messages":
        return messages_page()
    if location == "/whitelist":
        return whitelist_page()
    if location == "/blacklist":
        return blacklist_page()
    if location == "/channels":
        return channels_page()
    if location == "/settings":
        return settings_page()

    return not_found_page(location)


@dash.callback(
    dash.Output("mantine_provider", "forceColorScheme"),
    dash.Input("base_page_theme_switch_action", "n_clicks"),
    dash.State("mantine_provider", "forceColorScheme"),
    prevent_initial_call=True,
)
def change_theme(
    n_clicks,
    theme,
):
    error = False

    patched_mantine_provider_theme = dash.Patch()

    if n_clicks != None:
        patched_mantine_provider_theme = "dark" if theme == "light" else "light"

    return patched_mantine_provider_theme


@dash.callback(
    dash.Output("base_page_toggle_mic_button", "color"),
    dash.Output("base_page_toggle_mic_button_icon", "icon"),
    dash.Output("base_page_error_alert", "hide"),
    dash.Input("base_page_toggle_mic_button", "n_clicks"),
    prevent_initial_call=True,
)
def handle_toggle_mic_button(toggle_mic_button):
    error = False

    patched_toggle_mic_button_color = dash.Patch()
    patched_toggle_mic_button_icon = dash.Patch()
    patched_error_alert_hide = dash.Patch()

    if dash.callback_context.triggered_id == "base_page_toggle_mic_button":
        db_error, new_value = db.settings.toggle_mic()
        if db_error:
            error = True
            new_value = None

        if new_value != None:
            patched_toggle_mic_button_color = "green" if new_value else "red"
            patched_toggle_mic_button_icon = (
                "bx:microphone" if new_value else "bx:microphone-off"
            )

        patched_error_alert_hide = not error

    return (
        patched_toggle_mic_button_color,
        patched_toggle_mic_button_icon,
        patched_error_alert_hide,
    )


@dash.callback(
    dash.Output("base_page_toggle_twitch_button", "color"),
    dash.Output("base_page_error_alert", "hide", allow_duplicate=True),
    dash.Input("base_page_toggle_twitch_button", "n_clicks"),
    prevent_initial_call=True,
)
def handle_toggle_twitch_button(toggle_twitch_button):
    error = False

    patched_toggle_twitch_button_color = dash.Patch()
    patched_error_alert_hide = dash.Patch()

    if dash.callback_context.triggered_id == "base_page_toggle_twitch_button":
        db_error, new_value = db.settings.toggle_twitch()
        if db_error:
            error = True
            new_value = None

        if new_value != None:
            patched_toggle_twitch_button_color = "green" if new_value else "red"

        patched_error_alert_hide = not error

    return (
        patched_toggle_twitch_button_color,
        patched_error_alert_hide,
    )


def base_page(location):
    error = False

    db_error, result = db.settings.mic_on()
    toggle_mic_button_color = "green" if result else "red"
    toggle_mic_button_icon = "bx:microphone" if result else "bx:microphone-off"
    if db_error:
        error = True
        toggle_mic_button_color = "red"
        toggle_mic_button_icon = "bx:microphone-off"

    db_error, result = db.settings.twitch_on()
    toggle_twitch_button_color = "green" if result else "red"
    if db_error:
        error = True
        toggle_twitch_button_color = "red"

    db_error, current_username_in_use = db.settings.username_in_use()
    if db_error:
        error = True
        current_username_in_use = None

    db_error, current_channel_in_use = db.settings.channel_in_use()
    if db_error:
        error = True
        current_channel_in_use = None

    if current_username_in_use and current_channel_in_use:
        toggle_twitch_button_disabled = False
    else:
        toggle_twitch_button_disabled = True

    controls = dmc.Stack(
        children=dmc.Grid(
            [
                dmc.GridCol(
                    dmc.Anchor(
                        children=dmc.Group(
                            [
                                DashIconify(
                                    icon="mdi:github",
                                    width=32,
                                ),
                                dmc.Text("speechtotwitch", size="xl"),
                            ],
                            justify="center",
                        ),
                        href="https://github.com/wecmyrc/speechtotwitch",
                        underline=False,
                        variant="text",
                        mb=5,
                    ),
                    span="content",
                ),
                dmc.GridCol(
                    dmc.Group(
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
                                                                "Распознавание речи",
                                                            ],
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            withArrow=True,
                                            zIndex=12000,
                                        ),
                                        span="content",
                                        mb=-4,  # NOTE rewrite in future
                                    ),
                                    dmc.GridCol(
                                        dmc.Button(
                                            id="base_page_toggle_mic_button",
                                            children=dmc.Title(
                                                "Микрофон",
                                                order=5,
                                            ),
                                            leftSection=dmc.ThemeIcon(
                                                children=DashIconify(
                                                    id="base_page_toggle_mic_button_icon",
                                                    icon=toggle_mic_button_icon,
                                                    width=32,
                                                    color="white",
                                                ),
                                                variant="transparent",
                                            ),
                                            color=toggle_mic_button_color,
                                            w=500,
                                        ),
                                        span="content",
                                    ),
                                ],
                                align="flex-end",
                            ),
                            dmc.Grid(
                                [
                                    dmc.GridCol(
                                        dmc.Button(
                                            id="base_page_toggle_twitch_button",
                                            children=dmc.Title(
                                                "Twitch",
                                                order=5,
                                            ),
                                            leftSection=dmc.ThemeIcon(
                                                children=DashIconify(
                                                    icon="ant-design:twitch-outlined",
                                                    width=32,
                                                    color="white",
                                                ),
                                                variant="transparent",
                                            ),
                                            color=toggle_twitch_button_color,
                                            disabled=toggle_twitch_button_disabled,
                                            w=500,
                                        ),
                                        span="content",
                                    ),
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
                                                                "Отправка сообщений в чат twitch. Если выключено, то сообщения будут сохранятся без отправки",
                                                            ],
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            withArrow=True,
                                            zIndex=12000,
                                        ),
                                        span="content",
                                        mb=-4,  # NOTE rewrite in future
                                    ),
                                ],
                            ),
                        ],
                        gap="xl",
                    ),
                    span="content",
                ),
                dmc.GridCol(
                    dmc.ActionIcon(
                        id="base_page_theme_switch_action",
                        children=DashIconify(
                            id="theme_switch_icon",
                            icon="mdi:theme-light-dark",
                            width=32,
                        ),
                        size="xl",
                        variant="transparent",
                    ),
                    span="content",
                ),
            ],
            justify="space-between",
            align="center",
        ),
        justify="center",
        h=69,
    )

    db_error, main_content = content(location)
    if db_error:
        error = True
        main_content = None

    error_alert = dmc.Alert(
        id="base_page_error_alert",
        title=dmc.Group(
            [
                dmc.ThemeIcon(
                    children=DashIconify(
                        icon="bx:error",
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
        children="Что-то пошло не так. Проверь логи.",
        color="red",
        variant="light",
        hide=not error,
        withCloseButton=True,
    )

    base_page = dmc.AppShell(
        [
            dash.html.Div(id="app_shell_dummy_output", style={"display": "none"}),
            dmc.AppShellHeader(controls, px=50),
            dmc.AppShellNavbar(children=navbar(location)),
            dmc.AppShellMain(children=main_content),
            dmc.AppShellFooter(
                children=error_alert,
                zIndex=10000,
            ),
        ],
        header={
            "height": 70,
        },
        padding="xl",
        zIndex=9000,
        navbar={
            "width": 185,
            "breakpoint": "sm",
            "collapsed": {"mobile": True},
        },
        footer={
            "heigh": 100,
        },
    )

    return base_page
