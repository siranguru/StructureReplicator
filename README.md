# StructureReplicator

**StructureReplicator** is a command‑line Python utility that replicates a folder and file structure at a target location based on a baseline input. The baseline source can be provided either as a tree‑formatted text file (for example, generated using `tree /F`) or as a folder path [Input examples given below]. You can choose to replicate both folders and empty files or only the folder structure.

**Latest application:** AI/LLM generated file structure or generative AI based file structure (see sample input data below) can be stored as baseline.txt (or used as a folder) and replicated to any target location in your system.

## Key Features

- **Flexible Baseline Input:**  
  Supply the baseline as a tree‑formatted text file or as a folder.

- **Complete Structure Replication:**  
  Recreates the entire directory hierarchy in a specified target location.

- **Folders‑Only Option:**  
  Optionally replicate only the folder structure without creating any files.

- **Simple & Efficient:**  
  Easily mirror a predefined file system to a new location.

## Input Explanation

StructureReplicator accepts one of the following as the baseline input:

1. **Tree‑Formatted Text File:**  
   A plain text file that displays the directory structure in a tree‑like format. This file is typically generated by running the `tree /F` command on Windows or a similar command on other systems.  
    **Sample Input:**  
    ```plaintext
    /project-sample/
    ├── src/
    │   ├── main/
    │   │   ├── app.py
    │   │   └── config.yaml
    │   ├── utils/
    │   │   ├── helpers.py
    │   │   └── logger.py
    │   └── controllers/
    │       ├── user_controller.py
    │       └── auth_controller.py
    ├── docs/
    │   ├── README.md
    │   └── CHANGELOG.md
    ├── tests/
    │   ├── test_app.py
    │   └── test_utils.py
    └── setup.py

2. **Folder Path:**  
   You can also provide a folder path as the baseline input. In this case, the tool will scan the given folder and build its structure using `os.walk` in the same way as it does for the target location.

## Output Example

After replicating the structure to the target location, the tool will create a directory tree that mirrors the baseline.  
    **Sample Output:**
    
    project-sample
    ├── src
    │   ├── main
    │   │   ├── app.py     (empty file)
    │   │   └── config.yaml  (empty file)
    │   ├── utils
    │   │   ├── helpers.py  (empty file)
    │   │   └── logger.py   (empty file)
    │   └── controllers
    │       ├── user_controller.py  (empty file)
    │       └── auth_controller.py  (empty file)
    ├── docs
    │   ├── README.md      (empty file)
    │   └── CHANGELOG.md   (empty file)
    ├── tests
    │   ├── test_app.py    (empty file)
    │   └── test_utils.py  (empty file)
    └── setup.py         (empty file)

*Note:* When using the `--folders-only` option, only the directories are created and no files are generated.

## How It Works

1. **Baseline Parsing:**  
   - If a tree‑formatted text file is provided, the tool parses the text into a nested dictionary where folders are keys with dictionary values and files are keys with a value of `None`.
   - If a folder path is provided, the tool builds the nested dictionary structure using `os.walk`.

2. **Structure Replication:**  
   The tool traverses the nested dictionary and creates the corresponding directories in the target location using `os.makedirs`.

3. **File Creation Option:**  
   If the `--folders-only` flag is not set, empty files are also created for items represented as files in the baseline.

4. **Error Handling:**  
   The tool prints warnings if the baseline or target paths are not found and handles errors gracefully.

## Requirements

- Python 3.x

## Running the Script
- Replace the baseline input (text file or folder) with your desired directory structure.
- Specify the target location where the structure will be created.
- Use the --folders-only flag if you wish to create only folders.

- Open the Command prompt/terminal and go to the the location where the file `create_structure.py` is located using 

 `cd C:\Path\to\create_structure.py`.
  - When the baseline is a text file (baseline.txt):
##
    python create_structure.py --baseline "C:\Path\to\baseline.txt" --location "C:\Target\Location"

  - When the baseline is a folder:
##
    python create_structure.py --baseline "C:\Path\to\baseline_folder" --location "C:\Target\Location"

  - To replicate folders only:
##
    python create_structure.py --baseline "C:\Path\to\baseline.txt" --location "C:\Target\Location" --folders-only




## Troubleshooting

- **Paths with Spaces:**  
  Enclose file and folder paths in quotes.
- **Permissions:**  
  Ensure you have the necessary permissions to create files and directories at the target location.

## License

This project is licensed under the MIT License.
