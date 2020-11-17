#!/usr/bin/python

# to be run from within 'run' folder

import os,sys
import shutil
from glob import glob

designable_positions = [8,9,51,53,57,84,88,89,110,111,112,131,133,159,161,180,181,182,183,184,185,186,210,134,135]
# NOTE this this based on ROSETTA numbering, which counts the first residue (Pro2) as residue 1
amino_acids = ['A','V','I','L','M','F','Y','W','S','T','N','Q','C','R','H','K','D','E']

batch_submit=open("../batch_submit.txt","w")
parent_cwd=os.path.dirname(os.path.abspath('.'))

# adjust runtime options as needed
batch="bsub -N -n 1 -W 119:59"
exe="/cluster/apps/rosetta/3.8/x86_64/main/source/bin/rosetta_scripts.hdf5.linuxgccrelease"
options=" -ex1 -ex2 -ex3 -ex4 -run:preserve_header true"
cst="CSR.enzdes.cst"
lig="CSR.params"
lys="LYM.params"
pdb="RA95_CSR.pdb"
rotlib="RSR.rotlib.pdb"
ligand="CSR"
script="RA95_CXX_FD_SemiFixBB.xml"
nstruct="300"

python_script='extract_scores_from_silent.py'
counter=0

for element in designable_positions:

	position=element-1
	actual_position=element
	print('Making directory for position {position}'.format(position=position))
	for residue in amino_acids:
		dir_name=str(actual_position)+'_'+str(residue)+'_'+ligand
		counter+=1
		print('Making sub-directory for amino acid {residue}'.format(residue=residue))
		os.mkdir(dir_name)

		batch_submit.write('echo \"Submitting job {dir_name}\" && \
{batch} -J {dir_name}_run -o logs/log_{dir_name}.txt \
{exe} {options} \
-enzdes:cstfile ligs/{cst} \
-extra_res_fa ligs/{lig} \
-extra_res_fa ligs/{lys} \
-s pdb_inp/{pdb} \
-parser:protocol script/{script} \
-parser:script_vars target={position} \
-parser:script_vars aa={residue} \
-parser:script_vars ligand={ligand} \
-out:file:silent run/{dir_name}/{dir_name}.silent \
-nstruct {nstruct} \n\
echo "Submitting post-run processing" \n\
cd run/{dir_name} && \
bsub -N -n 1 -W 00:10 -J {dir_name}_py -w "done({dir_name}_run)" -o log_python.txt python {parent_cwd}/script/{python_script} \n\
cd {parent_cwd} \n'.format(dir_name=dir_name,position=position,residue=residue, batch=batch, exe=exe, options=options, cst=cst, lig=lig, lys=lys, script=script, pdb=pdb, nstruct=nstruct,ligand=ligand,parent_cwd=parent_cwd,python_script=python_script))

print("Total number of jobs is:", counter)

batch_submit.close()
