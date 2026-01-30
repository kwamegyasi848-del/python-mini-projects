import os
import shutil
import argparse

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Audio": [".mp3", ".wav"],
    "Video": [".mp4", ".mov"],
    "Archives": [".zip", ".rar"],
    "Code": [".py", ".js", ".java"]
}

def get_category(extension):
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"

def organize_files(path, dry_run=False):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if os.path.isfile(item_path):
            ext = os.path.splitext(item)[1].lower()
            category = get_category(ext)

            target_dir = os.path.join(path, category)

            if not dry_run:
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(item_path, os.path.join(target_dir, item))

            print(f"{'[DRY RUN]' if dry_run else 'Moved'} {item} → {category}/")

def main():
    parser = argparse.ArgumentParser(description="Organize files by category.")
    parser.add_argument("--path", required=True, help="Target folder path")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes")

    args = parser.parse_args()

    organize_files(args.path, args.dry_run)

if __name__ == "__main__":
    main()
