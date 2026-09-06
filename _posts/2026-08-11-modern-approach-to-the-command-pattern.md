---
layout: post
title: "Building a Python CLI with Typer: The Modern Approach to the Command Pattern"
slug: building-a-python-cli-with-typer-the-modern-approach-to-the-command-pattern
post_series_id:
  - python-cli-command-pattern
  - modern-python-application
image: /assets/img/building-a-python-cli-with-typer-the-modern-approach-to-the-command-pattern.png
excerpt: Typer brings Python type hints to CLI development — no decorators, no boilerplate, just annotated functions. See how it compares to argparse and Click on the same Task Manager CLI.
categories:
  - "Programming"
---

# Building a Python CLI with Typer: The Modern Approach to the Command Pattern
_Posted on **{{ page.date | date_to_string }}**_

![Building a Python CLI with Typer: The Modern Approach to the Command Pattern]({{ site.baseurl }}/assets/img/building-a-python-cli-with-typer-the-modern-approach-to-the-command-pattern.png){:width="760" height="400" .responsive_img}

## Introduction

You have already built the same Task Manager CLI twice. In [Part 1]({{ site.baseurl }}/building-a-python-cli-with-the-command-pattern/) you used Python's built-in `argparse` module and the Command Pattern to get a clean, extensible structure. In [Part 2]({{ site.baseurl }}/building-a-python-cli-with-click-a-cleaner-approach-to-the-command-pattern/) you replaced argparse with Click — the code got shorter, type validation became automatic, and the Command Pattern survived without a shared `execute(**kwargs)` interface.

