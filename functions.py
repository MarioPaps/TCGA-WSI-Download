import pandas as pd
import csv
import os
import re
import subprocess
import shutil


def process_clinical_info_csv(clinical_info_path:str):
    
    clinical_pd= pd.read_csv(clinical_info_path)
    unique_patients= clinical_pd["case_submitter_id"].unique().tolist()
    
    return unique_patients

def isolate_files(disease_manifest_path: str, file_extension: str = '.svs'):
    
    disease_manifest_pd= pd.read_csv(disease_manifest_path)
    disease_manifest_pd= disease_manifest_pd[disease_manifest_pd["filename"].str.endswith(file_extension)]
    
    return disease_manifest_pd

def obtain_DX1_files(disease_manifest_pd:pd.DataFrame):
    
    disease_manifest_pd=disease_manifest_pd[disease_manifest_pd["filename"].str.contains('DX1')]
    
    return disease_manifest_pd

def extract_tcga_code(filename):
    match = re.match(r'(TCGA-\w{2}-\w{4})', filename)
    if match:
        return match.group(1)
    return None

def identify_DX1_and_non_DX1_patients(DX1_pd:pd.DataFrame, unique_patients:list):
    
    
    DX1_patients= DX1_pd["filename"].tolist()
    DX1_patients= [extract_tcga_code(file) for file in DX1_patients]
    non_DX1_patients= list(set(unique_patients)-set(DX1_patients))
    
    
    return DX1_patients, non_DX1_patients
    
    
def slides_for_non_DX1_patients(disease_manifest_pd:pd.DataFrame, non_DX1_patients:list):
    
    non_DX1_patients_with_DX=[]
    non_DX1_patients_without_DX=[]
    
    for patient in non_DX1_patients:
        
        temp_pd=disease_manifest_pd[disease_manifest_pd["filename"].str.contains(patient)]
        mask_pd= temp_pd[temp_pd["filename"].str.contains("DX")]
        
        if mask_pd.empty:
            non_DX1_patients_without_DX.append(patient)
        else:
            non_DX1_patients_with_DX.append(patient)
    
    return non_DX1_patients_with_DX, non_DX1_patients_without_DX
    
def check_downloaded_patients(path_to_check:str, DX1_pd: pd.DataFrame):
    
    '''Check if we have already downloaded some of the relevant files and exclude them from DX1_pd'''
    all_files= os.listdir(path_to_check)
    svs_files = list(filter(lambda x: x.endswith('.svs'), all_files))
    DX1_files= DX1_pd["filename"].tolist()
    remaining_files= list(set(DX1_files)-set(svs_files))
    remaining_pd= DX1_pd[DX1_pd["filename"].isin(remaining_files)]
    
    return remaining_pd

def download_files(download_pd: pd.DataFrame):
    
    success_ids=[]
    failed_ids=[]
    
    if download_pd.empty:
        return success_ids,failed_ids
    
    for index, row in download_pd.iterrows():
        temp=row["id"]
        command = ['gdc-client', 'download', temp]
        #print(command)
        
        try:
            # Run the command
            subprocess.run(command, check=True)
            success_ids.append(temp)
            
        except subprocess.CalledProcessError as e:
            failed_ids.append(temp)
    
    return success_ids,failed_ids

def copy_downloads_to_folder(source_path:str, dest_path:str):
   
   if os.path.isdir(source_path) and os.path.isdir(dest_path):
       svs_folders= [f for f in os.listdir(source_path) if os.path.isdir(os.path.join(source_path,f))]
       path_svs_folders=[os.path.join(source_path,f) for f in svs_folders]
       
       for folder in path_svs_folders:
           file_name=[f for f in os.listdir(folder) if f.endswith('.svs')]
           
           if len(file_name)>0:
               complete_src_path= os.path.join(folder,file_name[0])
               shutil.move(complete_src_path, dest_path)
      
   return None