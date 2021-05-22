import sys

import handler
import tray_icon
from pubsub import pub

tray_icon.start_tray_icon()

download_handler = handler.InstallHandler()
# is_up_to_date = download_handler.is_latest_installed
is_up_to_date = False

if is_up_to_date:
    print("OpenRCT2 is already up to date")
    pub.sendMessage("quitSysTray")
    sys.exit()
else:
    download_handler.update_openrct2()
    pub.sendMessage("quitSysTray")
    sys.exit()
