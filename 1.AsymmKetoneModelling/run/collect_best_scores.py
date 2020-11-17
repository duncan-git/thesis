import os,sys
import shutil

# $ cd ${DIR}/run
# $ run collect_best_scores.py

# check if best_pdbs folder exists already, if not, make it
if not os.path.exists('best_totalscore_pdbs'):
	os.mkdir('best_totalscore_pdbs')

# run through each sub-directory and read each scorefile for that directory
# choose only the best total score for that directory

for folder in os.listdir('.'):
	if os.path.isdir(folder):
		os.chdir(folder)
		best_total_score=100000
		best_pdb_line=[]
		best_pdb=''
		regex=['I133F','RA95']
		average_score=0
		average_counter=0

		for file in sorted(os.listdir('.')):
			if file.endswith('.sc') or file.endswith('.scores'):
				with open(file) as score_read:
					for line in score_read:
						if line.startswith('SCORE:'):

							if not 'fa_atr' in line:
								cur_line=line.strip()
								cur_total_score=cur_line.split()[1]
								cur_total_score=float(cur_total_score)
								average_score+=cur_total_score
								average_counter+=1
								if cur_total_score < best_total_score:
									best_total_score=cur_total_score
									best_pdb_line=cur_line.split(' ')

		for element in best_pdb_line:
			if element in regex:
				best_pdb=element+'.pdb'

		average_score=average_score/average_counter

		print("Best pdb in this directory is:", best_pdb)
		print("Score for this pdb is:", best_total_score, "REU")
		print("Average score for this directory is:", average_score, "REU")

		shutil.copy(best_pdb,'../best_totalscore_pdbs/'+best_pdb)
		os.chdir('..')
