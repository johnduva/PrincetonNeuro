#!/bin/bash
#SBATCH --time=5:59:00
#SBATCH --mem=16000
#SBATCH -N 1
#SBATCH --cpus-per-task=8
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-socket=1
#SBATCH --gres=gpu:1
#SBATCH --output='/tigress/jduva/logs/track.%j.log'

VIDEO_PATH="$1"

module load anaconda
module load cudnn/cuda-10.1/7.5.0

conda activate /home/jduva/.conda/envs/sleap_env2

export HDF5_PLUGIN_PATH=/tigress/jduva/HDF5/plugins

sleap-track "$VIDEO_PATH" --video.dataset pg0 --video.input_format channels_first --tracking.tracker flow --match greedy -m 200110_145852.UNet.centroids/ -m 200110_135225.UNet.topdown_confidence_maps/


