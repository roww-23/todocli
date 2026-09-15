"""
Command-line to-do list manager.

Usage examples:
    todocli add "Buy groceries"
    todocli add "Finish report" --priority high --due 2026-09-20

    todocli list
    todocli list --pending

    todocli done 2
    todocli edit 2 --title "Finish report v2" --priority low
    todocli delete 2
    todocli clear
"""

import argparse
import sys

from todocli import storage


PRIORITY_ICONS = {"high": "[!]", "normal": "[ ]", "low": "[-]"}


def _print_task(task: storage.Task) -> None:
    status = "x" if task.done else " "
    icon = PRIORITY_ICONS.get(task.priority, "[ ]")
    due = f" (due {task.due_date})" if task.due_date else ""
    print(f"[{status}] #{task.id} {icon} {task.title}{due}")


def handle_add(args: argparse.Namespace) -> None:
    task = storage.add_task(args.title, priority=args.priority, due_date=args.due)
    print(f"Added task #{task.id}: {task.title}")


def handle_list(args: argparse.Namespace) -> None:
    tasks = storage.list_tasks(show_done=not args.pending)
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        _print_task(task)


def handle_done(args: argparse.Namespace) -> None:
    task = storage.mark_done(args.task_id)
    if task:
        print(f"Marked #{task.id} as done: {task.title}")
    else:
        print(f"No task found with id {args.task_id}", file=sys.stderr)
        sys.exit(1)


def handle_delete(args: argparse.Namespace) -> None:
    success = storage.delete_task(args.task_id)
    if success:
        print(f"Deleted task #{args.task_id}")
    else:
        print(f"No task found with id {args.task_id}", file=sys.stderr)
        sys.exit(1)


def handle_edit(args: argparse.Namespace) -> None:
    task = storage.edit_task(
        args.task_id, title=args.title, priority=args.priority, due_date=args.due
    )
    if task:
        print(f"Updated task #{task.id}:")
        _print_task(task)
    else:
        print(f"No task found with id {args.task_id}", file=sys.stderr)
        sys.exit(1)


def handle_clear(args: argparse.Namespace) -> None:
    removed = storage.clear_completed()
    print(f"Removed {removed} completed task(s).")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todocli",
        description="A simple command-line to-do list manager.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task description")
    add_parser.add_argument(
        "--priority", choices=["low", "normal", "high"], default="normal"
    )
    add_parser.add_argument("--due", default=None, help="Due date, e.g. 2026-09-20")
    add_parser.set_defaults(func=handle_add)

    # list
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "--pending", action="store_true", help="Show only tasks that aren't done"
    )
    list_parser.set_defaults(func=handle_list)

    # done
    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("task_id", type=int, help="ID of the task")
    done_parser.set_defaults(func=handle_done)

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID of the task")
    delete_parser.set_defaults(func=handle_delete)

    # edit
    edit_parser = subparsers.add_parser("edit", help="Edit a task")
    edit_parser.add_argument("task_id", type=int, help="ID of the task")
    edit_parser.add_argument("--title", default=None, help="New title")
    edit_parser.add_argument(
        "--priority", choices=["low", "normal", "high"], default=None
    )
    edit_parser.add_argument("--due", default=None, help="New due date")
    edit_parser.set_defaults(func=handle_edit)

    # clear
    clear_parser = subparsers.add_parser("clear", help="Remove all completed tasks")
    clear_parser.set_defaults(func=handle_clear)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
