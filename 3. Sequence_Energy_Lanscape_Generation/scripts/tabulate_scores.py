#!/usr/bin/python

# This script will be used to extract the top three scores from pdb files (already extracted from silent files)
# then output the results to HRF - both a raw and a subtracted from native table

# run from within 'run' directory

import os,sys
import numpy as np

native_ids=[('1','M'),('2','P'),('3','R'),('4','Y'),('5','L'),('6','K'),('7','G'),('8','W'),
('9','L'),('10','E'),('11','D'),('12','V'),('13','V'),('14','Q'),('15','L'),('16','S'),('17','L'),
('18','R'),('19','R'),('20','P'),('21','S'),('22','V'),('23','H'),('24','A'),('25','S'),('26','R'),
('27','Q'),('28','R'),('29','P'),('30','I'),('31','I'),('32','S'),('33','L'),('34','N'),('35','E'),
('36','R'),('37','I'),('38','L'),('39','E'),('40','F'),('41','N'),('42','K'),('43','R'),('44','N'),
('45','I'),('46','T'),('47','A'),('48','I'),('49','I'),('50','A'),('51','Y'),('52','Y'),('53','L'),
('54','R'),('55','K'),('56','S'),('57','P'),('58','S'),('59','G'),('60','L'),('61','D'),('62','V'),
('63','E'),('64','R'),('65','D'),('66','P'),('67','I'),('68','E'),('69','Y'),('70','A'),('71','K'),
('72','Y'),('73','M'),('74','E'),('75','P'),('76','Y'),('77','A'),('78','V'),('79','G'),('80','L'),
('81','S'),('82','I'),('83','K'),('84','T'),('85','E'),('86','E'),('87','K'),('88','Y'),('89','F'),
('90','D'),('91','G'),('92','S'),('93','Y'),('94','E'),('95','M'),('96','L'),('97','R'),('98','K'),
('99','I'),('100','A'),('101','S'),('102','S'),('103','V'),('104','S'),('105','I'),('106','P'),
('107','I'),('108','L'),('109','M'),('110','N'),('111','D'),('112','F'),('113','I'),('114','V'),
('115','K'),('116','E'),('117','S'),('118','Q'),('119','I'),('120','D'),('121','D'),('122','A'),
('123','Y'),('124','N'),('125','L'),('126','G'),('127','A'),('128','D'),('129','T'),('130','V'),
('131','L'),('132','L'),('133','I'),('134','V'),('135','E'),('136','I'),('137','L'),('138','T'),
('139','E'),('140','R'),('141','E'),('142','L'),('143','E'),('144','S'),('145','L'),('146','L'),
('147','E'),('148','Y'),('149','A'),('150','R'),('151','G'),('152','Y'),('153','G'),('154','M'),
('155','E'),('156','P'),('157','L'),('158','I'),('159','L'),('160','I'),('161','N'),('162','D'),
('163','E'),('164','N'),('165','D'),('166','L'),('167','D'),('168','I'),('169','A'),('170','L'),
('171','R'),('172','I'),('173','G'),('174','A'),('175','R'),('176','F'),('177','I'),('178','T'),
('179','I'),('180','Y'),('181','S'),('182','M'),('183','N'),('184','F'),('185','E'),('186','T'),
('187','G'),('188','E'),('189','I'),('190','N'),('191','K'),('192','E'),('193','N'),('194','Q'),
('195','R'),('196','K'),('197','L'),('198','I'),('199','S'),('200','M'),('201','I'),('202','P'),
('203','S'),('204','N'),('205','V'),('206','V'),('207','K'),('208','V'),('209','P'),('210','L'),
('211','L'),('212','D'),('213','F'),('214','F'),('215','E'),('216','P'),('217','N'),('218','E'),
('219','I'),('220','E'),('221','E'),('222','L'),('223','R'),('224','K'),('225','L'),('226','G'),
('227','V'),('228','N'),('229','A'),('230','F'),('231','M'),('232','I'),('233','S'),('234','S'),
('235','S'),('236','L'),('237','M'),('238','R'),('239','N'),('240','P'),('241','E'),('242','K'),
('243','I'),('244','K'),('245','E'),('246','L'),('247','I'),('248','E')]

############################################################################################################
# Adjust to whatever designable positions are in setup_dirs 
############################################################################################################

