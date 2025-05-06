import numpy as np

import gmsh
from scipy.spatial import ConvexHull
from scipy.stats import uniform
from  model.material import Material, JonhsonCook

class Part():

    def __init__(self, name):
        """
        Initialize the Part class with a name and empty dictionaries for nodes and elements.
        -   the nodes contain the following each node which contains these information:
            [0] node id, [1:3] coordinates, [4] temperature, [5] velocity, [6] acceleration, 
            [7] density, [8] young modulus, [9] force
        -   the elements contain the following each element which contains these information:
            [0] element id, [1:3] node ids, [4:6] stress, [7:9] strain, [10] damage, [11] state
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
        
        max_angle = 180
        min_angle = 0
        while (max_angle > 173) and (min_angle < 5):
            points = self._gen_rand_spherical_points(number_of_points)
            hull = ConvexHull(points)
            normals = []
            
            for simplex in hull.simplices:
                # Calculate the normal of the face
                v0, v1, v2 = points[simplex]
                normal = np.cross(v1 - v0, v2 - v0)
                normal = normal / np.linalg.norm(normal)  # Normalize the normal vector
                normals.append(normal)

            min_angle = self._calc_min_angle(normals)
            max_angle = self._calc_max_angle(normals)
        
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

    def _calc_max_angle(self, normals):
        max_angle = 0  # Start with a minimum angle
        for i in range(len(normals)):
            for j in range(i + 1, len(normals)):
                # Calculate the angle between normals
                n1 = normals[i]
                n2 = normals[j]
                cos_theta = np.dot(n1, n2)
                angle = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))  # Clip for numerical stability
                max_angle = max(max_angle, angle)

        return max_angle
    def _calc_min_angle(self, normals):
        min_angle = 180  # Start with a maximum angle
        for i in range(len(normals)):
            for j in range(i + 1, len(normals)):
                # Calculate the angle between normals
                n1 = normals[i]
                n2 = normals[j]
                cos_theta = np.dot(n1, n2)
                angle = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))  # Clip for numerical stability
                min_angle = min(min_angle, angle)

        return min_angle
    
    def generate_mesh(self, mesh_size: float):
        """Generate tetrahedral mesh for the grain by gmsh"""
        gmsh.initialize()
        gmsh.model.add(self.name)

        # Add nodes
        for node in self.nodes:
            gmsh.model.geo.addPoint(node[1], node[2], node[3], mesh_size, node[0])

        # Add elements (triangular faces of the convex hull)
        for element in self.elements:
            gmsh.model.geo.addTriangle(element[1], element[2], element[3])

        # Synchronize the model
        gmsh.model.geo.synchronize()

        # Generate 3D mesh
        gmsh.model.mesh.generate(3)

        # Extract nodes and elements from gmsh
        node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
        element_types, element_tags, element_node_tags = gmsh.model.mesh.getElements()

        # Update self.nodes and self.elements with the generated mesh
        self.nodes = [[tag] + list(node_coords[3 * (tag - 1):3 * tag]) for tag in node_tags]
        self.elements = [[tag] + list(element_node_tags[i]) for i, tag in enumerate(element_tags)]

        gmsh.finalize()
        nodes = np.array(self.nodes) * mesh_size
        elements = np.array(self.elements)