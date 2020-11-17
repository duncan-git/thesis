#!/usr/bin/python

from pymol import cmd

########### CHANGE THIS LIST AS NEEDED #######
delete_atoms=['N','HN','C','H1A','H1B','H1C'] # atoms to be removed from rotamer library
#delete_atoms=['N1','H17'] # atoms to be removed from rotamer library
three_letter_code='PP2' # three-letter residue name specified in -n for molfile_to_params
atoms_to_align=['C13','C12','C14'] # atoms around the lysine-ligand bond for alignment and visualisation
##############################################

cmd.delete('*')
cmd.load('conformers.mol2')
target='conformers'
cmd.split_states(target,prefix='Molecule_Name_')
cmd.delete(target)
counter=0
target_atom1=''
target_atom2=''
target_atom3=''
target_atom4=''
for object in cmd.get_object_list('(all)'):
	cmd.alter(object,'resn="'+three_letter_code+'"')
	counter+=1
	if counter==1:
		target_object=object
		target_atom1=target_object+' and name '+atoms_to_align[0]
		target_atom2=target_object+' and name '+atoms_to_align[1]
		target_atom3=target_object+' and name '+atoms_to_align[2]
		for element in delete_atoms:
			print("got here")
			cmd.remove('{object} and name {element}'.format(object=object,element=element))
	if counter > 1:
		mobile_atom1=object+' and name '+atoms_to_align[0]
		mobile_atom2=object+' and name '+atoms_to_align[1]
		mobile_atom3=object+' and name '+atoms_to_align[2]
		print(target_atom1)
		print(mobile_atom1)
		cmd.pair_fit(mobile_atom1,target_atom1,mobile_atom2,target_atom2,mobile_atom3,target_atom3)
		for element in delete_atoms:
			cmd.remove('{object} and name {element}'.format(object=object,element=element))
cmd.join_states(three_letter_code+'.rotlib','*')
cmd.save(three_letter_code+'.rotlib.pdb',three_letter_code+'.rotlib','0')
cmd.save(three_letter_code+'_edited.mol2','Molecule_Name_0001')
