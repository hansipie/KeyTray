import threading
import trayicon as tray
import presskey as pk
import sys

# Create threads
t1 = threading.Thread(target=tray.main)
t2 = threading.Thread(target=pk.run)

# Start threads
t1.start()
t2.start()

# Wait for both threads to finish
t1.join()
t2.join()

print("Both threads are done.")
