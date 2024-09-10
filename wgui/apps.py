import flask
import dash
import dash_mantine_components as dmc


import db.settings


def create_flask_app():
    flask_app = flask.Flask(__name__)

    return flask_app


def create_dash_app(flask_app):
    stylesheets = [
        "https://unpkg.com/@mantine/dates@7/styles.css",
        "https://unpkg.com/@mantine/code-highlight@7/styles.css",
        "https://unpkg.com/@mantine/charts@7/styles.css",
        "https://unpkg.com/@mantine/carousel@7/styles.css",
        "https://unpkg.com/@mantine/notifications@7/styles.css",
        "https://unpkg.com/@mantine/nprogress@7/styles.css",
    ]

    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        suppress_callback_exceptions=True,  # [note] check this
        external_stylesheets=stylesheets,
    )

    db_error, dark_theme = db.settings.dark_theme()
    if db_error:
        dark_theme = True

    dash_app.layout = dmc.MantineProvider(
        id="mantine_provider",
        children=dash.html.Div(
            [
                dash.dcc.Location("url"),
                dash.html.Div(id="page_content"),
                dash.page_container,
            ]
        ),
        forceColorScheme="dark" if dark_theme else "light",
        theme={
            "fontFamily": "'Helvetica', sans-serif",
        },
    )

    return dash_app
