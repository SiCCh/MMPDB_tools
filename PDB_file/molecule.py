class Molecule:
    def __init__(self, atoms, amount=1) -> None:
        self.amount = amount
        self.atoms = []
        name = atoms[0].resname
        same_name = False
        self.total_charge = None
        total_charge = 0.0
        if atoms[0].charge != None:
            for atom in atoms:
                total_charge += atom.charge
            self.total_charge = round(total_charge, 6)
        for atom in atoms:
            self.atoms += [atom]
            if atom.resname == name:
                same_name = True
            else:
                same_name = False
                break
        if same_name == False:
            print("Warning: Atoms in molecule object belongs to different residues.")
        self.name = name
    
    def dipole_moment(self):
        dipole_moment = 0.0
        ### IMPLEMENT THIS LAZY BASTARD
