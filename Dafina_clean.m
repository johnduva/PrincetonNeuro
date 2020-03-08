clc; clear;
disp('Running...');
load('body_part_labels.mat')
load('frame_idx.mat')
load('movie_observational_learning_labels.trk', '-mat');
labeled = find(~isnan(bp_labels.nose(:,1)));
intersect = intersect(frame_idx',labeled);
fields = fieldnames(bp_labels);

for bodyPart=1:length(fields)   %len = 4 (nose, head, centroid, tail)
    for frame=1:length(bp_labels.(fields{bodyPart}))
        for j=1:2

            if ~ismember(frame,intersect)
                bp_labels.(fields{bodyPart})(frame,j) = NaN;
            end
            
            pTrk(bodyPart,j,frame) =  bp_labels.(fields{bodyPart})(frame,j);
            test = fliplr(pTrk);
            
        end
    end
end
pTrk = test;

clear bodyPart; clear bp_labels; clear fields; clear frame; 
clear frame_idx; clear intersect; clear j; clear labeled; clear test;
save('duva_track.trk');

disp("Finished running.");