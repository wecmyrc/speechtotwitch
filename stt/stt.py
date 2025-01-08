import sys
import subprocess as sp
import atexit
import webbrowser
import time

from base_logger.base_logger import logger, error_notification
import db.init
import db.settings


def cleanup(pl):
    for p in pl:
        p.terminate()


def main():
    db_error, file = db.init.init_db()
    if db_error:
        try:
            os.remove(file)

        except Exception as e:
            error = "".join(traceback.format_exc())
            logger.critical(error, stack_info=True)
            print(error)

        finally:
            sys.exit(1)

    db_error = db.settings.restore_settings()[0]
    if db_error:
        print("Database error. Check logs")
        error_notification()

    db_error, open_browser_on_startup = db.settings.open_browser_on_startup()
    if db_error:
        print("Database error. Check logs")
        error_notification()
        open_browser_on_startup = True

    if open_browser_on_startup:
        webbrowser.open("http://127.0.0.1:8050/", new=0, autoraise=True)

    pl = list()

    if sys.platform == "win32":
        pl.append(sp.Popen(["poetry", "run", "wgui"]))
        time.sleep(0.2)  # NOTE sleep for clean init print
        pl.append(sp.Popen(["poetry", "run", "voice"]))

    elif sys.platform.startswith("linux"):
        pl.append(sp.Popen(["wgui"]))
        time.sleep(0.2)  # NOTE sleep for clean init print
        pl.append(sp.Popen(["voice"]))

    print("\nPress Ctrl-C to close\n")

    atexit.register(cleanup, pl)

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
