
addpath Segmentations
addpath nrrd_read_write_rensonnet/nrrd_read_write_rensonnet

%figure out the best crop size
%its 60,60,12
segs_dir = 'C:\Users\kb48\Downloads\LymphNodeProject\Segmentations';
seg_files = dir(fullfile(segs_dir,'normed*'));
box_size = [];
%files to avoid are files that are all of the same pixel intensity.
files_to_avoid = [];
files_to_avoid = load('files_to_avoid.mat','files_to_avoid');
files_to_avoid = files_to_avoid.files_to_avoid;
all_images_to_normalize = [];
num_imgs = 0;
count = 0;
for i = 1:size(seg_files,1)
   
    
    if ~ismember(i,files_to_avoid)
        count = count + 1;
        num_imgs = num_imgs + 1;
        headerInfo = nhdr_nrrd_read(seg_files(i).name, 1);
        X= headerInfo.data;
        
        reshaped_img = reshape(X,size(X,1)*size(X,2)*size(X,3),1);
        static_bkgrd_indx = find(reshaped_img == reshaped_img(1));
        make_binary = ones(size(X,1)*size(X,2)*size(X,3),1);
        make_binary(static_bkgrd_indx) = 0;
        not_eq_zero = find(make_binary ~= 0);
        make_binary(not_eq_zero) = 1;
        lymphs_three_d = reshape(make_binary,size(X,1),size(X,2),size(X,3));
        stats = regionprops3(lymphs_three_d);
    %next we are going to use the centroid of the relevant files to create
    %a box around the ROI and crop
        center = round(stats.Centroid);
        bounding_box = stats.BoundingBox;
        bounding_box = bounding_box+1;
        %round the bounding box numbers to even numbers
        if mod(bounding_box(4),2) ~= 0
            bounding_box(4) = bounding_box(4) + 1;
        end
        if mod(bounding_box(5),2) ~=0
            bounding_box(5) = bounding_box(5) + 1;
        end
        if mod(bounding_box(6),2) ~= 0
            bounding_box(6) = bounding_box(6) + 1;
        end
       
       
        
        %bounding box needed to be even number to find the voxel id of the
        %left most bounding box corner.
        c1_x = center(1) - bounding_box(4)/2;
        c1_y = center(2) - bounding_box(5)/2;
        c1_z = center(3) - bounding_box(6)/2;
     
        
        if c1_x <= 0
            c1_x = 1;
            
        end
        if c1_y <= 0
            c1_y = 1;
            
        end
        if c1_z <= 0
            c1_z = 1;
            
        end
        
        
        vout = imcrop3(X,[c1_x c1_y c1_z bounding_box(4) bounding_box(5) bounding_box(6)]);
        %the mask is only used for radiomics.
        %vout_mask = imcrop3(lymphs_three_d,[c1_x c1_y c1_z bounding_box(4) bounding_box(5) bounding_box(6)]);

        vout = imresize3(vout,[60 60 12]); 
        
        %mask used for radiomics
        %vout_mask = imresize3(vout_mask, [60 60 12]);
        %vout_mask = imbinarize(vout_mask);
        
        headerInfo.sizes = size(vout);
        headerInfo.data = vout;
        reshaped_vout = reshape(vout,size(vout,1)*size(vout,2)*size(vout,3),1);
        all_images_to_normalize = [all_images_to_normalize; reshaped_vout];
        %calls to write file for mask are for radiomics
        %headerInfo_mask = headerInfo;
        %headerInfo_mask.data = double(vout_mask);
        
        
        headerInfo = nhdr_nrrd_write("C:\Users\kb48\Downloads/LymphNodeProject\Segmentations\cropped_" + seg_files(i).name, headerInfo, 1);
        %writing binary mask to file for use with pyradiomics
        headerInfo_mask = nhdr_nrrd_write("C:\Users\kb48\Downloads/LymphNodeProject\Segmentations\cropped_mask_" + seg_files(i).name, headerInfo_mask, 1);
        
    else
        dummy_img = zeros(60*60*12,1);
        all_images_to_normalize = [all_images_to_normalize; dummy_img];
    end
    
end

%this is the code to set the zero mean and unit variance

all_imgs_zscore = zscore(all_images_to_normalize);
all_imgs_back_to_three_d = reshape(all_imgs_zscore,60,60,12,size(seg_files,1));
for i = 1:size(seg_files,1)
    if ~ismember(i,files_to_avoid)
        
        headerInfo = nhdr_nrrd_read(seg_files(i).name, 1);
        headerInfo.data = all_imgs_back_to_three_d(:,:,:,i);
        headerInfo.sizes = [size(all_imgs_back_to_three_d,1) size(all_imgs_back_to_three_d,2) size(all_imgs_back_to_three_d,3)];
        ok = nhdr_nrrd_write("C:\Users\kb48\Downloads\LymphNodeProject\Segmentations\zscore_cropped_" + seg_files(i).name, headerInfo ,1); 
    end
end

    
