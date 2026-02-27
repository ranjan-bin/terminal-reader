# tty-reader

**Read books in your terminal. Look like you're working.**

`tty-reader` opens PDFs, EPUBs, DOCX files, and plain text right in your terminal. It can disguise whatever you're reading as source code or server logs, so it blends in perfectly with everything else on your screen.

Built with [Textual](https://textual.textualize.io/) and [Rich](https://rich.readthedocs.io/).

---

## Features

- **Interactive File Picker:** Visually navigate your computer and select any supported file.
- **Stealth Modes:** Instantly wrap text in Python code or fake server logs.
- **Boss Key:** One keystroke (`Ctrl+B`) instantly hides your book behind a fake system monitor.
- **Auto-Bookmarks:** Close the app anytime. Pick up exactly where you left off.
- **Wide Format Support:** Works cleanly with `.pdf`, `.epub`, `.docx`, `.txt`, and `.md`.

---

## Installation

The recommended way to install Python CLI applications globally is using `pipx`. This avoids system package conflicts.

```bash
git clone https://github.com/yourusername/tty-reader.git
cd tty-reader
pipx install .
```

*Alternatively*, if you don't have `pipx`, you can install it in an isolated virtual environment:

```bash
git clone https://github.com/yourusername/tty-reader.git
cd tty-reader
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## Usage

Run it without any arguments to open the interactive file picker:

```bash
tty-reader
```

Or pass a file directly:

```bash
tty-reader book.epub
tty-reader book.pdf --mode log
tty-reader book.epub --resume
```

### Disguise Modes

Target complete stealth by switching modes on the fly using `m` or `1`/`2`/`3`:

- **`normal`** — The raw text, cleanly formatted.
- **`code`** — The text is dynamically wrapped in Python structure (functions, imports, config dictionaries) with real syntax highlighting.
- **`log`** — The text is generated as a stream of timestamped server logs, colored by level.

### Boss Key
Press **`Ctrl+B`** to instantly swap your screen to a fake system monitor (process table, CPU/memory stats, build output). Press it again to go back to reading.

### Bookmarks
Your position is saved automatically when you quit. Use `--resume` (or `-r`) to pick up where you left off. Press **`b`** to manually save a bookmark at your current scroll position.

---

## Keybindings

| Key | Action |
|:---:|:---|
| `j` / `k` <br> `↑` / `↓` | Scroll up / down |
| `Space` / `PgDn` | Next page |
| `PgUp` | Previous page |
| `n` / `p` | Next / previous chapter |
| `g` / `G` | Jump to start / end |
| `m` | Cycle disguise mode |
| `1` / `2` / `3` | Force normal / code / log mode |
| `Ctrl+B` | **Boss key** (Panic button) |
| `b` | Save bookmark |
| `?` | Show help |
| `q` | Quit |

---

**Have fun reading folks!**
