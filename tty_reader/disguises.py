"""Disguise formatters — make book text look like code or server logs."""

from datetime import datetime, timedelta
from rich.syntax import Syntax
from rich.text import Text


def _seeded_random(seed: int):
    """Simple LCG for deterministic output."""
    s = seed & 0x7FFFFFFF

    def _next():
        nonlocal s
        s = (s * 1664525 + 1013904223) & 0x7FFFFFFF
        return s / 0x7FFFFFFF

    return _next



FUNC_NAMES = [
    "process_data", "handle_request", "validate_input", "transform_output",
    "configure_service", "initialize_db", "fetch_metadata", "parse_response",
    "build_query", "execute_task", "resolve_config", "sanitize_payload",
    "aggregate_results", "dispatch_event", "compute_hash", "serialize_state",
]

MODULE_NAMES = [
    "config", "utils", "services.auth", "middleware.cache",
    "sqlalchemy", "fastapi", "redis", "celery", "pydantic",
    "core.logger", "handlers.user", "models.session", "hashlib",
    "pathlib", "typing", "validators.schema", "httpx", "asyncio",
]

VAR_NAMES = [
    "config", "result", "payload", "response", "metadata",
    "session", "connection", "buffer", "context", "options",
    "settings", "params", "query", "schema", "token",
]

CLASS_NAMES = [
    "DataProcessor", "RequestHandler", "ServiceManager", "CacheLayer",
    "AuthProvider", "QueryBuilder", "EventDispatcher", "TaskRunner",
]

PARAM_NAMES = ["options", "config", "ctx", "request", "data", "params"]


def _pick(arr, rng):
    return arr[int(rng() * len(arr)) % len(arr)]


def _escape(text: str) -> str:
    """Escape quotes for embedding in code strings."""
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")


def format_as_code(text: str, page_index: int) -> Syntax:
    """Format text as realistic Python source code."""
    rng = _seeded_random(page_index * 7919 + 31337)
    lines = [l for l in text.split("\n") if l.strip()]
    output = []
    line_num = page_index * 60 + 1

    # Imports at the top
    import_count = min(2 + int(rng() * 2), len(lines))
    for i in range(import_count):
        mod = _pick(MODULE_NAMES, rng)
        var = _pick(VAR_NAMES, rng)
        safe = _escape(lines[i])
        if rng() > 0.5:
            output.append(f"from {mod} import {var}  # {safe}")
        else:
            output.append(f"import {mod}  # {safe}")

    output.append("")
    i = import_count

    templates = ["jsdoc", "func", "config", "trycatch", "class", "var"]
    tidx = int(rng() * len(templates))

    while i < len(lines):
        remaining = len(lines) - i
        template = templates[tidx % len(templates)]
        tidx += 1

        if template == "jsdoc":
            count = min(2 + int(rng() * 3), remaining)
            chunk = lines[i : i + count]
            output.append("")
            func = _pick(FUNC_NAMES, rng)
            for j, line in enumerate(chunk):
                safe = _escape(line)
                if j == 0:
                    output.append(f'def {func}({_pick(PARAM_NAMES, rng)}, {_pick(PARAM_NAMES, rng)}):')
                    output.append(f'    """{safe}')
                elif j == len(chunk) - 1:
                    output.append(f'    {safe}"""')
                else:
                    output.append(f"    {safe}")
            i += count

        elif template == "func":
            count = min(2 + int(rng() * 4), remaining)
            chunk = lines[i : i + count]
            func = _pick(FUNC_NAMES, rng)
            output.append("")
            output.append(f"async def {func}({_pick(PARAM_NAMES, rng)}):")
            for line in chunk:
                safe = _escape(line)
                if rng() > 0.5:
                    output.append(f'    {_pick(VAR_NAMES, rng)} = "{safe}"')
                else:
                    output.append(f"    # {safe}")
            output.append(f"    return {_pick(VAR_NAMES, rng)}")
            i += count

        elif template == "config":
            count = min(3 + int(rng() * 3), remaining)
            chunk = lines[i : i + count]
            keys = ["database", "host", "port", "timeout", "max_retries", "debug", "cache_ttl", "api_key"]
            var = _pick(VAR_NAMES, rng)
            output.append("")
            output.append(f"{var} = {{")
            for j, line in enumerate(chunk):
                safe = _escape(line)
                key = keys[j % len(keys)]
                comma = "," if j < len(chunk) - 1 else ","
                output.append(f'    "{key}": "{safe}"{comma}')
            output.append("}")
            i += count

        elif template == "trycatch":
            count = min(2 + int(rng() * 3), remaining)
            if count < 2:
                count = 2
            chunk = lines[i : min(i + count, len(lines))]
            func = _pick(FUNC_NAMES, rng)
            output.append("")
            output.append("try:")
            for line in chunk[:-1]:
                safe = _escape(line)
                output.append(f'    await {func}("{safe}")')
            safe_last = _escape(chunk[-1]) if chunk else "error"
            output.append("except Exception as exc:")
            output.append(f'    logger.warning(f"{safe_last}: {{exc}}")')
            i += len(chunk)

        elif template == "class":
            count = min(2 + int(rng() * 3), remaining)
            chunk = lines[i : i + count]
            cls = _pick(CLASS_NAMES, rng)
            method = _pick(FUNC_NAMES, rng)
            output.append("")
            output.append(f"class {cls}:")
            output.append(f"    def {method}(self, {_pick(PARAM_NAMES, rng)}):")
            for line in chunk:
                safe = _escape(line)
                output.append(f"        # {safe}")
            output.append(f"        return self.{_pick(VAR_NAMES, rng)}")
            i += count

        else:  # var
            safe = _escape(lines[i])
            var = _pick(VAR_NAMES, rng)
            output.append(f'{var} = "{safe}"')
            i += 1

    code_str = "\n".join(output)
    return Syntax(code_str, "python", theme="monokai", line_numbers=True, start_line=line_num)



