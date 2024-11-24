import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pickle

from config import SCREENSHOT_PATH


class RunOmniparser(FileSystemEventHandler):

    def __init__(self):
        self.result = None
        self.found = False

    def on_created(self, event):
        if not event.is_directory and os.path.basename(event.src_path) == "end.txt":
            try:
                with open(event.src_path, "r") as file:
                    result_path = ""
                    while result_path == "":
                        result_path = file.readline().strip()
                    print(f"Opening result {result_path}")

                    with open(result_path, "rb") as file:
                        data = pickle.load(file)
                    self.result = (
                        data.get("file_path_base_64"),
                        data.get("return_list"),
                        data.get("simplified_return_list"),
                    )
                    self.found = True

                os.remove(event.src_path)
                print("end.txt deleted.")

            except Exception as e:
                print(f"Error processing start.txt: {e}")


def result_watchdog():
    folder_to_watch = SCREENSHOT_PATH

    event_handler = RunOmniparser()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)

    print(f"Watching for end.txt in {folder_to_watch}...")
    observer.start()
    try:
        while not event_handler.found:
            time.sleep(0.05)

        print("Exiting result watchdog")
        observer.stop()
        observer.join()

        return event_handler.result
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
