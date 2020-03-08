# Convert labels from 'Body Part Labeler' software into 'Animal Part Tracker' format.

# 1) Import incorrect .trk (labels) file from BPL, as well as a .mat file which provides a skeleton for the proper formatting.
# 2) Create three different loops to cycle through each bodyPart, frame, and x/y coordinate.
# 3) Each iteration will set either an x or y coordinate into the proper format.
# 4) Make sure that we only leave the variables that we want to save into the new trk file - then save it. 

clc; clear;
disp("Running...")
load('movie_observational_learning_labels.trk', '-mat');
load('body_part_labels.mat')

fields = fieldnames(bp_labels);
for bodyPart=1:length(fields) %len = 4 (nose, head, centroid, tail)
    for frame=1:length(bp_labels.(fields{bodyPart})) % == bp_labels.nose = 25,629 frames
        for xORyCoord=1:2 % x coordinate, then y coordinate
            pTrk(bodyPart,xORyCoord,frame) =  bp_labels.(fields{bodyPart})(frame,xORyCoord); %#ok<SAGROW>
            test = fliplr(pTrk); 
        end
    end
end

pTrk = test;
clear fields; clear bp_labels; clear frame; clear xORyCoord; clear bodyPart; clear test;
save('duva_track.trk')
%clear;
disp("Finished running at:");
disp(datetime('now'));
