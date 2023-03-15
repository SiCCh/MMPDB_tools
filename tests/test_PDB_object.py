
pdb = PDB_file("PDB_with_amounts.pdb")
for molecule in pdb.molecules:
    print(molecule.name)
