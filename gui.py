import tkinter as tk
from tkinter import ttk
import datetime

class PrintMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Print Job Monitor")
        self.root.geometry("800x400")

        # Create the main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create the Treeview for the job list
        self.tree = ttk.Treeview(main_frame, columns=("ID", "Document", "User", "Printer", "Status", "Pages", "Submitted"), show="headings")

        # Define headings
        self.tree.heading("ID", text="Job ID")
        self.tree.heading("Document", text="Document Name")
        self.tree.heading("User", text="User")
        self.tree.heading("Printer", text="Printer")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Pages", text="Pages")
        self.tree.heading("Submitted", text="Time Submitted")

        # Configure column widths
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Document", width=250)
        self.tree.column("User", width=100)
        self.tree.column("Printer", width=150)
        self.tree.column("Status", width=80, anchor=tk.CENTER)
        self.tree.column("Pages", width=50, anchor=tk.CENTER)
        self.tree.column("Submitted", width=120, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Status Bar
        self.status_bar = ttk.Label(self.root, text="Starting...", anchor=tk.W, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_jobs_list(self, jobs):
        """
        Clears the current list and displays the new list of jobs.
        """
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add new jobs
        for job in jobs:
            pages_str = f"{job.get('pages_printed', 'N/A')} / {job.get('total_pages', 'N/A')}"
            self.tree.insert("", tk.END, values=(
                job.get('job_id', ''),
                job.get('document_name', ''),
                job.get('user_name', ''),
                job.get('printer_name', ''),
                job.get('status', ''),
                pages_str,
                job.get('time_submitted', '')
            ))

        # Update status bar
        self.status_bar.config(text=f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def start(self):
        """
        Starts the Tkinter main loop.
        """
        self.root.mainloop()

if __name__ == '__main__':
    # This allows you to run the GUI by itself for testing purposes
    root = tk.Tk()
    app = PrintMonitorGUI(root)

    # Example mock data
    mock_jobs = [
        {
            "job_id": 1, "document_name": "Test_Document_1.docx", "user_name": "user1",
            "printer_name": "HP LaserJet", "status": "Printing", "total_pages": 5,
            "pages_printed": 2, "time_submitted": "2025-10-28 10:30:00"
        },
        {
            "job_id": 2, "document_name": "Another_Report.pdf", "user_name": "user2",
            "printer_name": "Canon Inkjet", "status": "Queued", "total_pages": 10,
            "pages_printed": 0, "time_submitted": "2025-10-28 10:32:15"
        }
    ]

    # Schedule the first update
    root.after(1000, lambda: app.update_jobs_list(mock_jobs))

    app.start()
