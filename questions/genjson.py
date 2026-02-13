import os
import json
import sys

# This is a helper script to generate assessment zones out of our questions.

# Configuration
TARGET_DIR = "DFAs/practice"

def generate_questions_json(target=TARGET_DIR, title=None):
    if (title is not None):
        data = {"title": title, "questions": []}
    else:
        data = {"questions": []}

    # Verify directory exists
    if not os.path.exists(target):
        print(f"Error: Directory '{target}' not found.")
        return

    # Get all entries in the directory, sorted alphabetically
    entries = sorted(os.listdir(target))

    for entry_name in entries:
        full_path = os.path.join(target, entry_name)

        # Check if it is actually a directory
        if os.path.isdir(full_path):
            
            # Ensure we use forward slashes even on Windows for consistency
            clean_path = full_path.replace("\\", "/")
            
            question_obj = {
                "id": clean_path,
                "points": 1
            }
            data["questions"].append(question_obj)

    # Print to console (stdout)
    print(json.dumps(data, indent=4))

if __name__ == "__main__":
    if (len(sys.argv) > 2):
        generate_questions_json(sys.argv[1], " ".join(sys.argv[2:]))
    elif (len(sys.argv) == 2):
        generate_questions_json(sys.argv[1])
    else:
        generate_questions_json()
