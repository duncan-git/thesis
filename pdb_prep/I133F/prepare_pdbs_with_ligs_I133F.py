#!/usr/bin/python

from pymol import cmd
from os import sys

# run from within PyMol after navigating to folder containing RA95.pdb

cmd.delete('*')
cmd.load('I133F_B.pdb','I133F_target')
current_cwd=os.getcwd()
loaded_ligs=[]
for file in os.listdir('../ligs'):
	if file.endswith('0001.pdb'):
		ligand_name=file.split('_')[0]
		loaded_ligs.append(ligand_name)
		cmd.load('../ligs/'+file,ligand_name)

target_atom1='I133F_target and name C12'
target_atom2='I133F_target and name C13'
target_atom3='I133F_target and name C14'

for ligand in loaded_ligs:
	mobile_atom1=ligand+' and name C12'
	mobile_atom2=ligand+' and name C13'
	mobile_atom3=ligand+' and name C14'
	cmd.pair_fit(mobile_atom1,target_atom1,mobile_atom2,target_atom2,mobile_atom3,target_atom3)

cmd.remove('I133F_target and resn PEN')

for ligand in loaded_ligs:
	cmd.fuse('I133F_target and resn LYM and name NZ',ligand+' and name C13','3')
	cmd.bond(ligand+' and resn LYM and name NZ',ligand+' and name C13')
	cmd.save('I133F_'+ligand+'.pdb',ligand,'0')
