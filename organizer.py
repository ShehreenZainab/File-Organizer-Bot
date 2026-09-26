"""
File Organizer Bot
-------------------
Watches a folder (e.g. Downloads) and automatically sorts new files into
category subfolders based on their extension, using rules from config.json.

Usage:
    python3 organizer.py                 # run normally, watch for new files
    python3 organizer.py --dry-run       # show what WOULD happen, moves nothing
    python3 organizer.py --sort-existing # organize files already in the folder

Author: Shehreen Zainab
"""

import argparse
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        sys.exit(1)
    with open(config_path, "r") as f:
        return json.load(f)


def get_category(extension: str, categories: dict) -> str:
    extension = extension.lower()
    for category, extensions in categories.items():
        if extension in extensions:
            return category
    return "Other"


def unique_destination(dest_folder: Path, filename: str) -> Path:
    dest_path = dest_folder / filename
    if not dest_path.exists():
        return dest_path
    stem = dest_path.stem
    suffix = dest_path.suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return dest_folder / f"{stem}_{timestamp}{suffix}"


def organize_file(file_path: Path, watch_folder: Path, categories: dict, dry_run: bool):
    if not file_path.exists():
        return

    extension = file_path.suffix.lower()
    category = get_category(extension, categories)
    dest_folder = watch_folder / category
    dest_path = unique_destination(dest_folder, file_path.name)

    if dry_run:
        print(f"[DRY RUN] Would move: {file_path.name} -> {category}/{dest_path.name}")
        return

    dest_folder.mkdir(exist_ok=True)
    shutil.move(str(file_path), str(dest_path))
    print(f"Moved: {file_path.name} -> {category}/{dest_path.name}")


class OrganizerHandler(FileSystemEventHandler):
    def __init__(self, watch_folder: Path, categories: dict, dry_run: bool):
        self.watch_folder = watch_folder
        self.categories = categories
        self.dry_run = dry_run

    def on_created(self, event):
        if event.is_directory:
            return
        time.sleep(1)  # let large downloads finish writing
        organize_file(Path(event.src_path), self.watch_folder, self.categories, self.dry_run)


def sort_existing_files(watch_folder: Path, categories: dict, dry_run: bool):
    for item in watch_folder.iterdir():
        if item.is_file():
            organize_file(item, watch_folder, categories, dry_run)


def main():
    parser = argparse.ArgumentParser(description="Automatically organize files by extension.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving files")
    parser.add_argument("--sort-existing", action="store_true", help="Organize existing files, then exit")
    args = parser.parse_args()

    config = load_config(Path("config.json"))
    watch_folder = Path(config["watch_folder"]).expanduser()

    if not watch_folder.exists():
        print(f"Watch folder does not exist: {watch_folder}")
        sys.exit(1)

    mode = "DRY RUN" if args.dry_run else "LIVE"
    print(f"File Organizer Bot started in {mode} mode. Watching: {watch_folder}")

    if args.sort_existing:
        sort_existing_files(watch_folder, config["categories"], args.dry_run)
        print("Finished sorting existing files.")
        return

    handler = OrganizerHandler(watch_folder, config["categories"], args.dry_run)
    observer = Observer()
    observer.schedule(handler, str(watch_folder), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nFile Organizer Bot stopped.")
    observer.join()


if __name__ == "__main__":
    main()