# lymph_node_project

1. Run norm.py first. Files resulting will have filename 'norm_...." and be stored in Segmentations folder.
2. Run crop_around_roi.m in Matlab. Couldn't figure out how to crop around a region of interest in python so I did this in Matlab. The function will avoid files that have volumes with no pixel information (blank volumes). It will rename files to cropped_..." and store them in the Segmentations folder. This function will also take all the data and set it to have mean of zero and unit variance. It will save the data with files starting with "zscore_...".
3. Last part is is importing the images and running the model. This is done with the file "lymph_node_model_3D.py". It will look for files that start with "zscore" in the Segmentations directory. It will get the label information from the excel spreadsheet. 

