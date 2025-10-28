import time
import win32print
import datetime

class PrintMonitor:
    def __init__(self):
        self.jobs = {}

    def get_print_jobs(self):
        """
        Gets all current print jobs and returns them as a list of dictionaries.
        """
        all_jobs = []
        try:
            for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
                flags, desc, name, comment = p
                phandle = win32print.OpenPrinter(name)
                print_jobs = win32print.EnumJobs(phandle, 0, -1, 2)
                if print_jobs:
                    for job in print_jobs:
                        job_info = {
                            "printer_name": name,
                            "job_id": job["JobId"],
                            "document_name": job["pDocument"],
                            "user_name": job["pUserName"],
                            "status": job["Status"],
                            "total_pages": job["TotalPages"],
                            "pages_printed": job["PagesPrinted"],
                            "time_submitted": job["Submitted"].strftime("%Y-%m-%d %H:%M:%S")
                        }
                        all_jobs.append(job_info)
                win32print.ClosePrinter(phandle)
        except Exception as e:
            # This will likely fail in a non-Windows environment.
            # In a real Windows environment, you'd want more robust error handling.
            print(f"Error communicating with print queue (this is expected on non-Windows): {e}")
            # Return some mock data for development purposes
            return [{
                "printer_name": "Mock Printer",
                "job_id": 1,
                "document_name": "Test Document.pdf",
                "user_name": "Jules",
                "status": "Printing",
                "total_pages": 1,
                "pages_printed": 0,
                "time_submitted": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }]

        return all_jobs

    def start_monitoring(self, callback):
        """
        Starts an infinite loop to monitor the print queue.
        Calls the callback function with the list of jobs whenever it changes.
        """
        print("Starting print monitor...")
        last_jobs = []
        while True:
            current_jobs = self.get_print_jobs()
            if current_jobs != last_jobs:
                print(f"Detected change in print queue. Jobs: {len(current_jobs)}")
                callback(current_jobs)
                last_jobs = current_jobs
            time.sleep(2) # Check every 2 seconds

if __name__ == '__main__':
    # This is an example of how to use the monitor
    def display_jobs(jobs):
        print("--- Current Print Jobs ---")
        if not jobs:
            print("No print jobs.")
        for job in jobs:
            print(f"  ID: {job['job_id']}, Document: {job['document_name']}, Status: {job['status']}")
        print("--------------------------\n")

    monitor = PrintMonitor()
    try:
        monitor.start_monitoring(display_jobs)
    except KeyboardInterrupt:
        print("Stopping print monitor.")
