import time

from talon.voice import Context, Key, press
from talon import ctrl, clip, applescript


def youtube_download_audio(m):
    youtube_download(video=False)

def youtube_download_video(m):
    youtube_download(video=True)

def youtube_download(video=True):
    press('escape')
    press('cmd-l')
    press('cmd-c')
    time.sleep(0.1)
    url = clip.get()
    print(f'url: {url}')
    press('escape')

    command = f'youtube-dl '
    if not video:
        command += '--extract-audio '
    command += '{url}'
    print(f'command: {command}')

    return applescript.run(
        f"""
        tell application "Terminal"
            do script "cd /Users/zdwiel/Music; {command}; exit"
        end tell
        """
    )


title = ' - YouTube'
context = Context('youtube', func=lambda app, win: title in win.title)
context.keymap({
    'download audio': youtube_download_audio,
    'download video': youtube_download_video,
})
