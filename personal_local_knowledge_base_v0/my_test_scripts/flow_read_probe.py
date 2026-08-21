
"""Print the first 20 records/lines from a local data file."""

from pathlib import Path
import sys

sys.stdout.reconfigure(errors="backslashreplace")

# Allow direct execution from the repository checkout, e.g. ``python path/to/this.py``.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from knowledge_search.dataset_reader import iter_local_dureader


def _path_from_input() -> Path:
    raw_path = sys.argv[1] if len(sys.argv) > 1 else input("Path: ")
    raw_path = raw_path.strip()
    # PowerShell commonly pastes a quoted path; input() keeps those quotes.
    if len(raw_path) >= 2 and raw_path[0] == raw_path[-1] and raw_path[0] in {'"', "'"}:
        raw_path = raw_path[1:-1]
    return Path(raw_path).expanduser()


path = _path_from_input()

if path.suffix.lower() == ".parquet":
    for count, record in enumerate(iter_local_dureader(path), start=1):
        print(record)
        if count == 20:
            break
else:
    with path.open("r", encoding="utf-8") as stream:
        for count, line in enumerate(stream, start=1):
            print(line, end="")
            if count == 20:
                break
