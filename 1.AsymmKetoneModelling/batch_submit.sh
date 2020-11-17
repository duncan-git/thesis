#!/bin/bash

for j in {'NB1','NB2','PP1','PP2','PEN','BUT'}; do
  mkdir run/I133F_$j
  for i in {1..500}; do
    bsub -n 1 -W 00:59 -o /dev/null rosetta_scripts.hdf5.linuxgccrelease @relax.flags -extra_res_fa ligs/${j}.params -enzdes:cstfile ligs/enzdes/${j}.enzdes.cst -s pdb_inp/I133F_${j}.pdb -out:path:all run/I133F_${j} -out:suffix _$i
  done
done

for j in {'NB1','PP3'}; do
  mkdir run/RA95_$j
  for i in {1..500}; do
    bsub -n 1 -W 00:59 -o /dev/null rosetta_scripts.hdf5.linuxgccrelease @relax.flags -extra_res_fa ligs/${j}.params -enzdes:cstfile ligs/enzdes/${j}.enzdes.cst -s pdb_inp/RA95_${j}.pdb -out:path:all run/RA95_${j} -out:suffix _$i
  done
done
