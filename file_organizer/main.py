import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".heic"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".ppt", ".pptx", ".xls", ".xlsx"},
    "Audio": {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"},
    "Video": {".mp4", ".mov", ".mkv", ".avi", ".wmv"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".rb", ".go", ".rs", ".html", ".css", ".sql"},
}

def pick_category(ext: str) -> str:
    ext = ext.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def organize(folder: Path, dry_run: bool = False) -> dict:
    if not folder.exists():
        raise FileNotFoundError(f"Path does not exist: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a folder: {folder}")

    counts = {}
    moved = 0

    for item in folder.iterdir():
        if item.is_dir():
            continue

        category = pick_category(item.suffix)
        dest_dir = folder / category
        dest_path = dest_dir / item.name

        if dest_path.exists():
            stem, suffix = item.stem, item.suffix
            i = 1
            while True:
                candidate = dest_dir / f"{stem} ({i}){suffix}"
                if not candidate.exists():
                    dest_path = candidate
                    break
                i += 1

        counts[category] = counts.get(category, 0) + 1

        if dry_run:
            print(f"[DRY RUN] Would move: {item.name} -> {category}/")
        else:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_path))
            print(f"✅ Moved: {item.name} -> {category}/")
        moved += 1

    print("\n--- Summary ---")
    print(f"Files processed: {moved}")
    for cat in sorted(counts.keys()):
        print(f"{cat}: {counts[cat]}")
    return counts

def main():
    parser = argparse.ArgumentParser(description="Organize files in a folder by file type.")
    parser.add_argument("--path", type=str, default=".", help="Folder path to organize (default: current folder)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without moving files")
    args = parser.parse_args()

    folder = Path(args.path).expanduser().resolve()
    organize(folder, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
