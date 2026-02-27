"""Boss key screen — fake system monitor."""

import random
from datetime import datetime

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import DataTable, Static


PROCESSES = [
    ("1", "root", 0.0, 0.1, "0:03.21", "/sbin/launchd"),
    ("287", "root", 0.3, 1.2, "0:45.10", "/usr/libexec/logd"),
    ("1847", "ranjan", 12.4, 4.2, "2:13.87", "node dist/server.js --port 3000"),
    ("1851", "postgres", 8.1, 15.7, "1:47.23", "postgres: worker process"),
    ("1923", "ranjan", 5.7, 2.3, "0:58.44", "npm run build:watch"),
    ("2102", "redis", 2.4, 1.1, "0:32.19", "redis-server *:6379"),
    ("2200", "nginx", 0.8, 0.3, "0:15.02", "nginx: worker process"),
    ("2201", "nginx", 0.6, 0.3, "0:14.88", "nginx: worker process"),
    ("2350", "ranjan", 3.2, 1.8, "0:42.55", "webpack --config webpack.prod.js"),
    ("2478", "ranjan", 1.1, 0.9, "0:22.31", "node_modules/.bin/jest --watch"),
    ("2591", "ranjan", 0.4, 0.5, "0:08.12", "node scripts/migrate.js"),
    ("2644", "ranjan", 15.8, 6.1, "3:21.05", "docker compose up -d"),
    ("2701", "_mysql", 4.3, 8.4, "1:05.33", "mysqld --defaults-file=/etc/my.cnf"),
    ("2899", "ranjan", 0.2, 0.4, "0:03.77", "tail -f /var/log/app/production.log"),
    ("3011", "ranjan", 0.1, 0.2, "0:01.44", "ssh -N -L 5433:db.internal:5432 bastion"),
]

BUILD_LINES = [
    "[bold]TypeScript Compiler v5.6.3[/bold]",
    "",
    "  [green]✓[/green] src/index.ts [dim](342ms)[/dim]",
    "  [green]✓[/green] src/app.ts [dim](215ms)[/dim]",
    "  [green]✓[/green] src/routes/api.ts [dim](891ms)[/dim]",
    "  [green]✓[/green] src/routes/auth.ts [dim](445ms)[/dim]",
    "  [green]✓[/green] src/middleware/cors.ts [dim](122ms)[/dim]",
    "  [green]✓[/green] src/models/User.ts [dim](678ms)[/dim]",
    "  [green]✓[/green] src/services/email.ts [dim](234ms)[/dim]",
    "  [green]✓[/green] src/utils/crypto.ts [dim](156ms)[/dim]",
    "",
    "[bold]Bundle size:[/bold] 445KB → 156KB [green](minified + gzip)[/green]",
    "[green][bold]Build completed successfully in 3.2s[/bold][/green]",
    "",
    "[dim]Watching for file changes...[/dim]",
    "",
    "[bold]Test Suites:[/bold]  [green]47 passed[/green], 47 total",
    "[bold]Tests:[/bold]       [green]312 passed[/green], 312 total",
    "[bold]Snapshots:[/bold]   [green]23 passed[/green], 23 total",
    f"[bold]Time:[/bold]        6.847s",
]


def _progress_bar(percent: float, width: int = 30) -> str:
    filled = int(percent / 100 * width)
    empty = width - filled
    color = "green" if percent < 60 else ("yellow" if percent < 80 else "red")
    return f"[{color}]{'█' * filled}[/{color}]{'░' * empty}"


class BossScreen(Screen):
    """Fake system monitor dashboard."""

    BINDINGS = [
        Binding("ctrl+b", "pop_screen", "Back", show=False),
        Binding("escape", "pop_screen", "Back", show=False),
        Binding("q", "pop_screen", "Back", show=False),
    ]

    DEFAULT_CSS = """
    BossScreen {
        background: #0d1117;
    }

    #boss-title {
        dock: top;
        height: 1;
        background: #1f6feb;
        color: white;
        padding: 0 1;
    }

    #process-table {
        height: 1fr;
        margin: 0 1;
    }

    #stats {
        height: 5;
        margin: 0 1;
        padding: 1;
        background: #161b22;
        border: solid #30363d;
    }

    #build-output {
        height: 22;
        margin: 0 1;
        padding: 1;
        background: #161b22;
        border: solid #30363d;
    }
    """

    def compose(self) -> ComposeResult:
        now = datetime.now().strftime("%H:%M:%S")
        yield Static(
            f" System Monitor — ranjan@macbook — Load: 2.34 1.87 1.45 — Uptime: 14d 3:22 — {now}",
            id="boss-title",
        )
        yield DataTable(id="process-table")

        cpu_avg = random.uniform(25, 55)
        mem_pct = random.uniform(60, 75)
        yield Static(
            f"  CPU: {_progress_bar(cpu_avg)} {cpu_avg:.1f}%    Tasks: 312 total, 3 running\n"
            f"  Mem: {_progress_bar(mem_pct)} {mem_pct:.1f}%    5.4G / 8.0G    Swap: 0B / 2.0G",
            id="stats",
            markup=True,
        )

        yield Static("\n".join(BUILD_LINES), id="build-output", markup=True)

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("PID", "USER", "%CPU", "%MEM", "TIME+", "COMMAND")
        table.cursor_type = "row"

        for pid, user, cpu, mem, time, cmd in PROCESSES:
            cpu_jitter = max(0, cpu + random.uniform(-1, 1))
            mem_jitter = max(0, mem + random.uniform(-0.3, 0.3))
            table.add_row(pid, user, f"{cpu_jitter:.1f}", f"{mem_jitter:.1f}", time, cmd)

    def action_pop_screen(self) -> None:
        self.app.pop_screen()
