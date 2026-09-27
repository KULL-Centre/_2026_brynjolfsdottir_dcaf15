import subprocess
import shutil
from pathlib import Path

# Main directories
#main_dirs = [Path(d) for d in ["pos2", "pos4", "pos6", "pos8", "pos10", "pos12", "pos14", "pos16","base"]]
main_dirs = [Path(d) for d in ["p1","p2", "p3", "p4"]]

# Replica count
num_replicas = 10

for main_dir in main_dirs:
    print(f"Processing {main_dir} ...")
    
    # Find what to copy
    py_files = list(main_dir.glob("*.py"))
    input_folder = main_dir / "input"

    for i in range(1, num_replicas + 1):
        replica_dir = main_dir / str(i)
        replica_dir.mkdir(exist_ok=True)

        # Copy .py files
        for py_file in py_files:
            shutil.copy2(py_file, replica_dir / py_file.name)

        # Copy input folder
        dest_input = replica_dir / "input"
        if dest_input.exists():
            shutil.rmtree(dest_input)
        shutil.copytree(input_folder, dest_input)

        # Check for succesful simulation
        mappresent = replica_dir / "data/asyn_dcaf15_asyn_dcaf15_cmap.npy"
        print(mappresent)
        if mappresent.exists():
            continue
        else:
            # Run commands
            print(f"Running prepare.py in {replica_dir}, followed by submit.py")
            subprocess.run(
                ["python", "prepare.py", "--name_1", "asyn", "--name_2", "dcaf15"],
                cwd=replica_dir,
                check=True
            )
            subprocess.run(
                ["python", "submit.py", "asyn", "dcaf15", str(i)],
                cwd=replica_dir,
                check=True
            )

print("All replicas created and jobs submitted.")

