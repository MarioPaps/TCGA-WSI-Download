import pandas as pd
import csv
import os
import re
import subprocess
import shutil
from functions import process_clinical_info_csv, isolate_files, obtain_DX1_files, extract_tcga_code, identify_DX1_and_non_DX1_patients
from functions import slides_for_non_DX1_patients, check_downloaded_patients, download_files, copy_downloads_to_folder

   
if __name__=="__main__":
    
    clinical_info_path='lusc_clinical.csv'
    unique_patients= process_clinical_info_csv(clinical_info_path)
    
    disease_manifest_path= 'LUSCManifestFile.csv'
    disease_manifest_pd= isolate_files(disease_manifest_path,'.svs')
    
    DX1_pd= obtain_DX1_files(disease_manifest_pd)
    DX1_patients, non_DX1_patients = identify_DX1_and_non_DX1_patients(DX1_pd, unique_patients)
    
    non_DX1_patients_with_DX, non_DX1_patients_without_DX= slides_for_non_DX1_patients(disease_manifest_pd, non_DX1_patients)
    
    path_to_check=r'F:\lusc_svs'
    remaining_pd= check_downloaded_patients(path_to_check, DX1_pd)
    success_ids,failed_ids= download_files(download_pd=remaining_pd)
    
    source_path=r'F:\newer_day'
    dest_path=r'F:\lusc_svs'
    
    copy_downloads_to_folder(source_path,dest_path)
    

    