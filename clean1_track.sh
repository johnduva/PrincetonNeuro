#!/bin/bash
#SBATCH --time=5:59:00
#SBATCH --mem=16000
#SBATCH -N 1
#SBATCH --cpus-per-task=8
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-socket=1
#SBATCH --gres=gpu:1
#SBATCH --output='/tigress/jduva/logs/track.%j.log'

# This script will typically be called within a bash loop such as:
# for video in OFT*; do python clean1_track.sh $video; done;
# Remember to update the paths below accordingly - and to set the proper number of animals.

# To save time and karma, usage on the head node of TigerGPU will usually not get you in trouble.
# Just run python -m sleap.info.trackcleaner <path> -c 1

VIDEO_PATH="$1"

module load anaconda
module load cudnn/cuda-10.1/7.5.0

conda activate /home/jduva/.conda/envs/sleap_env2

export HDF5_PLUGIN_PATH=/tigress/jduva/HDF5/plugins

numAnimals = 1
python -m sleap.info.trackcleaner "$VIDEO_PATH" -c numAnimals

