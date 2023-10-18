import sys
import ctypes
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
from pynput import keyboard

################### Key Monitoring ###################

numlock_status = False
keysignal = pyqtSignal(str)
msg_on = "Num Lock is ON."
msg_off = "Num Lock is OFF."

def emit_message():
    if numlock_status:
        print(msg_on)
        keysignal.emit("on")
    else:
        print(msg_off)
        keysignal.emit("off")

def check_numlock():
    hllDll = ctypes.WinDLL ("User32.dll")
    VK_NUMLOCK = 0x90
    return hllDll.GetKeyState(VK_NUMLOCK)

def on_press(key):
    global numlock_status  # Declare 'lock' as global variable
    try:
        if key == keyboard.Key.num_lock:
            print('Num Lock Key Pressed')
            numlock_status = not numlock_status
            emit_message()
    except AttributeError:
        pass

def runkeymon(thread_signal):
    global numlock_status
    numlock_status = check_numlock()
    global keysignal
    keysignal = thread_signal
    emit_message()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

################### Key Thread ###################

class KeyThread(QThread):
    thread_signal = pyqtSignal(str)
    def run(self):
        runkeymon(self.thread_signal)

###################################################

def set_icon(text):
    if text == "on":
        tray.setIcon(QIcon("resources/active.png"))
    else:
        tray.setIcon(QIcon("resources/inactive.png"))

def show_message(text):
    if text == "on":
        tray.showMessage("KeyTray", msg_on, QIcon("resources/active.png"), msecs=500)
    else:
        tray.showMessage("KeyTray", msg_off, QIcon("resources/inactive.png"), msecs=500)


app = QApplication(sys.argv)

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(QIcon("resources/active.png"))
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