"""File picker screen for selecting files."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DirectoryTree, Header, Footer


class FilePickerScreen(Screen):
    """Screen containing a directory tree to pick a file."""

    BINDINGS = [
        ("escape", "app.pop_screen", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DirectoryTree(".")
        yield Footer()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Called when the user selects a file in the directory tree."""
        # Check if the file has a supported extension
        ext = event.path.suffix.lower()
        if ext in [".pdf", ".epub", ".docx", ".txt", ".md"]:
            self.app.load_file(str(event.path))
            self.app.pop_screen()
        else:
            self.app.notify("Unsupported file type")
