import os
import sys
import pathlib
import notifypy
import logging
import logging.config

# from gunicorn import glogging


def error_notification():
    notifypy.Notify(
        default_notification_title="stt",
        default_notification_message="Что-то пошло не так. Проверь логи",
    ).send(block=False)


def log_file():
    log_path = str()
    log_file = str()

    try:
        if sys.platform == "win32":
            if getattr(sys, "frozen", False):
                log_path = os.path.dirname(sys.executable)
            else:
                log_path = os.path.dirname(__file__)

            log_file = os.path.join(log_path, "stt.log")

        elif sys.platform.startswith("linux"):
            log_path = str(pathlib.Path.home()) + "/.stt"
            pathlib.Path(log_path).mkdir(mode=0o777, parents=True, exist_ok=True)
            log_file = log_path + "/stt.log"

    except Exception as e:
        print(e)

    return log_file


# NOTE for gunicorn usage in future
# for gunicorn logging config https://stackoverflow.com/questions/41087790/how-to-override-gunicorns-logging-config-to-use-a-custom-formatter
# class MyLogger(glogging.Logger):
#     def setup(self, cfg):
#         logging.config.dictConfig(logging_config)


logging_config = {  # https://stackoverflow.com/questions/7507825/where-is-a-complete-example-of-logging-config-dictconfig
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
            "datefmt": "%d.%m.%Y %H:%M:%S %Z",
        },
    },
    "handlers": {
        "default": {
            "level": "ERROR",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_file(),
            "mode": "a",
            "maxBytes": 1048576,
            "backupCount": 2,
        },
    },
    "loggers": {
        "": {  # root logger
            "level": "NOTSET",
            "handlers": [
                "default",
            ],
        },
        "my.package": {
            "level": "WARNING",
            "propagate": False,
            "handlers": [
                "default",
            ],
        },
    },
}

logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)
