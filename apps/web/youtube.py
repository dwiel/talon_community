import time
import os

from talon.voice import Context, Key, press
from talon import ctrl, clip, applescript

from . import browser

DOWNLOAD_PATH = "~/Music"


def youtube_download_audio(m):
    youtube_download(video=False)


def youtube_download_video(m):
    youtube_download(video=True)


def youtube_download(video=True):
    press("escape")
    press("cmd-l")
    press("cmd-c")
    time.sleep(0.1)
    url = clip.get()
    print(f"url: {url}")
    press("escape")

    command = f"youtube-dl "
    if not video:
        command += "--extract-audio "
    command += "{url}"
    print(f"command: {command}")

    return applescript.run(
        f"""
        tell application "Terminal"
            do script "cd {os.path.expanduser(DOWNLOAD_PATH)}; {command}; exit"
        end tell
        """
    )


context = Context(
    "youtube", func=browser.url_matches_func("https://youtube.com/.*")
)
context.keymap(
    {
        "download audio": youtube_download_audio,
        "download video": youtube_download_video,
        "speed up": browser.send_to_page(">"),
        "speed down": browser.send_to_page("<"),
        "full screen": browser.send_to_page("f"),
    }
)
