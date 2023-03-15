import re 

class Bond:
            def __init__(self, line, fromline=False):
                if fromline == True:
                    fields = line.split()
                    if (len(fields[2]) <= 2) and (re.findall(r'[a-zA-Z]{1,2}[0-9]?', fields[2])):
                        ## Typical syntax used by xdraw
                        self.center = int(fields[1])
                        self.atom_type = str(fields[2])
                        self.bonded_atoms = fields[3:]
                    else:
                        ## Typical syntax outputed by antechamber using pdbm format.
                        self.center = int(fields[1])
                        self.atom_type = None
                        self.bonded_atoms = fields[2:]
                else:
                    raise NotImplementedError("This class should only be initialized using a line from a PDB file.")
