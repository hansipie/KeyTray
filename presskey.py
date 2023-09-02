import ctypes
from plyer import notification
from pynput import keyboard
from PyQt5.QtCore import pyqtSignal

lock = False
keysignal = pyqtSignal(str)

def show_message():
    if lock:
        message = "Num Lock est activé."
        keysignal.emit("active")
    else:
        message = "Num Lock est désactivé."
        keysignal.emit("inactive")
    print(message)

    notification.notify(
        title='KeyTray',
        message=message,
        app_name='KeyTray',
        timeout=0.5  # displays for 0.5 seconds
    )

def check_numlock():
    hllDll = ctypes.WinDLL ("User32.dll")
    VK_NUMLOCK = 0x90
    return hllDll.GetKeyState(VK_NUMLOCK)

def on_press(key):
    global lock  # Declare 'lock' as global variable
    try:
        if key == keyboard.Key.num_lock:
            print('Num Lock Key Pressed')
            lock = not lock
            show_message()
    except AttributeError:
        pass

def run(thread_signal):
    global lock
    lock = check_numlock()
    global keysignal
    keysignal = thread_signal
    show_message()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    run()