import subprocess
import argparse
from jinja2 import Template

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Submit a Slurm job for a CALVADOS simulation.")
parser.add_argument("protein1", type=str, help="Name of the first protein (e.g., asyn)")
parser.add_argument("protein2", type=str, help="Name of the second protein (e.g., dcaf15)")
parser.add_argument("replica", type=int, help="Replica number")
args = parser.parse_args()

# Build system name and path
system_name = f"{args.protein1}_{args.protein2}"

# Define job script template
submission = Template("""#!/bin/sh
#SBATCH --job-name={{ system }}_{{ replica }}
#SBATCH --nodes=1
#SBATCH --cpus-per-task=2
#SBATCH --partition=sbinlab_ib2
#SBATCH --mem=8GB
#SBATCH -t 32:00:00
#SBATCH -o {{ system }}/out
#SBATCH -e {{ system }}/err

# Load conda (edit to point at your own conda installation)
source ~/.bashrc
conda activate dcaf

python {{ system }}/run.py --path {{ system }}
""")

# Generate submission script
script_name = f"{system_name}_{args.replica}.sh"
script_content = submission.render(system=system_name, replica=args.replica)

with open(script_name, "w") as submit:
    submit.write(script_content)

# Submit the job
subprocess.run(["sbatch", script_name])
print(f"Submitted {script_name} for system {system_name}, replica {args.replica}")

