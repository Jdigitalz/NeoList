#!/usr/bin/env python3

import os
import sys
import stat
import time
import math
import argparse
from rich.console import Console
from rich.table import Table

parser = argparse.ArgumentParser(prog='neolist',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=35))
parser.add_argument("-s", "--simple", metavar="FORMAT", nargs="?", const="vertical",
                    help="format options: 'horizontal', 'vertical'")
parser.add_argument("-p", "--path", metavar="FILE PATH", nargs="?", const=True, type=str,
                    help="retrieve the full path of a file")
args = parser.parse_args()

os.chdir(os.getcwd())

console = Console()


def simple_view_horizontal(files, columns=6):
    console = Console()

    def make_grid(items):
        if not items:
            return
        rows = math.ceil(len(items) / columns)
        table = Table.grid(padding=(0, 2))
        for _ in range(columns):
            table.add_column(justify="left", no_wrap=True)
        grid = [[] for _ in range(rows)]
        for i, item in enumerate(items):
            grid[i % rows].append(item)
        for row in grid:
            row.extend([""] * (columns - len(row)))
            table.add_row(*row)
        console.print(table)

    visible_files = [f for f in files if not f.startswith(".")]
    simple_files = [f for f in visible_files if not os.path.isdir(f)]
    dirs = [f for f in visible_files if os.path.isdir(f)]

    simple_files_formatted = [emoji_print(f) for f in simple_files]
    dirs_formatted = [emoji_print(d) for d in dirs]

    make_grid(simple_files_formatted)
    make_grid(dirs_formatted)


def simple_view(files, style=None):
    if style == "vertical":
        simple_files = [f for f in files if not os.path.isdir(
            f) and not f.startswith(".")]
        dirs = [f for f in files if os.path.isdir(f) and not f.startswith(".")]
        for file in simple_files:
            print(emoji_print(file))
        for dir in dirs:
            print(emoji_print(dir))
    elif style == "horizontal":
        files = os.listdir()
        simple_view_horizontal(files)


# dictonary of extension with added emojis attached
extensions_values = {
    ".py": "🐍", ".js": "📜", ".ts": "📘", ".jsx": "⚛️", ".tsx": "⚛️",
    ".rb": "💎", ".pl": "🐪", ".php": "🐘", ".sh": "🐚", ".bash": "🐚", ".zsh": "🐚",
    ".ps1": "💻", ".r": "📊", ".lua": "🌙", ".tcl": "⚙️", ".dart": "🎯", ".groovy": "🎶",
    ".jl": "⚛️", ".c": "🔧", ".cpp": "➕", ".h": "📜", ".hpp": "📜", ".rs": "🦀",
    ".go": "🐹", ".java": "☕", ".cs": "🔷", ".swift": "🐦", ".kt": "🪪", ".kts": "🪪",
    ".scala": "🪜", ".hs": "λ", ".f90": "🔢", ".for": "🔢", ".m": "📈", ".asm": "🧠",
    ".html": "🌐", ".htm": "🌐", ".css": "🎨", ".scss": "🎨", ".sass": "🎨",
    ".xml": "🏷️", ".json": "📄", ".md": "📝", ".markdown": "📝", ".rst": "📚",
    ".yml": "🛠️", ".yaml": "🛠️", ".toml": "🛠️", ".ini": "⚙️", ".cfg": "⚙️",
    ".conf": "🛠️", ".env": "🌱", ".dockerfile": "🐳", ".dockerignore": "🚫",
    ".gitignore": "🚫", ".gitattributes": "", ".editorconfig": "🛠️",
    ".bat": "📁", ".cmd": "🖥️", ".command": "⌨️", ".makefile": "🏗️", ".mk": "🏗️",
    ".lock": "🔒", ".pom": "📦", ".gradle": "🛠️", ".jar": "🫙", ".class": "📦",
    ".csproj": "📦", ".sln": "🧩", ".vcxproj": "🧱", ".ninja": "🥷",
    ".desktop": "🖥️", ".lnk": "🔗", ".sys": "⚙️", ".dll": "🧩", ".so": "🧩",
    ".db": "🗃️", ".db3": "🗃️", ".sqlite": "🗃️", ".sqlite3": "🗃️",
    ".csv": "📊", ".tsv": "📊", ".xls": "📊", ".xlsx": "📊", ".ods": "📊",
    ".parquet": "🧱", ".avro": "📦", ".orc": "📦", ".rds": "📊", ".ipynb": "📒",
    ".txt": "📄", ".pdf": "📄", ".doc": "📄", ".docx": "📄", ".odt": "📄",
    ".log": "📝", ".rtf": "📄",
    ".ppt": "🎥", ".pptx": "🎥", ".odp": "🎥",
    ".zip": "🗃️", ".rar": "🗃️", ".7z": "🗃️", ".tar": "🗃️", ".gz": "🗃️", ".tgz": "🗃️",
    ".jpg": "📷", ".jpeg": "📷", ".png": "📷", ".gif": "📷", ".bmp": "📷",
    ".tiff": "📷", ".webp": "📷", ".ico": "📷", ".svg": "🖋️", ".psd": "🎨",
    ".mp3": "🎵", ".wav": "🎵", ".flac": "🎵", ".aac": "🎵", ".ogg": "🎵", ".m4a": "🎵",
    ".mp4": "🎬", ".mov": "🎬", ".avi": "🎬", ".mkv": "🎬", ".webm": "🎬",
    ".flv": "🎬", ".wmv": "🎬",
    ".bak": "💾", ".tmp": "⏳", ".swp": "💤", ".out": "📤", ".bin": "📦",
    ".exe": "🧩", ".apk": "📱", ".iso": "📀", ".dmg": "💿"
}


