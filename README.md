# tty-reader

Read books in your terminal. Look like you're working.

`tty-reader` opens PDFs, EPUBs, DOCX files, and plain text right in your terminal. It can disguise whatever you're reading as source code or server logs, so it blends in with everything else on your screen.

Built with [Textual](https://textual.textualize.io/) and [Rich](https://rich.readthedocs.io/).

## Install

```bash
git clone https://github.com/ranjan-bin/terminal-reader.git
cd tty-reader
pip install -e .
```

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

### Modes

- `normal` — The raw text, cleanly formatted.
- `code` — The text is dynamically wrapped in Python structure (functions, imports, config dictionaries) with real syntax highlighting.
- `log` — The text is generated as a stream of timestamped server logs, colored by level.

Switch modes on the fly while reading by pressing `m` or `1`/`2`/`3`.

### Boss Key
Press `Ctrl+B` to instantly swap your screen to a fake system monitor (process table, CPU/memory stats, build output). Press it again to go back to reading.

### Bookmarks
Your position is saved automatically when you quit. Use `--resume` (or `-r`) to pick up where you left off. Press `b` to manually save a bookmark at your current scroll position.

## Keybindings

| Key | Action |
|---|---|
| `j`/`k`, arrows | Scroll up/down |
| `Space`, `PgDn` | Next page |
| `PgUp` | Previous page |
| `n`/`p` | Next/previous chapter |
| `g`/`G` | Jump to start/end |
| `m` | Cycle disguise mode |
| `1`/`2`/`3` | Force normal / code / log mode |
| `Ctrl+B` | Boss key |
| `b` | Save bookmark |
| `?` | Show help |
| `q` | Quit |

## Supported Formats
Supports `.pdf`, `.epub`, `.docx`, `.txt`, and `.md`. Chapters are parsed automatically from headings or flow structures.
