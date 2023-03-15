import re 

class Atom:            
        def __init__(self, line, fromline=False):
            if fromline == True:
                fields = line.split()
                field_number = len(fields)
                if field_number == 9:
                    self.number = int(line[6:11])
                    self.name = line[12:16].strip()
                    self.resname = line[17:20].strip()
                    self.resnumber = int(line[22:26])
                    self.chain = line[21]
                    self.x = float(line[30:38])
                    self.y = float(line[38:46])
                    self.z = float(line[46:54])
                    self.charge = float(line[54:])
                    self.type = None
                elif field_number > 9:
                    self.number = int(fields[1])
                    self.name = fields[2]
                    self.resname = fields[3]
                    self.resnumber = int(fields[4])
                    self.x = float(fields[5])
                    self.y = float(fields[6])
                    self.z = float(fields[7])
                    self.charge = float(fields[8])
                    self.type = str(fields[-1])
            else:
                raise NotImplementedError("This class should only be initialized using a line from a PDB file.")