import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pickle

from config import SCREENSHOT_PATH
from modules.brain.ms_omniparser.omniparser import get_screenshot_with_bounding_box


class RunOmniparser(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and os.path.basename(event.src_path) == "start.txt":

            with open(event.src_path, "r") as file:
                screenshot_path = ""
                while screenshot_path == "":
                    screenshot_path = file.readline().strip()
                print(f"processing screenshot {screenshot_path}")
                file_path_base_64, return_list, simplified_return_list = (
                    get_screenshot_with_bounding_box(screenshot_path)
                )
                data = {
                    "file_path_base_64": file_path_base_64,
                    "return_list": return_list,
                    "simplified_return_list": simplified_return_list,
                }
                extension = screenshot_path.split(".")[1]
                file_name = screenshot_path.split(".")[0]
                pickle_file_path = file_name + "_pkl.pkl"
                with open(pickle_file_path, "wb") as file:
                    pickle.dump(data, file)
                with open(SCREENSHOT_PATH + "/end.txt", "w") as file:
                    file.write(pickle_file_path)

            os.remove(event.src_path)
            print("start.txt deleted.")


if __name__ == "__main__":
    folder_to_watch = SCREENSHOT_PATH

    event_handler = RunOmniparser()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)

    try:
        print(f"Watching for start.txt in {folder_to_watch}...")
        observer.start()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