def file_permissions(filename):
    return ''.join([('r' if os.stat(filename).st_mode & perm else '-') for perm in [
        stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR, stat.S_IRGRP, stat.S_IWGRP,
        stat.S_IXGRP, stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH]])


def file_timestamp(filename):
    mod_time = os.stat(filename).st_mtime
    return time.strftime('%Y-%m-%d %I:%M %p', time.localtime(mod_time))


def file_size(filename):
    return str(os.stat(filename).st_size)

def emoji_print(filename):
    if os.path.isdir(filename):
        emoji = "📁"
    else:
        file_ext = os.path.splitext(filename)[1].lower()
        emoji = extensions_values.get(file_ext, "❓")
    return f"{emoji} {filename}"


def dot_print(filename):
    return f"⚙️{filename}"


def main():
    files = os.listdir()
    if not files:
        exit()
    dot_entries = [f for f in files if f.startswith(".")]
    dot_files = [f for f in dot_entries if os.path.isfile(f)]
    dot_dirs = [f for f in dot_entries if os.path.isdir(f)]
    regular_files = [f for f in files if not os.path.isdir(
        f) and not f.startswith(".")]
    directories = [f for f in files if os.path.isdir(
        f) and not f.startswith(".")]
    table = Table(show_header=True, header_style="bold",
                  show_edge=False, box=False)

    table.add_column("Permissions", justify="center", style="dim")
    table.add_column("Timestamp", justify="center", style="dim")
    table.add_column("File Size", justify="center", style="dim")
    table.add_column("File", justify="left")

    for file in dot_files:
        table.add_row(
            file_permissions(file),
            file_timestamp(file),
            file_size(file),
            dot_print(file)
        )

    for file in regular_files:
        table.add_row(
            file_permissions(file),
            file_timestamp(file),
            file_size(file),
            emoji_print(file)
        )

    for file in dot_dirs:
        table.add_row(
            file_permissions(file),
            file_timestamp(file),
            file_size(file),
            emoji_print(file)
        )

    for file in directories:
        table.add_row(
            file_permissions(file),
            file_timestamp(file),
            file_size(file),
            emoji_print(file)
        )

    console.print(table)


if __name__ == "__main__":
    files = os.listdir()
    if len(sys.argv) == 1:
        main()
    elif args.simple == "vertical":
        simple_view(files, "vertical")
    elif args.simple == "horizontal":
        simple_view(files, "horizontal")
    elif args.path is True:
        console.print("[yellow]Please provide a file path[/yellow]")
    elif isinstance(args.path, str):
        if os.path.exists(args.path):
            print(os.path.abspath(args.path))
        else:
            console.print(f"[yellow]Could not find file '{
                          args.path}'[/yellow]")
