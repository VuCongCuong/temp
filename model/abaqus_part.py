

import gmsh
import meshio
import numpy as np

from scipy.spatial import ConvexHull
from scipy.stats import uniform
from  model.material import Material, JonhsonCook
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import pyvista as pv

class Part():

    def __init__(self, name):
        """
        Initialize the Part class with a name and empty dictionaries for nodes and elements.
        -   the nodes contain the following each node which contains these information:
            [0] node id, [1:3] coordinates, [4] temperature, [5] velocity, [6] acceleration, 
            [7] density, [8] young modulus, [9:11] force
        -   the elements contain the following each element which contains these information:
            [0] element id, [1:8] node ids, [9:15] stress, [16:22] strain, [23] damage, [24] state
        """
        self.name           = name
        self.nodes          =  {} 
        self.elements       =  {} 
        self.set            =  {}
        self.mat            : Material

    def select_by_coordinates(self, type: str, xrange: list, yrange: list, zrange: list, name: str):
        if type == "node":
            node_list = [node for node in self.nodes
                         if (xrange[0] < node[1]) and (node[1] < xrange[1])  
                         and (yrange[0] < node[2]) and (node[2] < yrange[1])
                         and (zrange[0] < node[3]) and (node[3] < zrange[1])
            ]
            self.set[name] = node_list
        elif type == "element":
            node_list = self.select_by_coordinates("node", xrange, yrange, zrange)
            element_list = [element for element in self.elements 
                            if element[1:] in node_list]
            self.set[name] = element_list
        else:
            raise ValueError("Invalid type. Choose 'node' or 'element'.")


    def select_by_zcoord(self, type: str, zrange: list, name: str):
        
        if type == "node":
            node_list = [node[0] for node in self.nodes if (zrange[0] <= node[3]) and (node[3] < zrange[1])]
            self.set[name] = node_list
        elif type == "element":
            node_list = self.select_by_zcoord("node", zrange)
            element_list = [element for element in self.elements 
                            if element[1:] in node_list]
            self.set[name] = element_list
        return self.set[name]
    
    def select_by_label(self, label_list: str):
        if label_list not in self.set:
            print("The label list does not exist.")
            return None
        return self.set[label_list]
    
    def assign_material(self, material: Material):
        self.mat = material    
    
    def select_by_radius(self, type: str, center: list, radius: float, name: str):
        if type == "node":
            node_list = [node for node in self.nodes 
                        if ((node[1]-center[0])**2 + (node[2]-center[1])**2 + (node[3]-center[2])**2) < radius**2]
            self.set[name] = node_list
        elif type == "element":
            node_list = self.select_by_radius("node", center, radius)
            element_list = [element for element in self.elements 
                            if element[1:] in node_list]
            self.set[name] = element_list
        else:
            raise ValueError("Invalid type. Choose 'node' or 'element'.")
    
class BasePart(Part):
    def __init__(self, name):
        super().__init__(name)
        self.xrange = [0, 0]
        self.yrange = [0, 0]
        self.zrange = [0, 0]


class Grain(Part):
    def __init__(self, name, num_vertices, size):
        super().__init__(name)
        self.size = size
        self.gen_convex_hull_grain(num_vertices)
        self.translate = [0, 0, 0]

    def gen_rand_translate(self, xrange, yrange, zrange):
        
        x = uniform.rvs(loc=xrange[0], scale=xrange[1]-xrange[0])
        y = yrange[0] + 0.5 * (yrange[1] - yrange[0])
        # scale z range 20 % on top
        zrange[0] = zrange[1] - (zrange[1]-zrange[0])*0.2
        z = uniform.rvs(loc=zrange[0], scale=zrange[1]-zrange[0])
        z = zrange[1]   # some testings
        self.translate = [x, y, z]       
        
    def _gen_rand_spherical_points(self, num_points):
        rng = np.random.default_rng()
        theta = rng.uniform(0, 2 * np.pi, num_points)  # Azimuthal angle
        phi = rng.uniform(0, np.pi, num_points)         # Polar angle

        # Convert spherical coordinates to Cartesian coordinates
        # concat to ignore the 0-index 
        x = np.concatenate(([0], np.sin(phi) * np.cos(theta)))
        y = np.concatenate(([0], np.sin(phi) * np.sin(theta)))
        z = np.concatenate(([0], np.cos(phi)))

        points = np.column_stack((x, y, z))*self.size # scale the grain
        return points
        
    def gen_convex_hull_grain(self, number_of_points):

        points = self._gen_rand_spherical_points(number_of_points)
        hull = ConvexHull(points)
        normals = []
        
        for simplex in hull.simplices:
            # Calculate the normal of the face
            v0, v1, v2 = points[simplex]
            normal = np.cross(v1 - v0, v2 - v0)
            normal = normal / np.linalg.norm(normal)  # Normalize the normal vector
            normals.append(normal)
    
        nodes = [ [i] + list(node) for i, node in enumerate(points[1:], start=1) ]
        elements = [ [i] + list(nodes) for i, nodes in enumerate(hull.simplices, start=1) ]
        
        # calculate the center of the grain
        center = np.mean(np.array(nodes[1:])[:,1:4], axis=0)

        # make sure the normal is outwards
        for i, ele in enumerate(elements):
            normal = np.cross(points[ele[1]] - points[ele[2]], 
                              points[ele[3]] - points[ele[2]])
            normal = normal / np.linalg.norm(normal)  # Normalize the normal vector
            mid_pt = np.mean(np.array(points[ele[1:3]]), axis=0)

            if np.dot(mid_pt-center, normal) < 0:
                tmp = ele[1]
                ele[1] = ele[3]
                ele[3] = tmp
                elements[i]  = ele
        
        self.nodes = nodes
        self.elements = elements
    
    def generate_mesh(self, mesh_size: float):
        points = np.array([node[1:] for node in self.nodes])  # Convert nodes to NumPy array
        cells = [("triangle", np.array([[node_id - 1 for node_id in element[1:]] for element in self.elements]))]  # Adjust indices to be zero-based
        meshio.write_points_cells(
            "convex_hull.stl",
            points,
            cells
        )
        
        gmsh.initialize()
        gmsh.option.setNumber("General.Terminal", 1)

        # Load the STL file
        gmsh.merge("convex_hull.stl")  # replace with your file name

        # Classify surfaces to prepare for volume definition
        angle = 40  # angle threshold for sharp edges
        force_parametrizable_patches = True
        include_boundary = True
        curve_angle = 180
        gmsh.model.mesh.classifySurfaces(angle * 3.14159 / 180., include_boundary,
                                        force_parametrizable_patches, curve_angle * 3.14159 / 180.)

        # Create geometry from classified STL
        gmsh.model.mesh.createGeometry()

        # Create surface loop and volume (if it's a closed STL)
        surfaces = gmsh.model.getEntities(2)
        surface_tags = [s[1] for s in surfaces]
        sl = gmsh.model.geo.addSurfaceLoop(surface_tags)
        vol = gmsh.model.geo.addVolume([sl])
        gmsh.model.geo.synchronize()

        # Mesh size controls (optional)

        # Calculate bounding box dimensions
        xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.getBoundingBox(-1, -1)
        bounding_box_diagonal = ((xmax - xmin)**2 + (ymax - ymin)**2 + (zmax - zmin)**2)**0.5

        # Set mesh size as a proportion of the bounding box diagonal
        proportion = 0.05  # Adjust this proportion as needed
        mesh_size = bounding_box_diagonal * proportion

        gmsh.option.setNumber("Mesh.CharacteristicLengthMin", mesh_size)
        gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size)    # Generate 3D mesh
        gmsh.model.mesh.generate(3)

        # Launch GUI (optional)
        
        # Extract the mesh data back into nodes and elements
        node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
        
        self.nodes = [[int(tag)] + list(coord) for tag, coord in zip(node_tags, node_coords.reshape(-1, 3))]
        element_types, element_tags, node_tags = gmsh.model.mesh.getElements(dim=3)
        self.elements = []
        
        for i in range(len(element_tags[0])):
            index1 = element_types[0]*i
            index2 = element_types[0]*(i+1)
            self.elements.append([i+1, *node_tags[0][index1:index2]])
        
        # self.plot_mesh()
        gmsh.finalize()
    
    def plot_mesh(self):
        # gmsh.fltk.run()
        import matplotlib.pyplot as plt

        # Extract node coordinates
        node_coords = np.array([node[1:] for node in self.nodes])

        # Plot nodes
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(node_coords[:, 0], node_coords[:, 1], node_coords[:, 2], c='b', marker='', label='Nodes')

        # Plot elements
        for element in self.elements:
            element_nodes = np.array([self.nodes[node_id - 1][1:] for node_id in element[1:]])
            poly = Poly3DCollection([element_nodes], alpha=0.2, edgecolor='k')
            ax.add_collection3d(poly)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()