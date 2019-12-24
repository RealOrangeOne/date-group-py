# Date Group
Group a directory of files.

Dates are determined through multiple sources:

- EXIF metadata
- Date in filename

## Installation

Install the dependencies specified in `requirements.txt`.

## Usage

Script takes just 1 argument, the path to group. All files in subdirectories will be moved. `--dry-run` can be moved to just print the files and groups rather than actually move them.

Files whose dates can't be parsed, are left in-place.