Now we do it a third time with [Typer](https://typer.tiangolo.com). Typer turns Python's own type annotations into a complete CLI — no option decorator stacks, no explicit type parameters, just function signatures. The result is the most readable version of the three, and it is the one I use in my own projects.

You should read this article if:

- You have read Parts 1 and 2 and want to see the evolution complete.
- You want a CLI library that is natively type-safe and plays well with mypy and IDE autocompletion.
- You want a real-world reference showing Typer in a real project before committing to it.

## argparse vs Click vs Typer at a Glance

Before diving into code, here is the complete picture:

| **Property** | argparse | Click | Typer |
|---|---|---|---|
| **Where it comes from** | Standard library | Third-party | Third-party (built on Click) |
| **How commands are defined** | `add_subparsers()` + `add_parser()` | `@click.command` / `@click.group` decorators | Annotated function signatures — no option decorators |
| **Type conversion** | Manual (`type=int`) | Decorator parameter (`type=int`) | Inferred from annotation (`: int`) |
| **Validation on bad input** | Manual | Automatic, built-in error message | Automatic, built-in error message |
| **Sub-apps / command groups** | Nested `add_subparsers()` | `@click.group` | `typer.Typer()` added via `app.add_typer()` |
| **`--help` generation** | From `help=` string | From `help=` string | From docstring + `help=` string |
| **IDE autocompletion for params** | None | Partial | Full — standard type hints |
| **Lines of code (task add)** | ~12 | ~4 | ~3 |

> Typer is to CLIs what FastAPI is to web APIs: the same idea of driving behaviour from type annotations rather than from imperative configuration.

## Why Typer?

Click removed the argparse boilerplate. Typer removes the option decorator stack.

To be precise: Typer still uses a decorator to register a command (`@app.command()`), just like Click. What disappears are all the `@click.option` and `@click.argument` decorators that pile up above every function in Click. With one option those are manageable; with four or five options the function itself disappears under a tower of decorators.

With Click, every option requires an explicit `@click.option("--name", type=str, required=True)` decorator. The type is declared twice — once in the decorator, once in the function signature — and they can silently drift apart. Typer merges the two: the function signature is the definition, and the single `@app.command()` decorator is the only one you need.

Two more practical gains:

1. **Docstrings become help text.** Write `"""Deploy a new agent sandbox."""` on a function and Typer uses it for `--help`. You document the code and the CLI at the same time.
2. **`Optional` and `Annotated` work as you expect.** `name: str | None = None` is an optional option. `Annotated[str, typer.Option(help="Task name")]` adds metadata without a separate decorator.

Typer is built on top of Click, so every Click feature is still available if you need it. You are not giving anything up.

## Installing Typer

```shell
uv add "typer[all]"
```

Breaking down the options:

- `typer` — the core library
- `[all]` — installs `rich` (coloured output, formatted help pages) and `shellingham` (shell auto-completion detection); highly recommended for end-user CLIs

Running `uv add` records the dependency in `pyproject.toml` and updates `uv.lock` — no manual editing needed.

## The Task Manager CLI — Code Walkthrough

The CLI syntax stays the same as in Parts 1 and 2:

```shell
python3 cli.py task add --name "Buy milk"
python3 cli.py task list
python3 cli.py task delete --id 1
python3 cli.py stats summary
python3 cli.py stats export --output report.csv
```

No external repository this time — all code lives inline in this article.

### Project Structure

```text
task-cli/
├── cli.py
└── commands/
    ├── __init__.py
    ├── base.py
    ├── add_task_command.py
    ├── list_task_command.py
    ├── delete_task_command.py
    └── stats_command.py
```

The structure is identical to Parts 1 and 2. Only `cli.py` changes significantly.

### The Base Command Class

Same marker pattern introduced in the Click version — no shared `execute()` method, just a semantic boundary:

```python
# commands/base.py
from abc import ABC


class Command(ABC):
    """Marker base class for CLI commands."""
```

### The Concrete Command Classes

The command classes are unchanged from the Click version. Each method carries an explicit, typed signature:

```python
# commands/add_task_command.py
from .base import Command


class AddTaskCommand(Command):
    def execute(self, name: str) -> None:
        with open("tasks.txt", "a") as f:
            f.write(name + "\n")
        print(f"Task added: {name}")
```

```python
# commands/list_task_command.py
from .base import Command


class ListTaskCommand(Command):
    def execute(self) -> None:
        try:
            with open("tasks.txt") as f:
                tasks = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            tasks = []
        if not tasks:
            print("No tasks found.")
            return
        print("Tasks:")
        for i, t in enumerate(tasks, 1):
            print(f"{i}. {t}")
```

```python
# commands/delete_task_command.py
from .base import Command


class DeleteTaskCommand(Command):
    def execute(self, task_id: int) -> None:
        try:
            with open("tasks.txt") as f:
                tasks = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("No tasks found.")
            return
        if task_id < 1 or task_id > len(tasks):
            print(f"Invalid task ID: {task_id}")
            return
        removed = tasks.pop(task_id - 1)
        with open("tasks.txt", "w") as f:
            f.write("\n".join(tasks))
        print(f"Task deleted: {removed}")
```

```python
# commands/stats_command.py
import csv
import os
from .base import Command


class StatsCommand(Command):
    TASKS_FILE = "tasks.txt"

    def summary(self) -> None:
        tasks = self._load_tasks()
        print(f"You have {len(tasks)} task(s).")
        for i, t in enumerate(tasks, 1):
            print(f"{i}. {t}")

    def export(self, output: str) -> None:
        tasks = self._load_tasks()
        if not tasks:
            print("No tasks to export.")
            return
        with open(output, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Task"])
            for i, task in enumerate(tasks, 1):
                writer.writerow([i, task])
        print(f"Tasks exported to {output}")

    def _load_tasks(self) -> list[str]:
        if not os.path.exists(self.TASKS_FILE):
            return []
        with open(self.TASKS_FILE) as f:
            return [line.strip() for line in f if line.strip()]
```

### The CLI Entry Point

This is where Typer replaces Click. Compare the structure to the Click version and notice what disappears: no `@click.option` decorator stacks, no explicit `type=` parameters.

```python
# cli.py
from typing import Annotated
import typer
from commands.add_task_command import AddTaskCommand
from commands.list_task_command import ListTaskCommand
from commands.delete_task_command import DeleteTaskCommand
from commands.stats_command import StatsCommand

app = typer.Typer(help="Task Manager CLI", no_args_is_help=True)
task_app = typer.Typer(help="Manage tasks.", no_args_is_help=True)
stats_app = typer.Typer(help="Show or export task statistics.", no_args_is_help=True)

app.add_typer(task_app, name="task")
app.add_typer(stats_app, name="stats")


@task_app.command("add")
def task_add(
    name: Annotated[str, typer.Option("--name", "-n", help="Task name.")],
) -> None:
    """Add a new task."""
    AddTaskCommand().execute(name=name)


@task_app.command("list")
def task_list() -> None:
    """List all tasks."""
    ListTaskCommand().execute()


@task_app.command("delete")
def task_delete(
    task_id: Annotated[int, typer.Option("--id", "-i", help="Task ID to delete.")],
) -> None:
    """Delete a task by ID."""
    DeleteTaskCommand().execute(task_id=task_id)


@stats_app.command("summary")
def stats_summary() -> None:
    """Show a summary of all tasks."""
    StatsCommand().summary()


@stats_app.command("export")
def stats_export(
    output: Annotated[
        str, typer.Option("--output", "-o", help="Output CSV file name.")
    ] = "tasks.csv",
) -> None:
    """Export tasks to a CSV file."""
    StatsCommand().export(output=output)


if __name__ == "__main__":
    app()
```

A few things worth noting:

- `app.add_typer(task_app, name="task")` registers a sub-app — the equivalent of `@click.group`. Each sub-app is an independent `typer.Typer()` instance.
- `Annotated[str, typer.Option(...)]` is the idiomatic Typer way to attach help text and flags to a parameter while keeping the type annotation separate and readable by mypy.
- The function docstring (`"""Add a new task."""`) becomes the command description in `--help` automatically.
- `no_args_is_help=True` on each app means running `python3 cli.py` or `python3 cli.py task` without a subcommand prints the help page instead of doing nothing.

### Running the CLI

```shell
python3 cli.py task add --name "Write Part 3"
python3 cli.py task add --name "Review PR"
python3 cli.py task list
python3 cli.py task delete --id 1
python3 cli.py stats summary
python3 cli.py stats export --output report.csv
```

The `--help` output for the top-level app:

```shell
python3 cli.py --help
```

Typer renders a rich, coloured help page listing all registered sub-apps and commands — at no extra cost.

## Side-by-Side: the Same Command in Three Libraries

To make the progression concrete, here is `task add` implemented in all three:

**argparse (Part 1)**

```python
add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument("--name", required=True, help="Task name")
add_parser.set_defaults(func=self.commands["add"].execute)
```

**Click (Part 2)**

```python
@cli.command(help="Add a new task")
@click.option("--name", "-n", required=True, help="Task name")
def add(name):
    AddTaskCommand().execute(name=name)
```

**Typer (this article)**

```python
@task_app.command("add")
def task_add(
    name: Annotated[str, typer.Option("--name", "-n", help="Task name.")],
) -> None:
    """Add a new task."""
    AddTaskCommand().execute(name=name)
```

| **Property** | argparse | Click | Typer |
|---|---|---|---|
| **Lines for `task add`** | 3 | 4 (2 decorators + function) | 3 (1 decorator + function) |
| **Type declared explicitly** | `type=str` (default) | `type=str` (default) | Inferred from `: str` |
| **Help text location** | `help=` in `add_argument` | `help=` in `@click.option` | Function docstring |
| **Required enforced by** | `required=True` | `required=True` | No default value present |
| **mypy compatibility** | Low — `args.name` is `Any` | Medium — decorator type and signature can drift | High — annotation is the single source of truth |

## A Real-World Reference: golem-cli

The pattern above is not just a toy example. [golem-cli](https://github.com/sasadangelo/golem-cli) is the CLI client for a real Agentic AI Platform-as-a-Service project I am working on, built with exactly this structure.

The `cli.py` entry point is pure Typer wiring — no business logic:

```python
# src/golem_cli/cli.py (excerpt)
app = typer.Typer(
    name="golem", help="golem — Golem Agent-as-a-Service CLI", no_args_is_help=True
)

agent_app = typer.Typer(help="Manage agent sandboxes.", no_args_is_help=True)
app.add_typer(agent_app, name="agent")


@agent_app.command("create")
def agent_create(
    config: Annotated[
        Path, typer.Option("--config", "-c", help="Path to the runner config YAML.")
    ],
    ttl: Annotated[
        int, typer.Option("--ttl", "-t", help="Sandbox time-to-live in seconds.")
    ] = 3600,
) -> None:
    """Deploy a new agent sandbox."""
    AgentCommand().create(config=config, ttl_seconds=ttl)
```

The business logic lives entirely in `AgentCommand`, `ChatCommand`, and `CpCommand` — the Command Pattern is preserved cleanly. The CLI file's only job is to map flags to method calls.

The project structure mirrors what you built in this series:

```text
golem-cli/
└── src/
    └── golem_cli/
        ├── cli.py              ← Typer wiring only
        └── commands/
            ├── base.py         ← Marker ABC
            ├── agent_command.py
            ├── chat_command.py
            └── cp_command.py
```

When Typer is your chosen library, this is what a real project looks like.

## When to Keep Using Click

Typer is the better default for new projects, but Click still wins in specific cases:

- **You are extending an existing Click-based codebase.** Typer can wrap Click objects, but mixing them adds complexity — stay pure.
- **You need Click plugins or third-party Click extensions.** The ecosystem is built around Click's decorator API.
- **You need fine-grained control over context objects and pass-through behaviour.** Click's `@click.pass_context` is more explicit for advanced orchestration.

For everything else — new projects, in-house tools, developer utilities — Typer's type-hint–driven approach is cleaner and safer.

## Conclusion

In this article we covered:

- Why Typer eliminates the decorator boilerplate that Click still requires, by inferring command structure from type annotations
- How to build a complete Task Manager CLI with Typer: sub-apps, typed options, docstring-driven help text
- How the same Command Pattern from Parts 1 and 2 carries over unchanged — business logic in command classes, wiring in `cli.py`
- A side-by-side comparison of `argparse`, Click, and Typer on the same command, with a concrete table of differences
- How `golem-cli` applies this exact pattern in a real project

This is the final article in the Python CLI series. The three posts together form a complete toolkit: argparse for zero-dependency scripts, Click for mature ecosystems, Typer for new projects where type safety and readability matter. For a deeper dive into the Command Pattern used throughout the series, the [Refactoring.Guru reference](https://refactoring.guru/design-patterns/command) is still the best starting point.

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌
