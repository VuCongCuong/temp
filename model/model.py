import os
import subprocess
import numpy as np
import logging

from model.importer import Importer
from model.abaqus_part import BasePart, Grain
from gcodeparser import GcodeParser

logger = logging.getLogger("main")
class Model:
    def __init__(self, name='Grind'):
        """Initialize the model class with model name."""
        self.model_name = name  
        self.settings = None
        self.base = None
        self.grains = []

        self.mode = 'single'
        self.gcode = None
        self.name = None
        self.mat_base = None
        self.wp_mat = None
        
        self.ntool_sect = 10
        self.grain_storage = dict()
        self.gra_mat_pos = None
        self.abra_vel = 0
        
        self.br = 0 # break character counter
    
    def import_base(self, file_path):
        """Import mesh file."""
        self.importer = Importer("BASE")
        self.base = self.importer.import_base(file_path, scale=100)
        return self.base
    
    def import_grains(self, name, vertices, totals=1, size=100,
                       spacing = 1, dist_type=None, mat=None, 
                       init_depth=0, increasing_depth=0,
                       velocity = 1):
        """Import n-abrasive grains to the model."""
        self.abra_vel = velocity
        grain_pos = []
        x = -(size + 100) # 100 is the offset of the tool to ensure that the tool is not in contact with the workpiece
        z = self.base.zrange[1] - init_depth
        yoffset = self.base.yrange[1]/2 

        if dist_type == 'random':
            for _ in range(totals):
                y = yoffset + np.random.uniform(-spacing, spacing)
                grain_pos.append((x, y, z))
        elif dist_type == 'normal':
            for _ in range(totals):
                y = yoffset + np.random.normal(-spacing, spacing)
                grain_pos.append((x, y, z))
        elif dist_type == 'uniform':
            if totals % 2 != 0:
                grain_pos.append((x, yoffset, z))
                for i in range(int(totals/2)):
                    i += 1
                    y1 = yoffset + i * spacing
                    y2 = yoffset - i * spacing
                    grain_pos.append((x, y1, z))
                    grain_pos.append((x, y2, z))
            else:
                for i in range(int(totals)):
                    y = yoffset + (i-totals/2) * spacing
                    grain_pos.append((x, y, z))
        
        grain_coords = []
        self.grains = [] # reset abrasive grains collection
        for i in range(totals):
            grain = Grain(name+str(i), vertices, size) # name, number of vertices
            grain.mat  = mat
            grain.translate = list(grain_pos[i])
            # grain.generate_mesh(5)
            self.grains.append(grain)
            grain_coords.append(grain)
        
        logger.info(f"Generate {totals} abrasive seed(s) with {dist_type} distribution.")
        
        return grain_coords
    

    def build(self, step: int, settings=None):
        """Build the model."""
       
        if self.mode == 'multiple': 
            for i, node in enumerate(self.gra_mat_pos[self.ntool_sect % (step+1)]):
                grain = Grain('G'+str(i), 10)
                grain.translate = list(node)
                grain.assign_material(self.wp_mat)
                self.grains.append(grain) 

        if step == 0:
            self.mat_base = self.base.mat
            self.name = f"{self.model_name}_{step}"
            self.write(file_path=self.name, mode=step) 
        else:
            self.base = self.importer.import_base(self.name+'.odb', scale=1)
            self.base.mat = self.mat_base
            self.name = f"{self.model_name}_{step}"
            self.write(file_path=self.name, mode=step)

    def run(self):
        """Run the simulation."""

        # check to remove the lock file
        file_path = self.name + '.lck'
        if os.path.exists(file_path): # Remove the file 
            os.remove(file_path) 
            logger.info(f"{file_path} has been removed successfully.")
        
        # run the simulation by involving abaqus solver
        # double precision is requirement
        cmd_command = f"abaqus job={self.name} input=./.run/{self.name} cpus=4 gpus=1 scratch=./.temp/ ask_delete=off"
        logger.info(f"Running the simulation with command:\n {cmd_command}")
        subprocess.run(cmd_command, check=True, shell=True, capture_output=True, text=True)
        logger.info(f"Simulation {self.name} is completed.")

    def stop(self):
        """Stop the simulation."""
        cmd_command = f"abaqus job={self.name} terminate"
        subprocess.run(cmd_command, shell=True, capture_output=True, text=True)


    def import_gcode(self, file_path):
        # open gcode file and store contents as variable
        with open(file_path, 'r') as f:
            gcode = f.read()

        for line in GcodeParser(gcode).lines:
            if line.command[0] == 'G':
                print("ok")
            
    
    def generate_matrix_of_grains(self, res=1, radius=1000, tool_type='cylinder', mat=None):
        """Generates a matrix of grains based on the selected distribution.
        """
        def _generate_sphere_matrix():
            """Generates a matrix of grains in a spherical shape.

            Returns
            -------
            list
                A list of grain positions forming a spherical matrix.
            """
            num_points = int(4 * np
            .pi * radius**2 / (res**2))

            grain_positions = []
            for _ in range(num_points):
                theta = np.random.uniform(0, 2 * np.pi)
                phi = np.random.uniform(0, np.pi)
                x = radius * np.sin(phi) * np.cos(theta)
                y = radius * np.sin(phi) * np.sin(theta)
                z = radius * np.cos(phi)
                grain_positions.append((x, y, z))

            return grain_positions
        
        def _generate_cylinder_matrix():
            """Generates a matrix of grains in a cylindrical shape.

            Parameters
            ----------
            res : float
                Resolution of the cylinder mesh.

            Returns
            -------
            list
                A list of grain positions forming a cylindrical matrix.
            """
            height = radius/2
            num_layers = int(height / res)
            num_points_per_layer = int(2 * np.pi * radius / res)

            gra_mat_pos = [[] for _ in range(self.ntool_sect)]  # Combined list for all sections

            section_angle = 2 * np.pi / self.ntool_sect
            for z in np.linspace(0, height, num_layers):
                for theta in np.linspace(0, 2 * np.pi, num_points_per_layer, endpoint=False):
                    x = radius * np.cos(theta)
                    y = radius * np.sin(theta)
                    position = (x, y, z)

                    # Determine which section the position belongs to
                    section_index = int(theta // section_angle)
                    gra_mat_pos[section_index].append(position)

            return gra_mat_pos
        
        
        if tool_type == "cylinder":
            self.gra_mat_pos = _generate_cylinder_matrix()

        elif tool_type == "sphere":
            self.gra_mat_pos = _generate_sphere_matrix()
        
        self.wp_mat = mat
        self.mode = 'multiple'
               

    def write(self, file_path, mode=0):
        current_dir = os.getcwd()
        if not os.path.exists('.run'):
            os.makedirs('.run')
        try:
            with open('.run/'+file_path+'.inp', 'w') as file:
                file.write("!Grinding simulation process, Author: Vu Hoai Lam\n")
                file.write("!Email: Lam.VH205731@sis.hust.edu.vn\n")
                file.write("*PHYSICAL CONSTANTS, ABSOLUTE ZERO=0.0\n")
                mats = [self.base.mat.name]
                mat_lists = [self.base.mat]
                for grain in self.grains:
                    if grain.mat.name not in mats:
                        mats.append(grain.mat.name)
                        mat_lists.append(grain.mat)

                self._write_materials(file, mat_lists)
                self._write_parts(file)
                self._write_assembly(file)
                self.write_boundary_conditions(file, mode)
                self._write_element_control(file)
                self._write_interaction(file)
                self._write_step(file)
            file.close()
            logger.info(f"Model {file_path} is written successfully.")
                
        except FileNotFoundError:
            print(f"Cannot write to the '{self.model_name}'.")

    def _write_base_elements(self, file, elements):
        trigger = 0
        for ele in elements:
            n = len(ele)
            if trigger != n:
                file.write(f"*ELEMENT, TYPE=C3D{n-1}T\n")
                trigger = n
            file.write("{:<10}, {}\n".format(ele[0], ",".join(map(str, ele[1:]))))
        return 0    
    
    def _write_abrasive_elements(self,file, elements):
        trigger = 0
        for ele in elements:
            n = len(ele)
            if  trigger != n:
                if n == 4:
                    file.write("*ELEMENT, TYPE=S3RT\n")
                else:
                    file.write(f"*ELEMENT, TYPE=C3D{n-1}T\n")
                trigger = n
            file.write("{:<10}, {}\n".format(ele[0], ",".join(map(str, ele[1:]))))
             
            
    def _write_list_data(self, file, datas):
        
        br = 0
        for data in datas:
            if isinstance(data, tuple) or isinstance(data, list):
                if len(data) > 1:
                    data = data[0]
            br += 1
            if br%8 == 0:
                file.write("{}\n".format(data))
            else:
                file.write("{}, ".format(data))
        if br%8 != 0:
            file.write("\n")


    def _write_materials(self, file, mat_lists):
        for mat in mat_lists:
            file.write(f"*MATERIAL, NAME={mat.name}\n")

            # Density
            if hasattr(mat, "density"):
                file.write(f"*Density\n{mat.density},\n")

            # Elastic
            if hasattr(mat, "E") and hasattr(mat, "u"):
                file.write(f"*Elastic\n{mat.E}, {mat.u}\n")

            # Plastic
            if all(hasattr(mat, attr) for attr in ["A", "B", "n", "m", "Tm", "Tr"]):
                file.write(f"*Plastic, hardening=JOHNSON COOK\n")
                file.write(f"{mat.A}, {mat.B}, {mat.n}, {mat.m}, {mat.Tm}, {mat.Tr}\n")

            # Rate dependent (Johnson-Cook)
            if hasattr(mat, "C") and hasattr(mat, "e0"):
                file.write(f"*Rate Dependent, type=JOHNSON COOK\n")
                file.write(f"{mat.C}, {mat.e0}\n")

            # Damage initiation
            if all(hasattr(mat, attr) for attr in ["D1", "D2", "D3", "D4", "D5", "Tm", "Tr"]):
                file.write(f"*DAMAGE Initiation, CRITERION=JOHNSON COOK\n")
                file.write(f"{mat.D1}, {mat.D2}, {mat.D3}, {mat.D4}, {mat.D5}, {mat.Tm}, {mat.Tr}, 1\n")
                file.write(f"*Damage Evolution, type=DISPLACEMENT\n10,\n")

            # Thermal properties
            if hasattr(mat, "k"):
                file.write(f"*Conductivity, TYPE=ISO\n{mat.k}\n")
            if hasattr(mat, "Cp"):
                file.write(f"*Specific heat\n{mat.Cp}\n")

    def _write_parts(self, file):
        """Write the parts to the input file."""
        ## write the tool
        for grain in self.grains:
            file.write("*PART, NAME={}\n".format(grain.name))
            file.write("*Node\n")
            # write the nodes
            for node in grain.nodes:
                file.write("{:<10}, {:<15}, {:<15}, {:<15}\n".format(node[0], node[1], node[2], node[3]))
            # write the elements
            self._write_abrasive_elements(file, grain.elements)
            file.write(f"*ELSET, ELSET={grain.name}_ELSET\n")
            self._write_list_data(file, grain.elements) 

            file.write(f"*SHELL SECTION, ELSET={grain.name}_ELSET, MATERIAL={grain.mat.name}\n")
            file.write(f"20, 5\n") # thickness and integration points
            file.write("*END PART\n")
            
        # write the workpiece
        file.write("*PART, NAME={}\n".format(str(self.base.name)))
        file.write("*Node\n")
        for node in self.base.nodes:
            file.write("{:<10}, {:<15}, {:<15}, {:<15}\n".format(node[0], node[1], node[2], node[3]))
        self._write_base_elements(file, self.base.elements)
        
        # Define element set
        file.write(f"*ELSET, ELSET={str(self.base.name)}_ELSET\n")
        self._write_list_data(file, self.base.elements)
        file.write(f"*SOLID SECTION, ELSET={str(self.base.name)}_ELSET, MATERIAL={self.base.mat.name}\n")
        file.write("*END PART\n")
    
    def _write_assembly(self, file):
        """Write the assembly to the input file."""
        ###############################################
        # Write the definition of the assembly
        ###############################################
        file.write("*ASSEMBLY, NAME=GRINDING_PROCESS\n")
        # write the tool assembly
        for grain in self.grains:
            file.write("*INSTANCE, NAME={}, PART={}\n".format(grain.name, grain.name)) 
            file.write("*NSET, NSET={}_NSET\n".format(grain.name))
            self._write_list_data(file, grain.nodes)
            file.write("*END INSTANCE\n")
        
        # define constrain between node
        file.write(f"*Node\n")
        file.write("1, -100, 0, 0\n")  # let 1 be the referenece node for tool
        file.write("*Nset, nset=SET_VEL\n")
        file.write("1\n")

        # write the workpiece assembly
        file.write(f"*INSTANCE, NAME={str(self.base.name)}, PART={str(self.base.name)}\n")
        file.write(f"*NSET, NSET=FIX_BASE_NSET\n")
        self.base.select_by_zcoord( type = 'node', zrange= [-0.1, 0.2], name = 'FIX_BASE_NSET')
        self._write_list_data(file, self.base.set['FIX_BASE_NSET'])
        # select node to make contact
        file.write(f"*NSET, NSET=S_SET_2\n")
        
        self.base.select_by_zcoord( type = 'node', 
                                   zrange= [self.base.zrange[1] - 0.2*(self.base.zrange[1]-self.base.zrange[0]), self.base.zrange[1]], 
                                   name = 'CONTACT_NSET')
        self._write_list_data(file, self.base.set['CONTACT_NSET'])
        ## Define node set
        file.write(f"*NSET, NSET=BASE_NSET\n")
        self.br = self._write_list_data(file, self.base.nodes)
        file.write("*END INSTANCE\n")

        for grain in self.grains:
            file.write(f"*ELSET, ELSET=SEED_COLLECT_NSET, instance={grain.name}\n")
            self._write_list_data(file, grain.elements)

        for grain in self.grains:
            file.write(f"*Surface, type=ELEMENT, name=m_Surf_{grain.name}\n")
            file.write(f"{grain.name}.{grain.name}_ELSET, SNEG\n")
        
        file.write("*Surface, type=NODE, name=s_Set_2_CNS_, internal\n")
        file.write("BASE.S_SET_2, 1.\n")

        # add constraint
        file.write(f"*Rigid Body, ref node=SET_VEL, elset=SEED_COLLECT_NSET, isothermal=NO\n")
        file.write("*END ASSEMBLY\n")

    def _write_element_control(self, file):
        ###############################################
        # Element controls
        ###############################################
        file.write(f"*Section Controls, name=EC-1, ELEMENT DELETION=YES, hourglass=STIFFNESS\n")
        file.write(f"1., 1., 1.\n")

    def write_boundary_conditions(self, file, mode):
        """Write the boundary conditions to the input file."""
        ###############################################
        ## BOUNNDARY CONDITIONS
        ###############################################
        file.write(f"*Boundary\n")
        file.write(f"BASE.FIX_BASE_NSET, ENCASTRE\n")
        file.write(f"*Boundary, op=NEW\n")
        file.write(f"SET_VEL, 2, 2\n")
        file.write(f"SET_VEL, 3, 3\n")
        file.write(f"SET_VEL, 4, 4\n")
        file.write(f"SET_VEL, 5, 5\n")
        file.write(f"SET_VEL, 6, 6\n")

        ###############################################
        ## DEFINI INITIAL CONDITION
        ###############################################
        if mode != 0:
            
            file.write("** Initial conditions\n")
            file.write("*INITIAL CONDITIONS, TYPE=STRESS\n")
            for ele in self.base.initial_stress:
                label, stress = ele
                stress_str = ', '.join(map(str, stress))
                file.write(f"{str(self.base.name)}.{label}, {stress_str}\n")
            
            file.write("*INITIAL CONDITIONS, TYPE=PLASTIC STRAIN\n") 
            for ele in self.base.initial_plstrain:
                label, plstrain = ele
                plstrain_str = ', '.join(map(str, plstrain))
                file.write(f"{str(self.base.name)}.{label}, {plstrain_str}\n") 

            file.write("*INITIAL CONDITIONS, TYPE=DAMAGE INITIATION, CRITERION=DUCTILE\n")
            for ele in self.base.initial_damage:
                label, damage = ele
                # damage_str = ', '.join(map(str, damage))
                file.write(f"{str(self.base.name)}.{label}, {damage}\n")
            
            file.write("*INITIAL CONDITIONS, TYPE=TEMPERATURE\n")
            for ele in self.base.initial_temperature:
                label, temperature = ele
                file.write(f"{str(self.base.name)}.{label}, {temperature}\n")
            
        file.write("*INITIAL CONDITIONS, TYPE=TEMPERATURE\n")
        for grain in self.grains:
            file.write(f"{grain.name}.{grain.name}_NSET, 20\n")
        
        if mode == 0:
            file.write("BASE.BASE_NSET, 20\n")
       

    def _write_interaction(self, file):
        """Write the interaction properties to the input file."""
        ###############################################
        ## INTERACTION PROPERTIES
        ###############################################
        file.write(f"** Contact Interaction\n")
        file.write(f"*Surface Interaction, name=IntProp\n")
        file.write(f"*Friction\n")
        file.write(f"0.3\n")
        file.write(f"*Surface Behavior, pressure-overclosure=HARD\n")
        file.write(f"*Gap Heat Generation\n")
        file.write(f"1., 0.5\n")
    
    def _write_step(self, file):
        """Write the step to the input file."""
        ###############################################
        ## DEFINI STEP: Step 1
        ###############################################
        file.write(f"*STEP, name=Step-1, nlgeom=YES\n")
        file.write(f"*DYNAMIC TEMPERATURE-DISPLACEMENT, EXPLICIT\n") # 
        file.write(f", 2.2e-5\n")
        
        # INTERACTION DEFINITION
        for grain in self.grains:
            file.write(f"*Contact Pair, interaction=INTPROP, mechanical constraint=KINEMATIC, cpset=Int-2\n")
            file.write(f"m_Surf_{grain.name}, s_Set_2_CNS_\n")
            
        ## VELOCITY
        file.write(f"*Boundary, type=VELOCITY\n")
        file.write(f"SET_VEL, 1, 1, {self.abra_vel}\n")
        self._write_output_request(file)
        file.write(f"*End Step\n")
    
    def _write_output_request(self, file):
        """Write the output request to the input file."""
        ###############################################
        ## OUTPUT REQUESTS
        ###############################################
        file.write(f"**Restart, write, number interval=1, time marks=NO\n")
        file.write(f"*Output, field, TIME INTERVAL=1e-6\n")
        file.write(f"STATUS\n")
        file.write(f"*Node Output\n")
        file.write(f"U, V, A, RF, COORD, NT\n")
        file.write(f"*Element Output, directions=YES, ELSET=BASE.BASE_ELSET\n")
        file.write(f"PE, PEEQ, S, SDEG, STATUS, TEMP\n") # PEVAVG,
        file.write(f"*Element Output, directions=YES, ELSET=G0.G0_ELSET\n")
        file.write(f"PE, PEEQ, S, SDEG, STATUS, TEMP\n") 
        file.write(f"*Contact Output\n")
        file.write(f"CSTRESS, CFORCE, CDISP, CSLIPR, CFRICWORK,\n") 
        ## HISTORY OUTPUT
        file.write(f"*Output, history, variable=PRESELECT\n")
        