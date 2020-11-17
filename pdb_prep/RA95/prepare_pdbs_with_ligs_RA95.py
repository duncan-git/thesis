#!/usr/bin/python

# run from within PyMol after navigating to folder containing RA95.pdb

from pymol import cmd
from os import sys

cmd.delete('*')
cmd.load('RA95.pdb','RA95_target')
current_cwd=os.getcwd()
loaded_ligs=[]
for file in os.listdir('../ligs'):
	if file.endswith('0001.pdb'):
		ligand_name=file.split('_')[0]
		loaded_ligs.append(ligand_name)
		cmd.load('../ligs/'+file,ligand_name)

target_atom1='RA95_target and name C12'
target_atom2='RA95_target and name C13'
target_atom3='RA95_target and name C14'

for ligand in loaded_ligs:
	mobile_atom1=ligand+' and name C12'
	mobile_atom2=ligand+' and name C13'
	mobile_atom3=ligand+' and name C14'
	cmd.pair_fit(mobile_atom1,target_atom1,mobile_atom2,target_atom2,mobile_atom3,target_atom3)

cmd.remove('RA95_target and resn LLK')

for ligand in loaded_ligs:
	cmd.copy('RA95_'+ligand,'RA95_target')
	cmd.fuse(ligand+' and name C13','RA95_'+ligand+' and resn LYM and name NZ','3')
	cmd.bond('RA95_'+ligand+' and resn LYM and name NZ','RA95_'+ligand+' and name C13')
	cmd.alter('RA95_'+ligand+' and resn '+ligand,'segi="B"')
	cmd.sort('RA95_'+ligand)
	cmd.save('RA95_'+ligand+'.pdb','RA95_'+ligand,'0')
