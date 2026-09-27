import shutil
from pathlib import Path

# Directories
source = Path("s50phospho")
targets = [Path(d) for d in ["pos2", "pos4", "pos6", "pos8", "pos10", "pos12", "pos14", "n75_trunc"]]

# Get all .py files and the input folder
py_files = list(source.glob("*.py"))
input_folder = source / "input"

for target in targets:
    target.mkdir(exist_ok=True)

    # Copy .py files
    for py_file in py_files:
        dest = target / py_file.name
        shutil.copy2(py_file, dest)
        print(f"Copied {py_file.name} → {target}")

    # Copy input folder
    dest_input = target / "input"
    if dest_input.exists():
        shutil.rmtree(dest_input)
    shutil.copytree(input_folder, dest_input, ignore=shutil.ignore_patterns('dcaf15.pdb'))
    print(f"Copied input folder → {target}/input")