designable_positions = [3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,30,31,32,33,34,
35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,54,55,56,58,60,61,62,63,64,65,67,68,69,70,71,72,73,
74,76,77,78,80,81,82,84,85,86,87,88,89,90,92,93,94,95,96,97,98,99,100,101,102,103,104,105,107,108,109,111,
112,113,114,115,116,117,118,119,120,121,122,123,124,125,127,128,129,130,131,132,133,134,135,136,137,138,
139,140,141,142,143,144,145,146,147,148,149,150,152,154,155,157,158,159,160,161,162,163,164,165,166,167,168,
169,170,171,172,174,175,176,177,178,179,181,182,183,184,185,186,188,189,190,191,192,193,194,195,196,197,198,
199,200,201,203,204,205,206,207,208,210,211,212,213,214,215,217,218,219,220,221,222,223,224,225,227,228,229,
230,231,232,233,234,235,236,237,238,240,241,242,243,244,245,246,247,248]

amino_acids = ['A','V','I','L','M','F','Y','W','S','T','N','Q','R','H','K','D','E','C']
table_header = ['Position','A','V','I','L','M','F','Y','W','S','T','N','Q','R','H','K','D','E','C','Native']

############################################################################################################
############################################################################################################


raw_table=open('../output/raw_table_tabulated.txt','w')
sub_table=open('../output/sub_scores_tabulated.txt','w')
error_log=open('../output/error_log.txt','w')

expected_pdbs=3

all_scores_array=[]

for position in designable_positions:
	
	score_insert=[]
	
	##########################################################################
	### Find the wild-type residue for target position
	##########################################################################

	wild_type_residue=''
	found_position=0
	
	# Check if target position actually exists 
	
	for folder in sorted(os.listdir('.')):
		if str(position)+'_A_CSR' == folder and found_position == 0:
			score_insert.append(str(position))
			found_position=1
				
			for element in native_ids:
				if str(position) == element[0]:
					wild_type_residue=element[1]
					
	##########################################################################
	### Work through the designed amino acids, extracting the triplicate scores
	### for each one, calculating the average and appending to a master array
	##########################################################################	
	
	if found_position == 1:
		print "Working on designable position:", position
		for aa in amino_acids:
		
			score_array=[]
			target_folder=str(position)+'_'+aa+'_CSR'
			pdb_counter=0
			
			if os.path.exists(target_folder):
				print "Moving to target folder:",target_folder
				os.chdir(target_folder)
				for file in os.listdir('.'):
					if file.endswith('.pdb'):
						pdb_counter+=1
						with open(file) as read_pdb:
							for line in read_pdb:
								if line.startswith('score'):
									score_array.append(float(line.strip().split()[1]))
				
				if pdb_counter < expected_pdbs:
					print "ERROR: Found less than 3 pdbs in folder ",target_folder,". Writing to error log."
					error_log.write('Less than 3 pdbs found in folder: '+target_folder+'\n')
					score_insert.append('ERROR!')
				else:
					average_score=np.average(score_array)
					score_insert.append(average_score)			
				os.chdir('../')
				
			else:
				print "ERROR: Missing sub-folder",target_folder
				error_log.write('Missing folder: '+target_folder+'\n')
				score_insert.append('ERROR!')
		
		score_insert.append(wild_type_residue)
		all_scores_array.append(score_insert)
	else:
		print "ERROR: Missing entire directory structure for position", position
		#error_log.write('Missing entire position directory: '+str(position)+'\n')

##########################################################################
### Start writing out scores to RAW table file
##########################################################################	
				
print "Writing RAW scores to file raw_table_tabulated.txt"

for element in table_header:
	raw_table.write(element+'\t')
	sub_table.write(element+'\t')
raw_table.write('\n')
sub_table.write('\n')

for element in all_scores_array:
	for sub_element in element:
		raw_table.write(str(sub_element)+'\t')
	raw_table.write('\n')

##########################################################################
### Subtract wild-type score from each entry, then write out to SUB_SCORES
##########################################################################	

print "Calculating subtracted scores......"
for entry in all_scores_array:
	position=entry[0]
	wild_type=entry[19]
	new_insert=[]

	# Find position and value of wild-type score in array entry
	for i,element in enumerate(table_header):
		if wild_type == element:
			wild_type_array_pos=i
	wild_type_score=entry[wild_type_array_pos]
	
	print "Working on position",position,"with native identity",wild_type,"and native score",wild_type_score

	# Subtract wild type from each score and append to new array
	for j,sub_entry in enumerate(entry):
		if j == 0:
			new_insert.append(sub_entry)
		if j > 0 and j < 19:
			if sub_entry == 'ERROR!':
				new_insert.append(sub_entry)
			else:
				if j == wild_type_array_pos:
					new_insert.append('N')
				else:
					subtracted_score=sub_entry-wild_type_score
					new_insert.append(subtracted_score)
		if j == 19:
			new_insert.append(wild_type)
			
	# Write out new scores to file
	for element in new_insert:
		sub_table.write(str(element)+'\t')
	sub_table.write('\n')
			
raw_table.close()
sub_table.close()
error_log.close()
	


