from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import presskey as pk

class KeyThread(QThread):
    thread_signal = pyqtSignal(str)
    def run(self):
        pk.run(self.thread_signal)

def set_icon(text):
    if text == "on":
        tray.setIcon(QIcon("resources/active.png"))
    else:
        tray.setIcon(QIcon("resources/inactive.png"))

def show_message(text):
    if text == "on":
        tray.showMessage("KeyTray", pk.msg_on, QIcon("resources/active.png"), msecs=1000)
    else:
        tray.showMessage("KeyTray", pk.msg_off, QIcon("resources/inactive.png"), msecs=1000)

app = QApplication(sys.argv)

# Create the icon
icon = QIcon("resources/unknown.png")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Create the menu
menu = QMenu()
exit_action = QAction("Exit")
exit_action.triggered.connect(app.exit)
menu.addAction(exit_action)

# Add the menu to the tray
tray.setContextMenu(menu)

# Create the thread
enginethread = KeyThread()
enginethread.thread_signal.connect(set_icon)
enginethread.thread_signal.connect(show_message)
enginethread.start()

sys.exit(app.exec_())