#!/bin/sh

#SBATCH --job-name=zipFiles    # create a short name for your job
#SBATCH --time=24:00:00          # total run time limit (HH:MM:SS)

echo Started running...

module load anacondapy/5.1.0
python zipFiles.py

echo Done.
