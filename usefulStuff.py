"""
utils.py — General-purpose terminal utilities for Python projects.

Usage:
    from utils import slow_print, print_separator, ...
"""

import time
import os
import sys
import textwrap
import random


# ── Text Output ───────────────────────────────────────────────────────────────

def slow_print(text: str, delay: float = 0.03, newline: bool = True):
    """Print text one character at a time."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    if newline:
        print()


def print_separator(char: str = "-", width: int = 40):
    """Print a horizontal separator line."""
    print(char * width)


def print_header(title: str, char: str = "=", width: int = 40):
    """Print a centred title between two separator lines."""
    print(char * width)
    print(title.center(width))
    print(char * width)


def print_boxed(text: str, width: int = 40, char: str = "#"):
    """Print text inside a simple box."""
    inner = width - 4
    lines = textwrap.wrap(text, inner)
    border = char * width
    print(border)
    for line in lines:
        print(f"{char} {line:<{inner}} {char}")
    print(border)


def print_table(headers: list, rows: list, col_width: int = 15):
    """Print a simple aligned table.

    Example:
        print_table(["Name", "Score"], [["Alice", 42], ["Bob", 7]])
    """
    def fmt_row(row):
        return "  ".join(str(cell).ljust(col_width) for cell in row)

    print_separator("-", col_width * len(headers) + 2 * (len(headers) - 1))
    print(fmt_row(headers))
    print_separator("-", col_width * len(headers) + 2 * (len(headers) - 1))
    for row in rows:
        print(fmt_row(row))
    print_separator("-", col_width * len(headers) + 2 * (len(headers) - 1))


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def countdown(seconds: int, message: str = "Starting in"):
    """Print a countdown timer."""
    for i in range(seconds, 0, -1):
        print(f"\r{message} {i}...", end="", flush=True)
        time.sleep(1)
    print()


# ── Input Helpers ─────────────────────────────────────────────────────────────

def prompt_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Prompt until the user enters a valid integer, optionally within a range."""
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"  Please enter a number >= {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"  Please enter a number <= {max_val}.")
                continue
            return value
        except ValueError:
            print("  Invalid input — please enter a whole number.")


def prompt_float(prompt: str, min_val: float = None, max_val: float = None) -> float:
    """Prompt until the user enters a valid float, optionally within a range."""
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"  Please enter a number >= {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"  Please enter a number <= {max_val}.")
                continue
            return value
        except ValueError:
            print("  Invalid input — please enter a number.")


def prompt_choice(prompt: str, choices: list) -> str:
    """Prompt until the user picks one of the allowed choices (case-insensitive)."""
    lower = [c.lower() for c in choices]
    options = "/".join(choices)
    while True:
        answer = input(f"{prompt} [{options}]: ").strip().lower()
        if answer in lower:
            return choices[lower.index(answer)]
        print(f"  Please enter one of: {options}")


def prompt_yes_no(prompt: str) -> bool:
    """Prompt for a yes/no answer. Returns True for yes."""
    return prompt_choice(prompt, ["yes", "no"]) == "yes"


def prompt_non_empty(prompt: str) -> str:
    """Prompt until the user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Input cannot be empty.")


# ── Colour (ANSI) ─────────────────────────────────────────────────────────────

class Color:
    """ANSI colour codes. Use Color.RED + text + Color.RESET."""
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"
    BOLD    = "\033[1m"
    RESET   = "\033[0m"


def cprint(text: str, color: str):
    """Print text in the given ANSI color, then reset."""
    print(f"{color}{text}{Color.RESET}")


# ── Timing ────────────────────────────────────────────────────────────────────

class Timer:
    """Simple elapsed-time context manager / manual timer.

    Example:
        with Timer() as t:
            do_work()
        print(t.elapsed())
    """
    def __init__(self):
        self._start = None
        self._end = None

    def start(self):
        self._start = time.perf_counter()

    def stop(self):
        self._end = time.perf_counter()

    def elapsed(self) -> float:
        end = self._end if self._end else time.perf_counter()
        return round(end - (self._start or end), 4)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_):
        self.stop()


# ── Random Helpers ────────────────────────────────────────────────────────────

def roll_dice(sides: int = 6, count: int = 1) -> list:
    """Roll `count` dice with `sides` sides. Returns list of results."""
    return [random.randint(1, sides) for _ in range(count)]


def weighted_choice(options: list, weights: list):
    """Pick one item from options using relative weights.

    Example:
        weighted_choice(["common", "rare", "legendary"], [70, 25, 5])
    """
    return random.choices(options, weights=weights, k=1)[0]


def clamp(value, min_val, max_val):
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))


# ── Progress Bar ──────────────────────────────────────────────────────────────

def progress_bar(current: int, total: int, width: int = 30, label: str = "") -> str:
    """Return a text progress bar string.

    Example:
        print(progress_bar(7, 10, label="HP"))  →  HP [#####################         ] 70%
    """
    pct = current / total if total else 0
    filled = int(width * pct)
    bar = "#" * filled + " " * (width - filled)
    prefix = f"{label} " if label else ""
    return f"{prefix}[{bar}] {int(pct * 100)}%"
