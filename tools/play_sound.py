import threading
from playsound import playsound


def play_mp3_in_background(file_path):
    """
    Play the specified MP3 file in a separate thread.

    :param file_path: Path to the MP3 file
    """

    def play():
        try:
            playsound(file_path)
        except Exception as e:
            print(f"Error while playing sound: {e}")

    thread = threading.Thread(target=play)
    # Set the thread as a daemon. This ensures the thread will exit when the main program exits.
    thread.daemon = True
    thread.start()

    return thread


def play_mp3_blocking(file_path):

    playsound(file_path)
