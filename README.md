# todocli

A simple Python command-line to-do list manager. Tasks are stored as JSON
in your home folder (`~/.todocli_tasks.json`), so they persist between runs.

## Requirements

- Python 3.10+

## Setup

Since `pip install -e .` gave us trouble with `gitcli`, you can use either
approach here too:

**Option A — install it (may need `py` instead of `pip` on Windows):**
```bash
cd todocli
py -m pip install -e .
```

**Option B — skip installing, just run it directly (always works):**
```bash
cd todocli
py -m todocli.cli <command> ...
```

## Usage

### Add a task
```bash
todocli add "Buy groceries"
todocli add "Finish report" --priority high --due 2026-09-20
```

### List tasks
```bash
todocli list              # show all tasks
todocli list --pending    # show only tasks that aren't done
```

### Mark a task done
```bash
todocli done 2
```

### Edit a task
```bash
todocli edit 2 --title "Finish report v2" --priority low --due 2026-09-25
```

### Delete a task
```bash
todocli delete 2
```

### Clear all completed tasks
```bash
todocli clear
```

## Command reference

| Command | Arguments/Options | Description |
|---|---|---|
| `add`    | `title`, `--priority`, `--due` | Add a new task |
| `list`   | `--pending` | List tasks (all, or only pending) |
| `done`   | `task_id` | Mark a task as complete |
| `edit`   | `task_id`, `--title`, `--priority`, `--due` | Update a task |
| `delete` | `task_id` | Remove a task |
| `clear`  | — | Remove all completed tasks |

## How it's structured

- `todocli/storage.py` — the data logic: loading/saving tasks to JSON,
  and functions like `add_task`, `mark_done`, `delete_task`
- `todocli/cli.py` — the command-line interface: reads what you typed
  and calls the right function in `storage.py`

Same pattern as the `gitcli` project — the "doing" logic is separate
from the "command" layer, so either piece could be reused elsewhere.
