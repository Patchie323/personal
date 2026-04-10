"""
utils.py — General-purpose terminal utilities for Python projects.

Usage:
    from utils import *
"""

import time
import os
import sys
import textwrap
import random
import webbrowser
import subprocess


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

# ── String Helpers ────────────────────────────────────────────────────────────

def truncate(text: str, max_len: int, suffix: str = "...") -> str:
    """Shorten text to max_len characters, appending suffix if cut.

    Example:
        truncate("Hello, world!", 8)  →  "Hello..."
    """
    if len(text) <= max_len:
        return text
    return text[:max_len - len(suffix)] + suffix


def typewriter(text: str, delay: float = 0.05, newline: bool = True):
    """Print text with a blinking cursor effect between characters."""
    for i, char in enumerate(text):
        print(f"\r{text[:i + 1]}_", end="", flush=True)
        time.sleep(delay)
    print(f"\r{text} ", end="")
    if newline:
        print()


# ── Math Helpers ──────────────────────────────────────────────────────────────

def map_range(value: float, in_min: float, in_max: float,
              out_min: float, out_max: float) -> float:
    """Rescale a value from one range to another.

    Example:
        map_range(50, 0, 100, 0, 255)  →  127.5   (half HP → half brightness)
        map_range(7, 0, 10, 0, 30)    →  21.0    (score → bar width)
    """
    if in_max == in_min:
        return out_min
    ratio = (value - in_min) / (in_max - in_min)
    return out_min + ratio * (out_max - out_min)


# ── Time Helpers ──────────────────────────────────────────────────────────────

def format_duration(seconds: float) -> str:
    """Convert a number of seconds into a human-readable string.

    Examples:
        format_duration(45)    →  "45s"
        format_duration(3661)  →  "1h 2m 1s"
        format_duration(90)    →  "1m 30s"
    """
    seconds = int(seconds)
    parts = []
    for unit, size in [("h", 3600), ("m", 60), ("s", 1)]:
        if seconds >= size:
            parts.append(f"{seconds // size}{unit}")
            seconds %= size
    return " ".join(parts) if parts else "0s"


# ── Terminal UI ───────────────────────────────────────────────────────────────

def menu(title: str, options: list) -> int:
    """Display a numbered menu and return the index (0-based) of the user's choice.

    Example:
        idx = menu("Main Menu", ["Start Game", "Load Game", "Quit"])
    """
    print_separator()
    print(f"  {title}")
    print_separator()
    for i, option in enumerate(options, 1):
        print(f"  [{i}] {option}")
    print_separator()
    return prompt_int("  > ", min_val=1, max_val=len(options)) - 1


def paginate(items: list, page_size: int = 10, title: str = ""):
    """Display a list in pages with next/prev navigation.

    Yields nothing — handles display and navigation internally.
    """
    total = len(items)
    page = 0
    total_pages = max(1, -(-total // page_size))  # ceiling division

    while True:
        clear_screen()
        if title:
            print_header(title)
        start = page * page_size
        chunk = items[start:start + page_size]
        for i, item in enumerate(chunk, start + 1):
            print(f"  {i:>3}. {item}")

        print_separator()
        print(f"  Page {page + 1}/{total_pages}  ({total} items)")
        nav = []
        if page > 0:
            nav.append("[P] Prev")
        if page < total_pages - 1:
            nav.append("[N] Next")
        nav.append("[Q] Quit")
        print("  " + "  ".join(nav))

        choice = input("  > ").strip().lower()
        if choice == "n" and page < total_pages - 1:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        elif choice == "q":
            break


# ── System / OS ──────────────────────────────────────────────────────────────

def confirm_action(prompt: str = "Are you sure?") -> bool:
    """Require the user to type 'yes' in full before proceeding.

    Returns True if confirmed, False otherwise. Intended for destructive actions.

    Example:
        if confirm_action("Delete all save files?"):
            delete_saves()
    """
    print(f"  {prompt}")
    print("  Type 'yes' to confirm: ", end="")
    return input().strip().lower() == "yes"


def copy_to_clipboard(text: str):
    """Copy text to the system clipboard.

    Works on macOS (pbcopy), Windows (clip), and Linux (xclip/xsel).
    """
    if sys.platform == "darwin":
        subprocess.run(["pbcopy"], input=text.encode(), check=True)
    elif sys.platform == "win32":
        subprocess.run(["clip"], input=text.encode(), check=True)
    else:
        try:
            subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)
        except FileNotFoundError:
            subprocess.run(["xsel", "--clipboard", "--input"], input=text.encode(), check=True)


def open_in_browser(url: str):
    """Open a URL in the default web browser."""
    webbrowser.open(url)


def open_file(path: str):
    """Open a file or folder with the default system application."""
    if sys.platform == "darwin":
        subprocess.run(["open", path], check=True)
    elif sys.platform == "win32":
        os.startfile(path)
    else:
        subprocess.run(["xdg-open", path], check=True)


def beep(count: int = 1):
    """Sound the terminal bell `count` times."""
    for _ in range(count):
        print("\a", end="", flush=True)
        if count > 1:
            time.sleep(0.3)


# ── String Extras ─────────────────────────────────────────────────────────────

def pluralize(n: int, word: str, plural: str = None) -> str:
    """Return 'n word' or 'n words' depending on n.

    Optionally supply an irregular plural form.

    Examples:
        pluralize(1, "item")         →  "1 item"
        pluralize(3, "item")         →  "3 items"
        pluralize(2, "person", "people")  →  "2 people"
    """
    if n == 1:
        return f"{n} {word}"
    return f"{n} {plural if plural else word + 's'}"


def wrap_text(text: str, width: int = 72, indent: str = "") -> str:
    """Word-wrap text to a given width, with optional leading indent per line.

    Example:
        print(wrap_text("A very long string...", width=40, indent="  "))
    """
    return textwrap.fill(text, width=width, initial_indent=indent, subsequent_indent=indent)


# ── Spinner ───────────────────────────────────────────────────────────────────
def spinner(duration: float = 2.0, delay: float = 0.1, label: str = ""):
    """Print a rotating spinner (-, /, |, \) for the specified duration.

    Args:
        duration: Total time in seconds to display the spinner.
        delay: Time in seconds between frames.
        label: Optional text to show before the spinner character.
    """
    chars = ["-", "/", "|", "\\"]
    if delay <= 0:
        return
    steps = int(duration / delay)
    for i in range(steps):
        print(f"\r{label} {chars[i % len(chars)]}", end="", flush=True)
        time.sleep(delay)
    # Clear the spinner line
    print("\r" + " " * (len(label) + 2) + "\r", end="")
