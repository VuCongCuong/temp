import numpy as np

from scipy.spatial import ConvexHull
from scipy.stats import uniform
from  model.material import Material, JonhsonCook


class Part():

    def __init__(self, name):
        self.name           = name
        self.nodes          =  {}
        self.elements       =  {}
        self.set            =  {}
        self.mat            = None
        
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
        return self.set[label_list]
    
    def assign_material(self, material: JonhsonCook):
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

        self.initial_stress         = {}
        self.initial_plstrain       = {}
        self.initial_damage         = {}
        self.initial_temperature    = {}
        

        

        


class Grain(Part):
    def __init__(self, name, number_of_vertices):
        super().__init__(name)
        self.gen_convex_hull_grain(number_of_vertices)
        self.translate = [0, 0, 0]

    def gen_rand_translate(self, xrange, yrange, zrange):
        
        # make x ranger only from -2 to -1
        xrange = [xrange[0]-60, xrange[0]-40]
        x = uniform.rvs(loc=xrange[0], scale=xrange[1]-xrange[0])

        y = yrange[0] + 0.5 * (yrange[1] - yrange[0])  # y tại 50% vùng Y
        
        # scale z range 20 % on top
        zrange[0] = zrange[1] - (zrange[1]-zrange[0])*0.2
        z = uniform.rvs(loc=zrange[0], scale=zrange[1]-zrange[0])
        z = zrange[1]   # some testings
        self.translate = [x, y, z]       


    def assign_translate_position(self, xrange, yrange, zrange, total_grains=1, index=0):
        """
        Gán vị trí dịch chuyển cụ thể cho một hạt mài (grain).

        Parameters:
        - grain: đối tượng Grain.
        - xrange, yrange, zrange: danh sách [min, max] của phôi theo từng trục.
        - total_grains: tổng số hạt.
        - index: thứ tự của hạt (0-based).
        """

        # Gán X: nằm bên trái phôi, cách từ 100 đến 150 đơn vị
        x = (xrange[0] - 50)

        # Gán Y:
        if total_grains == 1:
            y = yrange[0] + 0.5 * (yrange[1] - yrange[0])
        else:
            step_y = (yrange[1] - yrange[0]) / (total_grains)
            y = yrange[0] + (index + 0.5) * step_y

        # Gán Z: nằm ngay mặt trên của phôi
        z = zrange[1]

        # Lưu lại
        self.translate = [x, y, z]


    def assign_translate_position_plus_n(self, xrange, yrange, zrange, total_grains=1, index=0, spacing=1.0):
        """
        Gán vị trí dịch chuyển cho một hạt, với khoảng cách Y tăng dần theo index.

        Parameters:
        - spacing: đơn vị khoảng cách n (float)
        """

        # Gán X: lệch trái phôi
        x = xrange[0] - 50

        # Tính vị trí Y tăng dần
        step_y = (yrange[1] - yrange[0]) / (total_grains) # hoặc dùng trực tiếp yrange[0]
        y = yrange[0] + (spacing * index) + step_y * (index + 0.5)

        # Gán Z: mặt trên phôi
        z = zrange[1]

        # Cập nhật vị trí
        self.translate = [x, y, z]


        
    def _gen_rand_spherical_points(self, num_points):
        rng = np.random.default_rng()
        theta = rng.uniform(0, 2 * np.pi, num_points)  # Azimuthal angle
        phi = rng.uniform(0, np.pi, num_points)         # Polar angle

        # Convert spherical coordinates to Cartesian coordinates
        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)

        points = np.column_stack((x, y, z))*50 # scale the grain
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
        


        nodes = [ [i] + list(node) for i, node in enumerate(points, start=1) ]
        elements = [ [i] + list(element+1) for i, element in enumerate(hull.simplices, start=1) ]
        
        # calculate the center of the grain
        center = np.mean(np.array(nodes)[:,1:4], axis=0)

        # make sure the normal is outwards
        for ele in elements:
            normal = np.cross(points[ele[2]-1] - points[ele[1]-1], points[ele[2]-1] - points[ele[3]-1])
            normal = normal / np.linalg.norm(normal)  # Normalize the normal vector
            c = np.mean(np.array([points[ele[1]-1], points[ele[2]-1], points[ele[3]-1]]), axis=0)

            if np.dot(normal, c-center) < 0:
                tmp = ele[1]
                ele[1] = ele[2]  # Reverse the element if the normal is pointing inwards
                ele[2] = tmp

                elements[ele[0]-1]  = ele
        
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