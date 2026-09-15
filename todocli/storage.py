"""
Core task storage and logic. Tasks are stored as JSON in a file in the
user's home directory, so the list persists between runs.
"""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


DATA_FILE = Path.home() / ".todocli_tasks.json"


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    priority: str = "normal"   # low, normal, high
    due_date: str | None = None
    created_at: str = ""


def _load_raw() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_raw(tasks: list[dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def load_tasks() -> list[Task]:
    return [Task(**t) for t in _load_raw()]


def save_tasks(tasks: list[Task]) -> None:
    _save_raw([asdict(t) for t in tasks])


def next_id(tasks: list[Task]) -> int:
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1


def add_task(title: str, priority: str = "normal", due_date: str | None = None) -> Task:
    tasks = load_tasks()
    task = Task(
        id=next_id(tasks),
        title=title,
        done=False,
        priority=priority,
        due_date=due_date,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    tasks.append(task)
    save_tasks(tasks)
    return task


def list_tasks(show_done: bool = True) -> list[Task]:
    tasks = load_tasks()
    if not show_done:
        tasks = [t for t in tasks if not t.done]
    return tasks


def mark_done(task_id: int) -> Task | None:
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id:
            t.done = True
            save_tasks(tasks)
            return t
    return None


def delete_task(task_id: int) -> bool:
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t.id != task_id]
    if len(new_tasks) == len(tasks):
        return False
    save_tasks(new_tasks)
    return True


def edit_task(
    task_id: int,
    title: str | None = None,
    priority: str | None = None,
    due_date: str | None = None,
) -> Task | None:
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id:
            if title is not None:
                t.title = title
            if priority is not None:
                t.priority = priority
            if due_date is not None:
                t.due_date = due_date
            save_tasks(tasks)
            return t
    return None


def clear_completed() -> int:
    tasks = load_tasks()
    remaining = [t for t in tasks if not t.done]
    removed = len(tasks) - len(remaining)
    save_tasks(remaining)
    return removed
