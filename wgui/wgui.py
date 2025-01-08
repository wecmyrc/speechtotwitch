import os
import sys
import logging
import flask
import dash

dash._dash_renderer._set_react_version("18.2.0")

from wgui.apps import create_flask_app, create_dash_app

from wgui.pages.base_page import base_page


import traceback
from base_logger.base_logger import logger


@dash.callback(
    dash.Output("page_content", "children"),
    dash.Input("url", "pathname"),
)
def render_page(location):
    return base_page(location)


# NOTE for gunicorn start
# def start():
#     sys.excepthook = exc_handler
#     flask_app = create_flask_app()
#     dash_app = create_dash_app(flask_app)
#     dash_app.title = "stt"

#     return flask_app


def main():
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    flask_app = create_flask_app()
    dash_app = create_dash_app(flask_app)
    dash_app.title = "stt"
    dash_app.run(debug=False)  # NOTE with True crashes


if __name__ == "__main__":
    main()
