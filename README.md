# Music Player

A desktop music player built with Python and Tkinter.

It plays local audio files with play, pause, stop, forward, and back controls, a seek slider, a volume slider, and an elapsed-time status bar.

## Running

```bash
pip install -r requirements.txt
python player.py /path/to/your/music
```

You can also set the `MUSIC_DIR` environment variable, or pick the folder in the dialog at startup. (The folder used to be hardcoded to `C:/Music`.)

## What it does

From the code (the GUI needs a display, so this walkthrough is from reading the source, not a live run):

- On startup it lists every file in the music folder in the playlist box.
- Play loads the selected track with pygame and starts a per-second timer that updates the seek slider and the "Time Elapsed" status bar, reading the track length with mutagen. When a track ends it advances to the next one.
- The slider seeks within the track; the vertical slider controls volume.
- Next/previous wrap around at the ends of the playlist.
