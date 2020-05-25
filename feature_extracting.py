#feature extracting algorithm

import os
import numpy as np
import csv
from radiomics import featureextractor

data_dir = "C:\\Users\\kb48\\Downloads\\LymphNodeProject\\Segmentations\\"
def feature_extraction():
    #go through all the original images and the masks
    #match up the images and masks
    image_path = "C:\\Users\\kb48\\Downloads\\LymphNodeProject\\Segmentations\\cropped_resized_3d_images\\"
    mask_path = "C:\\Users\\kb48\\Downloads\\LymphNodeProject\\Segmentations\\cropped_3d_mask_images\\"
    output_file_path = "C:\\Users\\kb48\\Downloads\LymphNodeProject\\example_radiomics_features.csv"
    #iterate through all the images in the directories.
    
    filenames = []
    patient_id = []
    for filename in os.listdir(image_path):
        filenames.append(image_path + filename)
        patient_id.append(filename)
    count = 0
    for mask in os.listdir(mask_path):
        filenames[count] = [filenames[count], mask_path + mask]
        count = count + 1
   
    #for filename_mask in os.listdir(mask_path):
    #    print(filename_mask)
    
    extractor = featureextractor.RadiomicsFeatureExtractor()
    params = {}
    params['binWidth'] = 20
    params['sigma'] = [1, 2, 3]
    params['verbose'] = True
    
    extractor = featureextractor.RadiomicsFeatureExtractor(**params)
    results = []
    print("Enabled features:\n\t", extractor.enabledFeatures)
    for i in range(len(filenames)):
        result = extractor.execute(filenames[i][0], filenames[i][1])
        results.append(result)
    
    #print("    features:")
    '''
    for key,value in result.items():
        
        if isinstance(value, np.ndarray):
            print(value.shape)
            print("\t", key, ":", value[0])
    #ndarray - float64    
    '''
    
            
    
    headers = None
    with open(output_file_path, 'a') as outputFile:
        writer = csv.writer(outputFile, lineterminator='\n')
        if headers is None:
            headers = list(results[0].keys())
            headers.insert(0,'filename')
            writer.writerow(headers)
            for i in range(len(results)):
                #headers = list(results[i].keys())
            #writer.writerow(headers)
                
                headers_values = list(results[i].values())
                headers_values.insert(0, patient_id[i])
                writer.writerow(headers_values)
                #for i in range(len(headers)):
                #    writer.writerow([headers[i], headers_values[i]])
    
    
        '''
        row = []
        for h in headers:
            row.append(result.get(h,"N/A"))
            row = result.get(h,"N/A"))
            writer.writerow(row)
        writer.writerow(row)
        '''  
    

def main():
    feature_extraction()
    
main()