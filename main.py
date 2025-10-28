import tkinter as tk
import threading
from gui import PrintMonitorGUI
from print_monitor import PrintMonitor

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.gui = PrintMonitorGUI(root)
        self.monitor = PrintMonitor()

        # Start the monitoring in a separate thread
        self.monitor_thread = threading.Thread(target=self.start_monitoring, daemon=True)
        self.monitor_thread.start()

    def start_monitoring(self):
        """
        Wrapper function to start the monitor and pass the GUI's update method as a callback.
        """
        self.monitor.start_monitoring(self.update_gui)

    def update_gui(self, jobs):
        """
        Thread-safe method to schedule a GUI update on the main thread.
        """
        self.root.after(0, self.gui.update_jobs_list, jobs)

    def start(self):
        """
        Start the Tkinter main loop.
        """
        self.gui.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    app.start()
