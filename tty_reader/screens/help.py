"""Help screen — modal keybinding reference."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Middle
from textual.screen import ModalScreen
from textual.widgets import Static


HELP_TEXT = """\
[bold yellow]Keybindings[/bold yellow]

  [bold]j/k[/bold], [bold]↑/↓[/bold]       Scroll line by line
  [bold]Space[/bold]/[bold]PgDn[/bold]     Next page
  [bold]PgUp[/bold]           Previous page
  [bold]n[/bold]/[bold]p[/bold]             Next / previous chapter
  [bold]g[/bold]               Go to beginning
  [bold]G[/bold]               Go to end

  [bold]m[/bold]               Cycle mode (normal/code/log)
  [bold]1[/bold]/[bold]2[/bold]/[bold]3[/bold]           Switch mode directly

  [bold]Ctrl+B[/bold]          Boss key (fake dashboard)
  [bold]b[/bold]               Save bookmark

  [bold]?[/bold]               Toggle this help
  [bold]q[/bold]               Quit (auto-saves position)

  [dim]Press ? or Escape to close[/dim]"""


class HelpScreen(ModalScreen):
    """Modal keybinding help overlay."""

    BINDINGS = [
        Binding("escape", "close", "Close", show=False),
        Binding("question_mark", "close", "Close", show=False),
    ]

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }

    #help-box {
        width: 54;
        height: 24;
        background: #161b22;
        border: solid #f0c674;
        padding: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static(HELP_TEXT, id="help-box", markup=True)

    def action_close(self) -> None:
        self.app.pop_screen()
