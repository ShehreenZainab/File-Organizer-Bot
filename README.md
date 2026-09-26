# 📂 File Organizer Bot

A lightweight Python automation script that watches a folder (like `Downloads`) and instantly sorts new files into category subfolders — Images, Documents, Spreadsheets, Code, and more — based on file extension. No more digging through a Downloads folder full of unsorted files.

## Why I built this

I kept losing track of downloaded files scattered across one folder — screenshots next to spreadsheets next to random installers. Instead of manually organizing it every week, I automated it. It felt like a natural next step after building database-heavy desktop apps (POS System, Laundry Management System) — I wanted to write something that runs in the background and interacts directly with the operating system.

## Features

- **Real-time watching** — uses `watchdog` to detect new files the moment they appear, no polling.
- **Config-driven** — customize which extensions go to which folder by editing `config.json`, no code changes needed.
- **Dry-run mode** — preview exactly what would be moved before it touches a single file.
- **Duplicate-safe** — if a file with the same name already exists at the destination, a timestamp is appended instead of silently overwriting it.
- **Sort-existing mode** — run once on a folder that's already a mess, instead of only watching for new files.
- **Safe fallback** — unrecognized file types are moved to an "Other" folder instead of crashing the program.
- **Cross-platform** — built with `pathlib`, works on Windows, macOS, and Linux.

## Tech Stack

- Python 3
- [`watchdog`](https://pypi.org/project/watchdog/) — filesystem event monitoring
- Standard library: `shutil`, `pathlib`, `json`, `argparse`

## Setup

```bash
git clone https://github.com/ShehreenZainab/File-Organizer-Bot.git
cd File-Organizer-Bot
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Edit `config.json` to set your watch folder and category rules:

```json
{
  "watch_folder": "~/Downloads",
  "categories": {
    "Images": [".jpg", ".png"],
    "Documents": [".pdf", ".docx"],
    "Code": [".py", ".js"]
  }
}
```

Add or edit extensions and categories freely — no code changes required.

## Usage

**Preview what would happen to your existing files, without moving anything:**

```bash
python3 organizer.py --dry-run --sort-existing
```

**Organize files that already exist in the folder (one-time pass):**

```bash
python3 organizer.py --sort-existing
```

**Watch the folder live, organizing new files as they appear:**

```bash
python3 organizer.py
```

Stop the live watcher anytime with `Ctrl+C`.

## Project Structure

```
File-Organizer-Bot/
├── organizer.py        # main script
├── config.json          # customizable extension → folder rules
├── requirements.txt
├── .gitignore
└── README.md
```

## Possible Future Improvements

- [ ] System tray icon with start/stop toggle
- [ ] Undo command to reverse the last N moves
- [ ] Desktop notification when files are organized
- [ ] Recursive subfolder watching

## Author

**Shehreen Zainab** — IT undergraduate, University of Management and Technology, Lahore
[GitHub](https://github.com/ShehreenZainab)
