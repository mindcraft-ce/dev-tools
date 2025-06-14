# auto_diff.py
#
# A Python script to automatically generate a diff patch file from two
# input files. This script uses the 'unified diff' format, which is a
# standard for patch files and is used by tools like 'git' and 'diff'.

import difflib
import sys
from datetime import datetime, timezone

# --- Configuration ---
# The names of the two files to compare.
FILE1_NAME = "input1"
FILE2_NAME = "input2"

# The name of the output patch file.
PATCH_FILE_NAME = "diff.patch"
# ---------------------

def generate_diff():
    """
    Reads two files and generates a patch file based on their differences.
    """
    print("--- Automatic Diff Generator ---")

    # Read the contents of the first file
    try:
        print(f"Reading original file: {FILE1_NAME}")
        with open(FILE1_NAME, 'r', encoding='utf-8') as f1:
            # .readlines() keeps the newlines, which difflib handles correctly
            file1_lines = f1.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{FILE1_NAME}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading {FILE1_NAME}: {e}")
        sys.exit(1)

    # Read the contents of the second file
    try:
        print(f"Reading new file: {FILE2_NAME}")
        with open(FILE2_NAME, 'r', encoding='utf-8') as f2:
            file2_lines = f2.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{FILE2_NAME}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading {FILE2_NAME}: {e}")
        sys.exit(1)

    # Get current time for the file headers in the diff
    now = datetime.now(timezone.utc).astimezone().isoformat()

    # Generate the diff in the "unified" format
    # The result is a generator, which yields the lines of the diff.
    diff_lines = difflib.unified_diff(
        file1_lines,
        file2_lines,
        fromfile=FILE1_NAME,
        tofile=FILE2_NAME,
        fromfiledate=now,
        tofiledate=now,
        lineterm='\n' # Use standard newline character
    )
    
    # The diff generator might return no lines if the files are identical.
    # We convert the generator to a list to check if it's empty.
    diff_list = list(diff_lines)

    if not diff_list:
        print("\nFiles are identical. No patch file will be created.")
        return

    # Write the generated diff to the patch file
    try:
        print(f"Writing differences to patch file: {PATCH_FILE_NAME}")
        with open(PATCH_FILE_NAME, 'w', encoding='utf-8') as patch_file:
            # .writelines() is efficient for writing a list of lines
            patch_file.writelines(diff_list)
    except Exception as e:
        print(f"An error occurred while writing the patch file: {e}")
        sys.exit(1)

    print(f"\nSuccessfully created patch file: '{PATCH_FILE_NAME}'")
    print("You can apply this patch using a command like: patch input1 < diff.patch")


if __name__ == "__main__":
    generate_diff()