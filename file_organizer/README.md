# File Organizer (Python)

Organizes files in a folder into category subfolders (Images, Documents, Audio, Video, Archives, Code, Other).

## Run
Dry run (no changes):
python main.py --path "C:\Path\To\Folder" --dry-run

Move files:
python main.py --path "C:\Path\To\Folder"

## Notes
- Skips subfolders (only moves files).
- Prevents overwriting by auto-renaming duplicates.