SERVICES = [
    "api-gateway", "auth-service", "user-service", "db-manager",
    "cache-layer", "worker-01", "worker-02", "scheduler",
    "notification-svc", "payment-processor", "search-indexer",
    "file-storage", "rate-limiter", "health-check",
]

LEVELS = [
    ("INFO", "green", 45),
    ("DEBUG", "dim", 30),
    ("WARN", "yellow", 15),
    ("ERROR", "red", 8),
    ("TRACE", "dim", 2),
]

CONTEXTS = [
    "method=GET path=/api/v2/users status=200 time=45ms",
    "method=POST path=/api/v2/data status=201 time=123ms",
    "method=GET path=/api/v2/config status=200 time=12ms",
    "query=SELECT rows=128 duration=23ms pool=primary",
    "query=INSERT rows=1 duration=5ms pool=primary",
    "cache=HIT key=user:9382 ttl=300s",
    "cache=MISS key=session:4821 ttl=0s",
    "queue=jobs pending=3 processed=1847 failed=0",
    "conn=ws-4829 event=message size=1.2kb",
    "retry=2/3 backoff=500ms target=upstream-01",
    "request_id=a8f2c3d1 trace_id=7b4e9f02 span=12",
    "token=refresh scope=read:users ttl=1800s",
    "bytes_in=2048 bytes_out=8192 compression=gzip",
    "workers=4/8 heap=234mb rss=512mb uptime=3h22m",
    "task=cleanup removed=47 duration=890ms next=3600s",
]


def _pick_level(rng):
    total = sum(w for _, _, w in LEVELS)
    roll = rng() * total
    for name, color, weight in LEVELS:
        roll -= weight
        if roll <= 0:
            return name, color
    return LEVELS[0][0], LEVELS[0][1]


def _service_pid(service: str) -> int:
    h = 0
    for c in service:
        h = ((h << 5) - h + ord(c)) & 0xFFFF
    return 30000 + (h % 20000)


def format_as_log(text: str, page_index: int) -> Text:
    """Format text as realistic server logs."""
    rng = _seeded_random(page_index * 6271 + 42069)

    base = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    current_ms = int(base.timestamp() * 1000) + page_index * 30000

    result = Text()
    lines = text.split("\n")

    for i, line in enumerate(lines):
        if not line.strip():
            current_ms += int(rng() * 5000) + 2000
            result.append("\n")
            continue

        current_ms += int(rng() * 150) + 50
        ts = datetime.fromtimestamp(current_ms / 1000).strftime("%Y-%m-%dT%H:%M:%S.") + f"{current_ms % 1000:03d}Z"

        service = _pick(SERVICES, rng)
        pid = _service_pid(service)
        level_name, level_color = _pick_level(rng)
        ctx = _pick(CONTEXTS, rng)

        result.append(f"[{ts}] ", style="dim")
        result.append(f"{service:<20} ", style="cyan")
        result.append(f"pid={pid} ", style="dim")
        result.append(f"{level_name:<5} ", style=level_color)
        result.append(line.strip())
        result.append(f" | {ctx}", style="dim")

        if i < len(lines) - 1:
            result.append("\n")

    return result
