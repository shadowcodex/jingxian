# file_watcher.py
import time, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RebuildEventHandler(FileSystemEventHandler):
    """Triggers a site rebuild on any file change."""
    def __init__(self, rebuild_func):
        self.rebuild = rebuild_func
    def on_any_event(self, event):
        # Ignore directory events and the output folder to prevent feedback loops
        if event.is_directory:
            return
        if "output" in event.src_path:
            return
        # Trigger rebuild (you might add debouncing here)
        print(f"Change detected: {event.src_path} -> rebuilding site")
        self.rebuild()

def watch_paths(paths, rebuild_func):
    """Watch given paths for changes and call rebuild_func on change."""
    event_handler = RebuildEventHandler(rebuild_func)
    observer = Observer()
    for p in paths:
        observer.schedule(event_handler, p, recursive=True)
    observer.start()
    try:
        # Keep the watcher running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
