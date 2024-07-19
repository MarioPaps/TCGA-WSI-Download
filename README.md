# TCGA-WSI-Download

Managing Whole Slide Images (WSIs) can be challenging for individuals who have just begun to engage with the field. This Python utility aims to help users efficiently download WSIs from the TCGA database. The user simply needs to locate the clinical and manifest files of the TCGA project of interest and save them into CSV format. 

## Possible issues
- The tool has only been tested on Windows at the moment. Testing on Mac and Linux is part of future work.
- Some TCGA downloads break, leading to 'svs.partial' files. This is because of a conflict between GDC client and Anaconda. Hence, you are advised to run the code in a simple pip environment that does not require Anaconda. The tool keeps track of file IDs of both successful and unsuccessful downloads. Therefore, you could save the IDs of failed downloads to a .txt file and try downloading them on another computer.

