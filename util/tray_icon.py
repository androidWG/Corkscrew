import logging
import os
from infi.systray import SysTrayIcon
from pubsub import pub

import util


def on_quit_callback(_systray):
    os._exit(1)


def update_systray_hover_text_listener(text):
    systray.update(hover_text=text)


def quit_tray_icon_listener():
    logging.info("Removing tray icon...")
    systray.shutdown()


def start_tray_icon():
    global systray

    tray_icon = util.resource_path("../resources/icon.ico")

    systray = SysTrayIcon(tray_icon, "Corkscrew", on_quit=on_quit_callback)
    systray.start()

    pub.subscribe(update_systray_hover_text_listener, "updateSysTray")
    pub.subscribe(quit_tray_icon_listener, "quitSysTray")