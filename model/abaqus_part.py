import gmsh
import meshio
import numpy as np
import pyvista as pv
from matplotlib import cm


from scipy.stats import uniform
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize
from itertools import combinations, permutations
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from model.merge_node import UnionFind, cluster_elements
from  model.material import Material

import matplotlib.pyplot as plt

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
    
    def create_set(self, name: str, element_list: list):
        """
        Create a set with the given name.
        """
        if name in self.set:
            print(f"Set {name} already exists. Overwriting.")

        self.set[name] = element_list
        print(f"Set {name} created.")
        
        return 0
        

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
        
        self.node_neighbor = {}
        self.prj_pts = []

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
        cells = [("triangle", np.array([[node_id - 1 for node_id in element[1:]] 
                                        for element in self.elements]))]  # Adjust indices to be zero-based
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
                                        force_parametrizable_patches, 
                                        curve_angle * 3.14159 / 180.)

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

        
        # Extract the mesh data back into nodes and elements
        node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
        
        self.nodes = [[int(tag)] + list(coord) for tag, coord in zip(node_tags, node_coords.reshape(-1, 3))]
        element_types, element_tags, node_tags = gmsh.model.mesh.getElements(dim=3)
        self.elements = []
        
        for i in range(len(element_tags[0])):
            index1 = element_types[0]*i
            index2 = element_types[0]*(i+1)
            self.elements.append([i+1, *node_tags[0][index1:index2]])
        
        gmsh.finalize()    
    
    def get_outer_faces(self):
        outer_face_dict = {}
        for element in self.elements:
            for i, comb in enumerate((combinations(element[1:], 3))): # 3 points random point alway form a plane
                trigger = False
                for perm in permutations(comb):
                    if outer_face_dict.get(perm):
                        trigger = True
                        del outer_face_dict[perm]
                        break
                if not trigger:
                    outer_face_dict[perm] = [comb, element, i]
        
        self.create_set('OUTER_FACE', [ele[1][0] for ele in outer_face_dict.values()])
        self.create_set('OUTER_FACE_S1', [ele[1][0] for ele in outer_face_dict.values() if ele[2] == 0])
        self.create_set('OUTER_FACE_S2', [ele[1][0] for ele in outer_face_dict.values() if ele[2] == 1])
        self.create_set('OUTER_FACE_S3', [ele[1][0] for ele in outer_face_dict.values() if ele[2] == 3])
        self.create_set('OUTER_FACE_S4', [ele[1][0] for ele in outer_face_dict.values() if ele[2] == 2])
        return outer_face_dict
    
    def sel_outer_node_by_dir(self, x, y, z):        
        # Define the direction vector and normalize it
        dir_vector = np.array([x, y, z], dtype=np.float64)
        dir_vector /= np.linalg.norm(dir_vector)
        outer_face_dict = self.get_outer_faces()

        uf = UnionFind()
        outer_nodes = []
        node_coords = []
        boundary = []

        # find the neighbor of each node
        for face, _, __ in outer_face_dict.values():
            for node in face:
                if (node-1) not in self.node_neighbor:
                    self.node_neighbor[node-1] = []
                self.node_neighbor[node-1].extend([node-1 for node in face])
            outer_nodes.extend(face)  # Add all node indices from the face
        outer_nodes = sorted(set(outer_nodes))  # Remove duplicates and sort
       
        for node, conn in self.node_neighbor.items():
            self.node_neighbor[node] = sorted(set(conn))

        for node in outer_nodes:
            node_coords.append(self.nodes[node-1])  # Convert to zero-based indexing if necessary

        # Project node coordinates to plane perpendicular which go through (0, 0, 0) to dir_vector
        
        for point in node_coords:
            point = point[1:]
            self.prj_pts.append(np.array(point) - dir_vector * np.dot(np.array(point), dir_vector))
        self.prj_pts = np.array(self.prj_pts)
        index = [1, 2]
        if y == z == 0: index = [1, 2]
        elif x == z == 0: index == [0, 2]
        elif z == y == 0: index == [0, 1]
        
        hull = ConvexHull(self.prj_pts[:, index])  # Use all projected points to construct the convex hull
        simplices = hull.simplices.tolist()
        if simplices:
            ordered_simplices = [simplices.pop(0)]
            while simplices:
                last = ordered_simplices[-1][1]
                for i, s in enumerate(simplices):
                    if s[0] == last:
                        ordered_simplices.append(s)
                        simplices.pop(i)
                        break
                    elif s[1] == last:
                        ordered_simplices.append([s[1], s[0]])
                        simplices.pop(i)
                        break
            hull.simplices = np.array(ordered_simplices)
        
        boundary.append(hull.simplices[0][0]) # Init the start point of the boundary
        for simplice in hull.simplices:
            A = simplice[0]
            B = simplice[1]
            boundary = self._find_hull_boundary(A, A, B, boundary, hull.simplices[0][0])

        for node, neighbor in self.node_neighbor.items():
            if node not in boundary:
                # Remove all boundary nodes from neighbor list
                neighbor = [n for n in neighbor if n not in boundary]
                for node in neighbor:
                    uf.add(node)  # Ensure all nodes are in Union-Find
                for i in range(len(neighbor) - 1):
                    uf.union(neighbor[i], neighbor[i + 1])
        
        # Calculate the center for each cluster
        clusters = uf.get_all()
        cluster_centers = []
        for cluster in clusters:
            if not cluster:
                cluster_centers.append(None)
                continue
            cluster_coords = np.array([self.nodes[int(node)][1:] for node in cluster])
            center = np.mean(cluster_coords, axis=0)
            cluster_centers.append(center)
        
        center_dir = cluster_centers[1] - cluster_centers[0]
        
        uf1 = UnionFind()
        for face, ele, S_id in outer_face_dict.values():
            if all((conn-1) not in boundary for conn in face):
                for node in face:
                    uf1.add(node)
                for i in range(len(face) - 1):
                    uf1.union(face[i], face[i + 1])
        face_clusters = uf1.get_all()
        elemenet_clusters = [[] for _ in range(len(face_clusters))]
        for i, face_cluster in enumerate(face_clusters):
            for face, ele, S_id in outer_face_dict.values():
                if all(node in face_cluster for node in face):
                    elemenet_clusters[i].append([face, S_id, ele[0]])

            
        # Find the center of each element cluster
        element_cluster_centers = []
        for cluster in elemenet_clusters:
            # cluster is a list of [face, S_id], so extract all node indices from faces
            node_indices = set()
            for face, _, __ in cluster:
                node_indices.update(face)
            cluster_coords = np.array([self.nodes[int(node)-1][1:] for node in node_indices])
            center = np.mean(cluster_coords, axis=0)
            element_cluster_centers.append(center)
        center_dir2 = element_cluster_centers[1] - element_cluster_centers[0]

        if np.dot(center_dir2, dir_vector)>0:
            self.create_set("FONT_ELSET", [ele for face, S_id, ele in elemenet_clusters[0]])
            self.create_set("BACK_ELSET", [ele for face, S_id, ele in elemenet_clusters[1]])
            self.create_set("FONT_S1_ELSET", [ele for face, S_id, ele in elemenet_clusters[0] if S_id == 0])
            self.create_set("FONT_S2_ELSET", [ele for face, S_id, ele in elemenet_clusters[0] if S_id == 1])
            self.create_set("FONT_S3_ELSET", [ele for face, S_id, ele in elemenet_clusters[0] if S_id == 3])
            self.create_set("FONT_S4_ELSET", [ele for face, S_id, ele in elemenet_clusters[0] if S_id == 2])
            self.create_set("BACK_S1_ELSET", [ele for face, S_id, ele in elemenet_clusters[1] if S_id == 0])
            self.create_set("BACK_S2_ELSET", [ele for face, S_id, ele in elemenet_clusters[1] if S_id == 1])
            self.create_set("BACK_S3_ELSET", [ele for face, S_id, ele in elemenet_clusters[1] if S_id == 3])
            self.create_set("BACK_S4_ELSET", [ele for face, S_id, ele in elemenet_clusters[1] if S_id == 2])
        else:
            self.create_set("FONT_ELSET", [ele for face, S_id, ele in elemenet_clusters[1]])
            self.create_set("BACK_ELSET", [ele for face, S_id, ele in elemenet_clusters[0]])
            self.create_set("FONT_S1_ELSET", [ele for face, S_id, ele in elemenet_clusters[1] if S_id == 0])
            self.create_set("FONT_S2_ELSET", [ele for face, S_id, ele in elemenet_clusters[1] if S_id == 1])
            self.create_set("FONT_S3_ELSET", [ele for face, S_id, ele in elemenet_clusters[1] if S_id == 3])
            self.create_set("FONT_S4_ELSET", [ele for face, S_id, ele in elemenet_clusters[1] if S_id == 2])
            self.create_set("BACK_S1_ELSET", [ele for face, S_id, ele in elemenet_clusters[0] if S_id == 0])
            self.create_set("BACK_S2_ELSET", [ele for face, S_id, ele in elemenet_clusters[0] if S_id == 1])
            self.create_set("BACK_S3_ELSET", [ele for face, S_id, ele in elemenet_clusters[0] if S_id == 3])
            self.create_set("BACK_S4_ELSET", [ele for face, S_id, ele in elemenet_clusters[0] if S_id == 2])

        if np.dot(center_dir, dir_vector) > 0:
            tmp = [node+1 for node in clusters[0]]
            self.create_set("VEL_NSET", tmp)
            return clusters[0]
        else:
            tmp = [node+1 for node in clusters[1]]
            self.create_set("VEL_NSET", tmp)
            return clusters[1] 
        
        


    
    def _find_hull_boundary(self, current, pt_start, pt_end, visited, start):
        potential = {}
        for conn in self.node_neighbor[current]:
            if conn == pt_end:
                if pt_end == start: # end of the search
                    visited.append(conn)
                    return visited
                if conn not in visited:
                    visited.append(conn)
                return visited
            if (conn == current) or (conn in visited):
                continue

            # Calculate the distance from conn to the line through start and end
            direction = self.prj_pts[pt_end] - self.prj_pts[pt_start]
            direction = direction / np.linalg.norm(direction)
            point_vec = self.prj_pts[conn] - self.prj_pts[pt_start]
            point_rel = self.prj_pts[conn] - self.prj_pts[current]
            # ignore if this direction is not the same as the direction
            if np.dot(point_rel, direction) < 0:
                continue
            proj_len = np.dot(point_vec, direction)
            proj_point = self.prj_pts[pt_start] + proj_len * direction
            dist_to_line = np.linalg.norm(self.prj_pts[conn] - proj_point)
            if potential.get(current) is None:
                potential[current] = []
            potential[current].append([conn, dist_to_line])

        if len(potential[int(current)]) == 0:
            return visited  # Prevent infinite recursion if no valid next node
        
        potential[current].sort(key=lambda x: x[1])
        visited.append(potential[current][0][0])
        return self._find_hull_boundary(potential[current][0][0], pt_start, pt_end, visited, start)

    def _plot_boundary_cluster(self, clusters, boundary):
        
        # Plot all outer faces and boundary in the same 3D image
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        ax.view_init(elev=90, azim=-90)
        # Plot node_neighbor connections as gray lines
        for node, neighbors in self.node_neighbor.items():
            node_coord = self.nodes[node][1:]
            for neighbor in neighbors:
                neighbor_coord = self.nodes[neighbor][1:]
                ax.plot([node_coord[0], neighbor_coord[0]],
                        [node_coord[1], neighbor_coord[1]],
                        [node_coord[2], neighbor_coord[2]],
                        color='gray', linewidth=0.5, alpha=1)
        
        boundary_coords = np.array([self.nodes[int(node)][1:] for node in boundary])
        ax.plot(boundary_coords[:, 0], boundary_coords[:, 1], boundary_coords[:, 2], c='r', linewidth=2, label='Boundary')
        # Plot boundary points as red dots
        ax.scatter(boundary_coords[:, 0], boundary_coords[:, 1], boundary_coords[:, 2], c='r', s=50, label='Boundary Points')
        # Plot all clusters of merge_nodes
    
        
        colors = [ 'b', 'g', 'y', 'k']
        for idx, cluster in enumerate(clusters):
            if not cluster:
                continue
            cluster_coords = np.array([self.nodes[int(node)][1:] for node in cluster])
            ax.scatter(cluster_coords[:, 0], cluster_coords[:, 1], cluster_coords[:, 2],
                       color=colors[idx % len(colors)], label=f'Cluster {idx+1}')
            # Plot edge connections within the cluster
            plt.savefig(f'connected_cluster_{idx}_00.png')
            for i, node in enumerate(cluster):
                node_coord = self.nodes[int(node)][1:]
                for neighbor in self.node_neighbor[node]:
                    neighbor_coord = self.nodes[neighbor][1:]
                    ax.plot([node_coord[0], neighbor_coord[0]],
                            [node_coord[1], neighbor_coord[1]],
                            [node_coord[2], neighbor_coord[2]],
                            color=colors[idx % len(colors)], linewidth=1, alpha=0.7)
                plt.savefig(f'connected_cluster_{idx}_{i}.png')
        plt.show()
        
        # Assign a unique color to each face using a colormap
        # import matplotlib.colors as mcolors

        # num_faces = len(outer_face_dict)
        # cmap = cm.get_cmap('viridis', num_faces)
        # for idx, value in enumerate(outer_face_dict.values()):
        #     face = value[0]
        #     face_nodes = np.array([self.nodes[node-1][1:] for node in face])
        #     color = cmap(idx)
        #     poly = Poly3DCollection([face_nodes], alpha=0.2, edgecolor='k', facecolor='cyan')
        #     ax.add_collection3d(poly)    
        # outer_coords = np.array([self.nodes[node-1][1:] for node in outer_nodes])
        # ax.scatter(outer_coords[:, 0], outer_coords[:, 1], outer_coords[:, 2], c='b', label='Outer Nodes')

        # Plot boundary as a closed loop
       
        
        # plt.show()
        # print("okk")

    def plot_projected_convex_hull_and_boundary(self, prj_pts, hull, boundary, node_neighbor):

        # Plot the projected convex hull and boundary
        fig, ax = plt.subplots(figsize=(8, 6))
        # Plot all projected points
        ax.scatter(prj_pts[:, 0], prj_pts[:, 1], color='blue', label='Projected Nodes')
        # Add node ids to the points
        # for idx, (x, y) in enumerate(prj_pts[:, 0:2]):
        #     ax.text(x, y, str(idx), fontsize=8, color='black', ha='center', va='center')    
        # Plot convex hull
        for simplex in hull.simplices:
            ax.plot(prj_pts[simplex, 0], prj_pts[simplex, 1], 'g--', linewidth=0.5)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend()

        for i, node in enumerate(boundary):
            node_idx = int(node)
            if node_idx < 0 or node_idx >= len(prj_pts):
                continue

            ax.scatter(prj_pts[node_idx][0], prj_pts[node_idx][1], color='red')
            for neighbor in node_neighbor[node_idx]:
                neighbor_idx = int(neighbor)
                if neighbor_idx < 0 or neighbor_idx >= len(prj_pts):
                    continue
                x = [prj_pts[node_idx][0], prj_pts[neighbor_idx][0]]
                y = [prj_pts[node_idx][1], prj_pts[neighbor_idx][1]]
                ax.plot(x, y, 'k-', linewidth=0.5)
            
            plt.savefig(f'projected_convex_hull_boundary_step_{2*i}.png')
            next_idx = int(boundary[(i+1) % len(boundary)])
            if next_idx < 0 or next_idx >= len(prj_pts):
                continue
            boundary_pts = np.array([prj_pts[node_idx], prj_pts[next_idx]])
            ax.plot(boundary_pts[:, 0], boundary_pts[:, 1], 'r-', lw=2, label='Boundary')
            ax.set_title(f'Projected Convex Hull and Boundary Step: {i}')
            plt.savefig(f'projected_convex_hull_boundary_step_{2*i+1}.png')
        # plt.show(block=True)


    


        



                        