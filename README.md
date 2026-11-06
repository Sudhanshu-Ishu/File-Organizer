# File Organizer

A command-line tool written in Python that sorts files from a source folder into category folders inside a separate destination folder.

Built by Sudhanshu Yadav as a task for Codenova.

## Features

- Dry-run preview by default: nothing is moved unless `--apply` is used
- Confirmation prompt (`yes`) before any file is moved
- Separate source and destination folders (identical or nested folders are rejected)
- Categories: Images, Documents, Code, Videos, Audio, Archives, Others
- Duplicate filenames are renamed (`photo.jpg` becomes `photo_1.jpg`) instead of being overwritten
- Log file (`organizer_log.txt`) saved in the destination folder
- Graceful handling of a missing source folder, permission errors, and failed moves

## Requirements

- Python 3.8 or newer (no external libraries)

## Usage

Preview only:

```
python main.py SourceFolder DestinationFolder
```

Move the files:

```
python main.py SourceFolder DestinationFolder --apply
```

## Example

```
python main.py SourceTest DestinationTest

Preview of file organization:
--------------------------------------------------
code.py -> Code/code.py
document.pdf -> Documents/document.pdf
photo.jpg -> Images/photo.jpg
--------------------------------------------------
Total files to organize: 3
Dry-run complete. No files have been moved.
```