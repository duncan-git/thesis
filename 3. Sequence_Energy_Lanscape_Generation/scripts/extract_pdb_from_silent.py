#!/usr/bin/python

# This script should read the scores from a Rosetta silent file and output
# the best three total score to a "tags" file for extraction

import sys,os
from natsort import realsorted,ns

label_bool=0
labels=[]
score_pos=0
description_pos=0
regex='RA95_CSR'
all_scores=[]
current_structure=''
parent_directory='/cluster/home/duncanm/Cyclohexanone/190109_cluster_silent/'

## Start by working on silent file to extract best three total_scores with descriptions
silent_bool=0
silent_count=0

tags=open('103_D_CSR_tags.sh','w')
scores=open('103_D_CSR.scores','w')

for file in os.listdir('.'):
	if file.endswith('.silent'):
		silent_bool=1
	
		current_structure=os.getcwd().split('/')[-1]
		
		file_handle=current_structure
		
		with open(file) as read_silent:
			for line in read_silent:
				if line.startswith("SCORE:") and label_bool == 0:
					label_bool=1
					labels=line.strip().split()			
					for i,element in enumerate(labels):
						scores.write(element+'\t')
						if element == 'score':
							score_pos=i
						if element == 'description':
							description_pos=i
			
					scores.write('\n')
		
				if line.startswith("SCORE:") and regex in line:
					silent_count+=1
					all_scores.append([line.strip().split()[score_pos],file,line.strip().split()[description_pos]])
			
sorted_total_pose=realsorted(all_scores, key=lambda x: x[0])

if silent_count > 2:
	for k in range(3):
		scores.write(element[0]+'\t')
		tags.write('$ROSETTA/bin/extract_pdbs.hdf5.linuxgccrelease -extra_res_fa ../../ligs/LYM.params -extra_res_fa ../../ligs/CSR.params -in:file:silent '+sorted_total_pose[k][1]+' -in:file:tags '+sorted_total_pose[k][2]+'\n')

		scores.write('\n')
	
tags.close()
scores.close()

# Within shell, source the newly generated .tags file to extract three pdbs

# for file in os.listdir('.'):
# 	if file.endswith('.sh'):
# 		cmd='source '+os.getcwd()+'/'+file
# 		os.system(cmd)		
# # 	if file.endswith('.scores'):
# # 		shutil.move(file,parent_directory+'/output/'+current_structure+'/'+file)
# 
# # reporter to check three pdbs are generated
# 
# check_pdb=0
# print(current_structure)
# for file in os.listdir('.'):
# 	if file.endswith('.pdb'):
# 		check_pdb+=1
# 		
# 		pdb_handle=file.split('.')[0]
# 		pdb_num=pdb_handle.split('_')[2]
# 		file_name=current_structure+'_'+pdb_num+'.pdb'
# 		
# #		shutil.move(file,parent_directory+'/output/'+current_structure+'/'+file_name)
# if check_pdb != 3 or silent_bool == 0:
# 	error_log=open(parent_directory+'python_log.txt','a+')
# 	if silent_bool == 0:
# 		error_log.write('######### Missing SILENT_FILE from directory: '+os.getcwd().split('/')[-1]+' ###############\n')		
# 	elif check_pdb != 3:
# 		error_log.write('Missing pdbs from directory: '+os.getcwd().split('/')[-1]+'... PDBs reported:'+str(check_pdb)+'\n')
# 	
# error_log.close()		
		
					
		
			
	