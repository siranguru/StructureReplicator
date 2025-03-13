import os
import re
import argparse

def parse_tree(tree_str):
    """
    Parse a tree-like string (e.g. output from "tree /F") into a nested dictionary.
    Folders are stored as keys whose values are dictionaries.
    Files are stored as keys with value None.
    
    The algorithm:
      1. The first non-blank line is taken as the root.
      2. For each subsequent line, determine its depth by counting the leading
         characters (spaces and vertical bars '│') before the connector ("├── " or "└── ").
         We assume each indent level corresponds to 4 characters.
      3. Remove the connector and extra spaces to extract the name.
      4. If the name ends with '/', it is a folder (stored as a dict) with the slash removed;
         otherwise, it’s a file (stored with value None).
      5. A stack is used to keep track of the current branch.
    """
    lines = [line.rstrip() for line in tree_str.splitlines() if line.strip()]
    if not lines:
        return {}
    
    root_line = lines[0].strip()
    root = root_line.strip("/")
    tree = {root: {}}
    stack = [(0, tree[root])]
    
    for line in lines[1:]:
        indent_match = re.match(r'^([ │]+)', line)
        indent_str = indent_match.group(1) if indent_match else ""
        level = len(indent_str) // 4
        
        line_without_indent = re.sub(r'^[ │]*(├── |└── )', '', line)
        name = line_without_indent.strip()
        
        if name.endswith("/"):
            is_folder = True
            name = name.rstrip("/")
        else:
            is_folder = False
        
        while stack and stack[-1][0] >= level + 1:
            stack.pop()
        parent = stack[-1][1] if stack else tree[root]
        if is_folder:
            parent[name] = {}
            stack.append((level + 1, parent[name]))
        else:
            parent[name] = None
    return tree

def build_actual_tree(folder):
    """
    Walk through the given folder and build a nested dictionary structure.
    Folder keys are stored as folder names (without trailing '/').
    Files are stored as keys with a value of None.
    
    If the folder does not exist, a warning is printed and an empty dictionary is returned,
    so that the diff will report all baseline items as missing.
    """
    if not os.path.exists(folder):
        print(f"Warning: Folder '{folder}' does not exist. Treating it as empty.")
        return {}
    
    tree = {}
    for root, dirs, files in os.walk(folder):
        rel_path = os.path.relpath(root, folder)
        if rel_path == ".":
            current_node = tree
        else:
            parts = rel_path.split(os.sep)
            current_node = tree
            for part in parts:
                current_node = current_node.setdefault(part, {})
        for d in sorted(dirs):
            current_node[d] = {}
        for f in sorted(files):
            current_node[f] = None
    folder_name = os.path.basename(os.path.abspath(folder))
    return {folder_name: tree}

def create_structure(structure, target_path, create_files=True):
    """
    Recursively create the folder (and optionally file) structure under target_path.
    
    Parameters:
      structure: nested dict representing the folder/file structure.
      target_path: root directory where the structure will be created.
      create_files: if True, create empty files for items whose value is None.
                    If False, only create directories.
    """
    for name, content in structure.items():
        current_path = os.path.join(target_path, name)
        if isinstance(content, dict):
            # Create folder if it doesn't exist.
            os.makedirs(current_path, exist_ok=True)
            # Recursively create sub-structure.
            create_structure(content, current_path, create_files)
        else:
            # content is None so it is a file.
            if create_files:
                # Ensure the parent folder exists.
                os.makedirs(target_path, exist_ok=True)
                # Create an empty file if it doesn't exist.
                if not os.path.exists(current_path):
                    open(current_path, 'w').close()

def main():
    parser = argparse.ArgumentParser(
        description="Replicate folder structure from a baseline.txt file in a target location."
    )
    parser.add_argument("--baseline", required=True,
                        help="Path to the baseline.txt file (tree output).")
    parser.add_argument("--location", required=True,
                        help="Target location in which to create the structure.")
    parser.add_argument("--folders-only", action="store_true",
                        help="If specified, only create folders (no files).")
    args = parser.parse_args()
    
    # Read baseline.txt
    try:
        with open(args.baseline, "r", encoding="utf-8") as f:
            baseline_text = f.read()
    except Exception as e:
        print(f"Error reading baseline file: {e}")
        return
    
    # Determine the baseline structure.
    if os.path.isfile(args.baseline):
        try:
            with open(args.baseline, "r", encoding="utf-8") as f:
                baseline_text = f.read()
            structure = parse_tree(baseline_text)
        except Exception as e:
            print(f"Error reading baseline file: {e}")
            return
    elif os.path.isdir(args.baseline):
        structure = build_actual_tree(args.baseline)
    else:
        print("Error: Baseline argument must be a valid file or folder path.")
        return
    
    create_files = not args.folders_only
    
    
    # The parsed structure includes the root folder as key.
    # We will create its contents under the target location.
    # For example, if the baseline root is "color-finder-api" and 
    # the location is "C:\Projects", then the folder will be created as "C:\Projects\color-finder-api".
    create_files = not args.folders_only
    
    try:
        create_structure(structure, args.location, create_files)
        print("Structure creation completed successfully.")
    except Exception as e:
        print(f"Error during structure creation: {e}")

if __name__ == "__main__":
    main()
