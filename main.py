import argparse
import shutil
from datetime import datetime
from pathlib import Path

LOG_NAME = "organizer_log.txt"

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"},
    "Code": {".py", ".js", ".ts", ".java", ".c", ".cpp", ".html", ".css", ".json"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov"},
    "Audio": {".mp3", ".wav", ".flac", ".aac"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
}


def get_category(file_path):
    """Return the category folder name for a file."""
    ext = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def organize_files(source_folder, target_folder):
    """Prepare file organization operations."""
    source = Path(source_folder)
    target = Path(target_folder)
    operations = []

    for file_path in source.iterdir():
        if not file_path.is_file() or file_path.name == LOG_NAME:
            continue

        destination_folder = target / get_category(file_path)
        destination_file = destination_folder / file_path.name
        counter = 1

        while destination_file.exists() or any(
            destination == destination_file for _, destination in operations
        ):
            new_name = f"{file_path.stem}_{counter}{file_path.suffix}"
            destination_file = destination_folder / new_name
            counter += 1

        operations.append((file_path, destination_file))

    return operations


def write_log(log_file, lines):
    """Append log lines; never crash if logging fails."""
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
    except OSError as error:
        print(f"Warning: could not write log file: {error}")


def main():
    parser = argparse.ArgumentParser(
        description="Organize files into category folders."
    )
    parser.add_argument("source", help="Path to the folder containing files to organize.")
    parser.add_argument("target", help="Path to the destination folder.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move the files. Without this flag, only a preview is shown.",
    )
    args = parser.parse_args()

    source_folder = Path(args.source).resolve()
    target_folder = Path(args.target).resolve()

    if not source_folder.exists() or not source_folder.is_dir():
        print(f"Error: Source folder not found: {source_folder}")
        return

    if (
        source_folder == target_folder
        or source_folder in target_folder.parents
        or target_folder in source_folder.parents
    ):
        print("Error: Source and destination must be separate folders.")
        return

    try:
        operations = organize_files(source_folder, target_folder)
    except PermissionError as error:
        print(f"Error: Permission denied while reading source folder: {error}")
        return
    except OSError as error:
        print(f"Error: Could not read source folder: {error}")
        return

    if not operations:
        print("No files found to organize.")
        return

    print("\nPreview of file organization:")
    print("-" * 50)
    for source_file, destination_file in operations:
        relative = destination_file.relative_to(target_folder).as_posix()
        print(f"{source_file.name} -> {relative}")
    print("-" * 50)
    print(f"Total files to organize: {len(operations)}")

    if not args.apply:
        print("Dry-run complete. No files have been moved.")
        print("Add --apply to move the files.")
        return

    answer = input("\nMove these files? Type 'yes' to continue: ").strip().lower()
    if answer != "yes":
        print("Cancelled. No files have been moved.")
        return

    try:
        target_folder.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"Error: Could not create destination folder: {error}")
        return

    log_file = target_folder / LOG_NAME
    log_lines = [f"--- Run at {datetime.now():%Y-%m-%d %H:%M:%S} ---"]
    moved = 0
    skipped = 0

    for source_file, destination_file in operations:
        relative = destination_file.relative_to(target_folder).as_posix()
        try:
            destination_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_file), str(destination_file))
            print(f"Moved: {source_file.name} -> {relative}")
            log_lines.append(f"MOVED: {source_file.name} -> {relative}")
            moved += 1
        except (PermissionError, OSError) as error:
            print(f"Skipped: {source_file.name} ({error})")
            log_lines.append(f"SKIPPED: {source_file.name} ({error})")
            skipped += 1

    write_log(log_file, log_lines)

    print("\nOrganization complete.")
    print(f"Files moved: {moved}")
    print(f"Files skipped: {skipped}")


if __name__ == "__main__":
    main()