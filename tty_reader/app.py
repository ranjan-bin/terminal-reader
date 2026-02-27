"""Main Textual app — layout, bindings, mode switching, CLI."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import RichLog, Static

from . import reader, text_utils, bookmarks, disguises
from .screens.boss import BossScreen
from .screens.help import HelpScreen


class TTYReaderApp(App):
    """Terminal document reader with stealth modes."""

    CSS_PATH = "styles/app.tcss"

    BINDINGS = [
        Binding("q", "quit_app", "Quit", show=False),
        Binding("space", "next_page", "Next Pg", show=True),
        Binding("pagedown", "next_page", "PgDn", show=False),
        Binding("pageup", "prev_page", "PgUp", show=False),
        Binding("j", "scroll_down", "↓", show=False),
        Binding("k", "scroll_up", "↑", show=False),
        Binding("down", "scroll_down", "Down", show=False),
        Binding("up", "scroll_up", "Up", show=False),
        Binding("n", "next_chapter", "Next Ch", show=True),
        Binding("p", "prev_chapter", "Prev Ch", show=True),
        Binding("g", "go_start", "Start", show=False),
        Binding("G", "go_end", "End", show=False),
        Binding("m", "cycle_mode", "Mode", show=True),
        Binding("1", "mode_normal", "Normal", show=False),
        Binding("2", "mode_code", "Code", show=False),
        Binding("3", "mode_log", "Log", show=False),
        Binding("ctrl+b", "boss_key", "Boss", show=True),
        Binding("b", "bookmark", "Save", show=True),
        Binding("question_mark", "show_help", "Help", show=True),
    ]

    def __init__(
        self,
        file_path: Optional[str] = None,
        mode: str = "normal",
        resume: bool = False,
    ):
        super().__init__()
        self.file_path = file_path
        self.display_mode = mode
        self.resume = resume

        # Document state
        self.document = None
        self.all_lines: list[str] = []
        self.chapter_starts: list[int] = []
        self.chapter_titles: list[str] = []
        self.total_lines = 0
        self.lines_per_page = 30

    def compose(self) -> ComposeResult:
        yield RichLog(id="content", highlight=False, markup=False, wrap=True)
        yield Static("", id="status-bar")

    def on_mount(self) -> None:
        if self.file_path:
            self.load_file(self.file_path)
        else:
            from .screens.picker import FilePickerScreen
            self.push_screen(FilePickerScreen())

    def load_file(self, path: str) -> None:
        self.file_path = path
        self.document = reader.read_file(self.file_path)
        self.title = self.document["metadata"].get("title", Path(self.file_path).name)

        self._reflow_content()
        self._render_content()

        # Resume from bookmark
        if self.resume:
            bm = bookmarks.get_bookmark(self.document["metadata"]["file_hash"])
            if bm:
                if bm.get("mode"):
                    self.display_mode = bm["mode"]
                    self._render_content()
                if bm.get("scroll_line"):
                    content = self.query_one("#content", RichLog)
                    content.scroll_to(y=bm["scroll_line"], animate=False)

        self._update_status()

    def _reflow_content(self) -> None:
        width = self.size.width - 4 if self.size.width > 10 else 76
        self.lines_per_page = max(1, (self.size.height or 24) - 2)

        self.all_lines = []
        self.chapter_starts = []
        self.chapter_titles = []

        for i, chapter in enumerate(self.document["chapters"]):
            self.chapter_starts.append(len(self.all_lines))
            self.chapter_titles.append(chapter["title"])

            reflowed = text_utils.reflow(chapter["content"], width)
            self.all_lines.extend(reflowed.split("\n"))

            if i < len(self.document["chapters"]) - 1:
                self.all_lines.extend(["", "───", ""])

        self.total_lines = len(self.all_lines)

    def _render_content(self) -> None:
        content = self.query_one("#content", RichLog)
        content.clear()

        if self.display_mode == "normal":
            content.write("\n".join(self.all_lines))
        elif self.display_mode == "code":
            page_size = self.lines_per_page or 40
            for i in range(0, len(self.all_lines), page_size):
                chunk = "\n".join(self.all_lines[i : i + page_size])
                page_idx = i // page_size
                content.write(disguises.format_as_code(chunk, page_idx))
        elif self.display_mode == "log":
            page_size = self.lines_per_page or 40
            for i in range(0, len(self.all_lines), page_size):
                chunk = "\n".join(self.all_lines[i : i + page_size])
                page_idx = i // page_size
                content.write(disguises.format_as_log(chunk, page_idx))

    def _get_current_chapter(self) -> int:
        content = self.query_one("#content", RichLog)
        scroll_y = content.scroll_offset.y
        chapter_idx = 0
        for i, start in enumerate(self.chapter_starts):
            if scroll_y >= start:
                chapter_idx = i
            else:
                break
        return chapter_idx

    def _update_status(self) -> None:
        content = self.query_one("#content", RichLog)
        status = self.query_one("#status-bar", Static)

        scroll_y = content.scroll_offset.y
        total_pages = max(1, self.total_lines // max(1, self.lines_per_page))
        current_page = min(scroll_y // max(1, self.lines_per_page) + 1, total_pages)
        max_scroll = max(1, self.total_lines - self.lines_per_page)
        percent = min(100, int(scroll_y / max_scroll * 100)) if max_scroll > 0 else 0

        chapter_idx = self._get_current_chapter()
        ch_title = self.chapter_titles[chapter_idx] if chapter_idx < len(self.chapter_titles) else ""

        mode_labels = {"normal": "NORMAL", "code": "CODE", "log": "LOG"}
        mode = mode_labels.get(self.display_mode, self.display_mode.upper())

        filename = Path(self.file_path).name
        status.update(f" {filename} | Pg {current_page}/{total_pages} | {percent}% | [{mode}] | {ch_title}")


    def on_rich_log_scroll(self) -> None:
        self._update_status()

    def watch_scroll_y(self) -> None:
        self._update_status()


    def action_scroll_down(self) -> None:
        self.query_one("#content", RichLog).scroll_down()
        self._update_status()

    def action_scroll_up(self) -> None:
        self.query_one("#content", RichLog).scroll_up()
        self._update_status()

    def action_next_page(self) -> None:
        content = self.query_one("#content", RichLog)
        content.scroll_to(y=content.scroll_offset.y + self.lines_per_page, animate=False)
        self._update_status()

    def action_prev_page(self) -> None:
        content = self.query_one("#content", RichLog)
        target = max(0, content.scroll_offset.y - self.lines_per_page)
        content.scroll_to(y=target, animate=False)
        self._update_status()

    def action_next_chapter(self) -> None:
        current = self._get_current_chapter()
        next_ch = min(current + 1, len(self.chapter_starts) - 1)
        content = self.query_one("#content", RichLog)
        content.scroll_to(y=self.chapter_starts[next_ch], animate=False)
        self._update_status()

    def action_prev_chapter(self) -> None:
        current = self._get_current_chapter()
        prev_ch = max(current - 1, 0)
        content = self.query_one("#content", RichLog)
        content.scroll_to(y=self.chapter_starts[prev_ch], animate=False)
        self._update_status()

    def action_go_start(self) -> None:
        self.query_one("#content", RichLog).scroll_to(y=0, animate=False)
        self._update_status()

    def action_go_end(self) -> None:
        content = self.query_one("#content", RichLog)
        content.scroll_to(y=self.total_lines, animate=False)
        self._update_status()

    def action_cycle_mode(self) -> None:
        modes = ["normal", "code", "log"]
        idx = modes.index(self.display_mode)
        self.display_mode = modes[(idx + 1) % len(modes)]
        saved = self.query_one("#content", RichLog).scroll_offset.y
        self._render_content()
        self.query_one("#content", RichLog).scroll_to(y=saved, animate=False)
        self._update_status()

    def action_mode_normal(self) -> None:
        self._set_mode("normal")

    def action_mode_code(self) -> None:
        self._set_mode("code")

    def action_mode_log(self) -> None:
        self._set_mode("log")

    def _set_mode(self, mode: str) -> None:
        if self.display_mode == mode:
            return
        self.display_mode = mode
        saved = self.query_one("#content", RichLog).scroll_offset.y
        self._render_content()
        self.query_one("#content", RichLog).scroll_to(y=saved, animate=False)
        self._update_status()

    def action_boss_key(self) -> None:
        self.push_screen(BossScreen())

    def action_show_help(self) -> None:
        self.push_screen(HelpScreen())

    def action_bookmark(self) -> None:
        content = self.query_one("#content", RichLog)
        scroll_y = content.scroll_offset.y
        chapter_idx = self._get_current_chapter()

        bookmarks.save_bookmark(self.document["metadata"]["file_hash"], {
            "chapter": chapter_idx,
            "scroll_line": scroll_y,
            "mode": self.display_mode,
            "file_name": Path(self.file_path).name,
            "file_path": self.file_path,
        })

        status = self.query_one("#status-bar", Static)
        status.update(" Bookmark saved!")
        self.set_timer(1.5, self._update_status)

    def action_quit_app(self) -> None:
        # Auto-save position
        content = self.query_one("#content", RichLog)
        scroll_y = content.scroll_offset.y
        chapter_idx = self._get_current_chapter()

        bookmarks.save_bookmark(self.document["metadata"]["file_hash"], {
            "chapter": chapter_idx,
            "scroll_line": scroll_y,
            "mode": self.display_mode,
            "file_name": Path(self.file_path).name,
            "file_path": self.file_path,
        })
        self.exit()

    def on_resize(self) -> None:
        if self.document is None:
            return
        old_scroll = self.query_one("#content", RichLog).scroll_offset.y
        self._reflow_content()
        self._render_content()
        self.query_one("#content", RichLog).scroll_to(y=old_scroll, animate=False)
        self._update_status()


def main():
    parser = argparse.ArgumentParser(
        prog="tty-reader",
        description="Read books in your terminal. Look like you're working.",
    )
    parser.add_argument("file", nargs="?", help="File to read (PDF, EPUB, DOCX, TXT, MD)")
    parser.add_argument(
        "-m", "--mode",
        choices=["normal", "code", "log"],
        default="normal",
        help="Display mode (default: normal)",
    )
    parser.add_argument(
        "-r", "--resume",
        action="store_true",
        help="Resume from last saved reading position",
    )

    args = parser.parse_args()

    file_path = None
    if args.file:
        file_path = str(Path(args.file).resolve())
        if not Path(file_path).exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)

    app = TTYReaderApp(file_path=file_path, mode=args.mode, resume=args.resume)
    app.run()


if __name__ == "__main__":
    main()
