import numpy as np
import subprocess
import pickle

from model.abaqus_part import BasePart


def update_range(nodes):
    node_data = np.array(nodes)
    if node_data.size == 0:
        return [[0, 0], [0, 0], [0, 0]]
    # Get the min and max values for each coordinate
    xrange = [np.min(node_data[:, 1]), np.max(node_data[:, 1])]
    yrange = [np.min(node_data[:, 2]), np.max(node_data[:, 2])]
    zrange = [np.min(node_data[:, 3]), np.max(node_data[:, 3])]
    return [xrange, yrange, zrange]

class Importer():
    """Class to import data from an ABAQUS input file for base class"""
    def __init__(self, name: str):
        self.part = BasePart(name)

    def import_base(self, filepath: str, scale: float):
        part = None
        file_ext = filepath.split('.')[-1]
        importer = Importer("BASE")
        
        if file_ext == 'inp':
            part = importer.from_inp_file(filepath=filepath, scale=scale)
        elif file_ext == 'odb':
            part = importer.from_odb_file(filepath=filepath, part_name='BASE')

        print('Complete import the base')
        return part
    
    def from_inp_file(self, filepath, scale=1):
        """Open the input file and read the data.
        This function has the ability to import only once part at a time

        Arguments:
            filepath (str): The path to the input file
            scale: (int)
        Returns:
            None
        """

        try:
            nodes, elements = [], []
            trigger = 0 # = 0 for part, 1 for nodes, 2 for elements
            with open(filepath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.upper() # make string to upper case because in abaqus the string is not sensitive
                    if line[0] != '*':  # ignore if this line is a comment 
                        if trigger == 1:    # for line containts node
                            node_data = line.strip().split(',')
                            nodes.append([int(node_data[0])]+[float(i) for i in node_data[1:]]) # Convert to float if numeric
                        elif trigger == 2:  # for line containts element
                            element_data = line.strip().split(',')
                            elements.append([int(i) for i in element_data if i != ''])
                    elif 'PART' in line:
                        trigger = 0
                        name = line.split("=")[1].strip() # split by equal character and get the name of the part
                    elif 'NODE' in line:
                        trigger = 1
                    elif 'ELEMENT' in line:
                        trigger = 2

            # update range of the base
            self.part.xrange, self.part.yrange, self.part.zrange = update_range(nodes)

            # translate objects to origin
            if self.part.xrange[0] != 0 or self.part.yrange[0] != 0 or self.part.zrange[0] != 0:
                for i in range(len(nodes)):
                    nodes[i][1] -= self.part.xrange[0]
                    nodes[i][2] -= self.part.yrange[0]
                    nodes[i][3] -= self.part.zrange[0]

                self.part.xrange[1] -= self.part.xrange[0]
                self.part.yrange[1] -= self.part.yrange[0]
                self.part.zrange[1] -= self.part.zrange[0]
                self.part.xrange[0] = 0
                self.part.yrange[0] = 0
                self.part.zrange[0] = 0
            
            #   scale the workpiece 
            for node in nodes:
                node[1] *= scale
                node[2] *= scale
                node[3] *= scale
            self.part.xrange[1] *= scale
            self.part.yrange[1] *= scale
            self.part.zrange[1] *= scale
            
            # update the main parts
            self.part.nodes = nodes
            self.part.elements  = elements

            return self.part

        except FileNotFoundError:
            print(f"File '{filepath}' not found.")

    def from_odb_file(self, filepath, part_name):
        base_encrypted = subprocess.Popen(["abaqus", "python", "./model/read_odb.py"], 
                                          stdin=subprocess.PIPE, 
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          shell=True,
                                          text=True)
        output, _ = base_encrypted.communicate(input=filepath)
        with open(output, "rb") as f:
            base = pickle.load(f)
            
        return base

    