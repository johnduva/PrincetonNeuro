# This script automatically deletes predictions with scores below 10%.
# It also names each track after the uploaded file, but may need to be altered based on circumstances (lines 36-37).

from sleap import Labels
import sys

SCORE_THRESHOLD = .1

filename = sys.argv[1]
out_filename = str(filename)+'_highscores_trackName.h5'

labels = Labels.load_file(filename)

lf_inst_list = []

# Find the (frame, instance) pairs with score below threshold
for frame in labels:
    for instance in frame:
        if hasattr(instance, "score"):
            if instance.score is not None:
                if instance.score < SCORE_THRESHOLD:
                    lf_inst_list.append((frame, instance))

if lf_inst_list:

    print(f"Removing {len(lf_inst_list)} instances...")

    # Remove each of the instances
    for frame, instance in lf_inst_list:
        labels.remove_instance(frame, instance, in_transaction=True)

else:
    print("No instances to remove.")

# Save track as filename
print("Saving track as " + str(filename[0:11]))
labels.tracks[0].name = filename[0:11]

# Save the updated project file
Labels.save_file(labels, out_filename)
print(out_filename)




