#!/usr/bin/env python3
"""
update_progress.py

Scans the solution folders in this repo and auto-updates the
progress table inside README.md between the markers:

<!-- PROGRESS_START -->
...table...
<!-- PROGRESS_END -->

Usage:
    python update_progress.py

Run this any time after adding new solution files, then commit
the updated README.md along with your new solutions.

Folder structure expected:
    hackerrank.cooking/
    ├── python/
    ├── data-structures/
    ├── algorithms/
    ├── sql/
    └── ai/

Each solved problem should be its own file inside the relevant
folder (any extension counts: .py, .sql, .txt, .md, etc).
"""

import os

# Map folder name -> pretty label shown in the README table
TOPICS = {
    "python": "Python",
    "data-structures": "Data Structures",
    "algorithms": "Algorithms",
    "sql": "SQL",
    "ai": "Artificial Intelligence",
}

README_PATH = "README.md"
START_MARKER = "<!-- PROGRESS_START -->"
END_MARKER = "<!-- PROGRESS_END -->"


def count_solutions(folder):
    """Count files (not directories) inside a folder, recursively."""
    if not os.path.isdir(folder):
        return 0
    total = 0
    for root, _, files in os.walk(folder):
        for f in files:
            if not f.startswith("."):  # skip hidden files like .DS_Store
                total += 1
    return total


def build_table():
    rows = []
    rows.append("| Topic | Problems Solved |")
    rows.append("|-------|------------------|")
    grand_total = 0
    for folder, label in TOPICS.items():
        count = count_solutions(folder)
        grand_total += count
        rows.append(f"| {label} | {count} |")
    rows.append(f"| **Total** | **{grand_total}** |")
    return "\n".join(rows)


def update_readme():
    if not os.path.exists(README_PATH):
        print(f"Could not find {README_PATH} in the current directory.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if START_MARKER not in content or END_MARKER not in content:
        print(
            "Could not find PROGRESS_START / PROGRESS_END markers in README.md.\n"
            "Add these two lines around your progress table:\n\n"
            f"{START_MARKER}\n(table will go here)\n{END_MARKER}"
        )
        return

    before = content.split(START_MARKER)[0]
    after = content.split(END_MARKER)[1]
    new_table = build_table()

    new_content = f"{before}{START_MARKER}\n{new_table}\n{END_MARKER}{after}"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README.md progress table updated successfully.")
    print()
    print(new_table)


if __name__ == "__main__":
    update_readme()