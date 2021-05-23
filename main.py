import sys
import handler
import platform
import logging
import log_setup
from pubsub import pub

current_platform = platform.system()
log_setup.setup_logging("launcher.log")

logging.info("Starting main.py")


# From https://stackoverflow.com/a/16993115/8286014
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    pub.sendMessage("quitSysTray")
    sys.exit()


sys.excepthook = handle_exception

if current_platform == "Windows":
    import tray_icon

    tray_icon.start_tray_icon()

download_handler = handler.InstallHandler()
is_up_to_date = download_handler.is_latest_installed

if current_platform == "Linux":
    logging.warning("Linux is currently unsupported. Exiting...")
    sys.exit()

if is_up_to_date:
    logging.info("OpenRCT2 is already up to date")
else:
    download_handler.update_openrct2()

pub.sendMessage("quitSysTray")
sys.exit()
