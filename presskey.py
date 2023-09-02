import ctypes
from pynput import keyboard
from PyQt5.QtCore import pyqtSignal

numlock_status = False
keysignal = pyqtSignal(str)
msg_on = "Num Lock on."
msg_off = "Num Lock off."

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

def run(thread_signal):
    global numlock_status
    numlock_status = check_numlock()
    global keysignal
    keysignal = thread_signal
    emit_message()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
