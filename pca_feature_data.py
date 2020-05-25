import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

def pca_lymph():
    #read in the feature data from csv
    feature_data_path = "C:\\Users\\kb48\\Downloads\LymphNodeProject\\example_radiomics_features.csv"
    data = pd.read_csv(feature_data_path)
    data = data.to_numpy()
    filenames = data[:,0]
    data = data[:,1:]
    
    #standardize the data
    data = StandardScaler().fit_transform(data)
    pca = PCA(.95)
    principalComponents = pca.fit_transform(data)

    #get label data
    pos_neg_data =  pd.ExcelFile("C:\\Users\\kb48\\Downloads\\LymphNodeProject\\info_about_lymph_node_cases.xlsx")
    labels_sheet = pd.read_excel(pos_neg_data,'anon_LN status key')
    patient_filenames = labels_sheet['anomMRN'].tolist()
    patient_classifications = labels_sheet['LN_status'].tolist()
    for i in range(len(patient_classifications)):
    
        if patient_classifications[i] == 'N+':
            patient_classifications[i] = 1
        else:
            patient_classifications[i] = 0
    binary_labels = []
    for i in range(len(filenames)):
        patient_filename_split = filenames[i].split('_')
        
        
        pid_str = patient_filename_split[-1]
        
        pid_nums = pid_str[-8] + pid_str[-7] + pid_str[-6]
        
        match_pid = [x for x in patient_filenames if pid_nums in x]
        matching_indx = patient_filenames.index(match_pid[0])
        binary_labels.append(patient_classifications[matching_indx])
    
    #split data into train and test
    split = 0.25
    train_data, test_data, train_lbl, test_lbl = train_test_split( principalComponents,
        binary_labels, test_size=split, random_state=0)

    svclassifier = SVC(kernel='rbf')
    svclassifier.fit(train_data, train_lbl)
    test_pred = svclassifier.predict(test_data)
    print(confusion_matrix(test_lbl,test_pred))
    print(classification_report(test_lbl,test_pred))
    
    
    
def main():
    pca_lymph()
main()