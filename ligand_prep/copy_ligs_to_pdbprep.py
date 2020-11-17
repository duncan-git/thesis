import os,sys
import shutil

# Run from within ligand prep folder to copy all files ending with 0001.pdb (i.e. generated from
# molfile_to_params.py) into pdb_prep/ligs folder

# also copy params and rotlibs to production folder
cwd=os.getcwd()
parent_cwd=os.path.abspath(os.path.join(cwd,'..'))

for folder in os.listdir('.'):
    if os.path.isdir(folder):
        os.chdir(folder)
        for file in os.listdir('.'):
            if file.endswith('.params') or file.endswith('.rotlib.pdb'):
                if file not in (parent_cwd+'/production/ligs'):
                    shutil.copy(file,parent_cwd+'/production/ligs')
            if file.endswith('0001.pdb'):
                if file not in (parent_cwd+'/pdb_prep/ligs'):
                    shutil.copy(file,parent_cwd+'/pdb_prep/ligs')
        os.chdir(cwd)
