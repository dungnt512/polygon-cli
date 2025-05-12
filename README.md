# polygon-cli
Command-line tool for [polygon](https://polygon.codeforces.com/)

## Requirements

* Python 3 (tested on 3.4)
* requests lib
* prettytable lib
* colorama lib
* pyyaml lib
* diff and diff3 available in path

## Supported features

* Download files and solutions from polygon.
* Uploading them back to polygon.
* Automatic merging with conflicts.
* Download checkers from polygon.
* List all available problemsets (sorted by ID, newest first).
* Enhanced package downloading with format options and PIN support.
* Initialize by problem name instead of just ID.
* Automatically extract PIN code from problem URL.
* Download all problem files with package-like directory structure.

## Installation

### Using pip3

Run `pip3 install polygon-cli`

### Using the source code

1. Install Python3 and setuputils module (for example, it goes with pip3)
2. Checkout repo using `git clone https://github.com/kunyavskiy/polygon-cli.git`

3. Run `python3 setup.py install [--user]`

      * On Linux, it will put the executable polygon-cli in /usr/local/bin
      * On Windows, it will create a polygon-cli.exe in Python/Scripts folder

## First launch

Type `polygon-cli init <problem-id>` or `polygon-cli init <problem-name>` to start working with problem

The CLI will ask you for:
1. Polygon URL (default: https://polygon.codeforces.com)
2. Login credentials
3. API key and secret

## Basic usage

### Using the API key

1. Go to the settings page (click your login in the upper right corner of the Polygon site and select "settings")
2. Go to the third tab, it is about the API keys
3. If you had no key, add a key, add a description to it if you want and click "Create" button. Copy the key and the secret
4. If you already have a key, you can use it, just click "Show key and secret" (you can have several keys)

### Commands

To get the list of available commands, type `polygon-cli --help` or just `polygon-cli`

Current commands are:

* login - Log in to polygon.
* init - Initialize tool for problem.
* init_contest - Initialize tool for several problems in contest.
* update - Download files from polygon working copy, and merge with local copy if needed.
* add - Upload files to polygon working copy.
* commit - Put all polygon working copy to polygon main revision.
* diff - Display diff of local and polygon version of file.
* list - List files in polygon.
* download_package - Download package from polygon.
* download_checker - Download checker from polygon.
* download_all_tests - Download all tests from polygon.
* list_problemset - List all available problem sets.
* download_files - Download all problem files with package-like structure.

### Package Download Example

```bash
# Download Windows package
polygon-cli download_package

# Download Linux package with custom filename
polygon-cli download_package --format linux -o my_problem.zip

# Download package with PIN
polygon-cli download_package --pin p85dIBF 
```

### Working with problem by name

When initializing a problem, you can use its name instead of ID:

```bash
polygon-cli init a-plus-b
```

The system will automatically find the problem ID and save it along with the problem owner and PIN code.

### Download All Problem Files

The `download_files` command downloads all files from a problem and organizes them in a directory structure similar to the package format:

```bash
# Basic usage - downloads to directory named after problem
polygon-cli download_files

# Download to a specific directory
polygon-cli download_files --output my_problem_files

# Create a ZIP archive in addition to the directory
polygon-cli download_files --create-zip

# Overwrite existing directory
polygon-cli download_files --force

# Download silently (no progress messages)
polygon-cli download_files --quiet
```

This creates a directory structure like:
```
my_problem_files/
├── src/           # Source files (including checker, validator, etc.)
├── tests/         # Test files
├── solutions/     # Solutions
├── statements/    # Problem statements
└── problem_info.txt
```

## New Features

### Download Checker
Download the problem's checker with:
```
polygon-cli download_checker [--target PATH]
```

### List All Problemsets
List all available problemsets:
```
polygon-cli list_problemset
```

### Enhanced Package Download
Download package with more options:
```
polygon-cli download_package [--format {windows,linux,mac}] [--output FILE_PATH] [--pin PIN_CODE]
```

### Download All Files with Package Structure
Download all problem files with a package-like structure:
```
polygon-cli download_files [--output DIR_PATH] [--create-zip] [--force] [--quiet]
```
