import sys
import pickle
import numpy as np

import odbAccess
from abaqusConstants import *
from abaqus import session
import os


class UnionFind:
    """Union-Find (Disjoint-Set) implementation for clustering."""
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, node):
        """Find the root of the node with path compression."""
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        """Union two nodes by rank."""
        root1 = self.find(node1)
        root2 = self.find(node2)
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1

    def add(self, node):
        """Add a new node."""
        if node not in self.parent:
            self.parent[node] = node
            self.rank[node] = 0

    def get_all(self):
        """Get all sets as a list of lists."""
        clusters = {}
        for node in self.parent:
            root = self.find(node)
            if root not in clusters:
                clusters[root] = []
            clusters[root].append(node)
        return list(clusters.values())
    

def cluster_elements_optimized(elements, status_map, min_cluster_size=100):
    """
    Optimized clustering of elements using Union-Find.
    
    Args:
        elements (list): List of elements with attributes `label` and `connectivity`.
        status_map (dict): A map of element labels to their status (e.g., active/inactive).
        min_cluster_size (int): Minimum number of elements in a cluster to keep.

    Returns:
        tuple: (node_clusters, element_clusters) after filtering.
    """
    # Initialize Union-Find structure
    uf = UnionFind()

    # Step 1: Union all nodes that belong to the same element
    for ele in elements:
        label = ele.label
        if not status_map[label]:
            continue  # Skip inactive elements
        conn = ele.connectivity
        for node in conn:
            uf.add(node)  # Ensure all nodes are in Union-Find
        for i in range(len(conn) - 1):
            uf.union(conn[i], conn[i + 1])

    # Step 2: Group nodes by their connected component root
    clusters = {}
    for node in uf.parent:
        root = uf.find(node)
        if root not in clusters:
            clusters[root] = set()
        clusters[root].add(node)

    # Step 3: Map nodes back to elements
    node_to_cluster = {node: root for root, nodes in clusters.items() for node in nodes}
    element_clusters = {}
    for ele in elements:
        label = ele.label
        if not status_map[label]:
            continue
        cluster_id = node_to_cluster[ele.connectivity[0]]  # Assume connectivity is non-empty
        if cluster_id not in element_clusters:
            element_clusters[cluster_id] = []
        element_clusters[cluster_id].append(label)

    # Step 4: Filter clusters by size
    element_clusters = [cluster for cluster in element_clusters.values() if len(cluster) > min_cluster_size]
    node_clusters = [list(nodes) for nodes in clusters.values() if len(nodes) > min_cluster_size]

    return node_clusters, element_clusters



def get_result(filepath):
    base_information = []
    
    try:    
        odb         = odbAccess.openOdb(filepath)
        instance_1    = odb.rootAssembly.instances['BASE']
        instance_2    = odb.rootAssembly.instances['G0']
        elements_1    = instance_1.elements
        # elements_2    = instance_2.elements


        global_max = -float('inf')
        global_min = float('inf')
        all_temps = []
        global_max_wp = -float('inf')


        # Access the first step
        step_name   = odb.steps.keys()[-1]
        step        = odb.steps[step_name]
        for i, frame in enumerate(step.frames):
            extract_datas = {}
            # Create dictionaries to map element data
            status_map  = {value.elementLabel: value.data for value in frame.fieldOutputs['STATUS'].getSubset(region=instance_1).values}
            # stress_map  = {value.elementLabel: value.data for value in frame.fieldOutputs['S'].getSubset(region=instance_1).values}
            # pls_map     = {value.elementLabel: value.data for value in frame.fieldOutputs['PE'].getSubset(region=instance_1).values}
            # damage_map  = {value.elementLabel: value.data for value in frame.fieldOutputs['PEEQ'].getSubset(region=instance_1).values}
            # coord_map   = {value.nodeLabel: value.data for value in frame.fieldOutputs['COORD'].getSubset(region=instance_1).values}  
            temp_map_1    = {value.nodeLabel: value.data for value in frame.fieldOutputs['NT11'].getSubset(region=instance_1).values}
            # vel_map     = {value.nodeLabel: value.data for value in frame.fieldOutputs['V'].getSubset(region=instance_1).values}  
            # acc_map     = {value.nodeLabel: value.data for value in frame.fieldOutputs['A'].getSubset(region=instance_1).values}
            # force_map   = {value.nodeLabel: value.data for value in frame.fieldOutputs['RF'].getSubset(region=instance_1).values}
            temp_map_2    = {value.nodeLabel: value.data for value in frame.fieldOutputs['NT11'].getSubset(region=instance_2).values}

            temp_2 = [value.data for value in frame.fieldOutputs['NT11'].getSubset(region=instance_2).values]
            temp_1 = [value.data for value in frame.fieldOutputs['NT11'].getSubset(region=instance_1).values]
                     
            list_of_element = []
            list_of_active_node = []
            # Optional: Convert sets back to lists if needed
            node_clusters, element_clusters = cluster_elements_optimized(elements_1, status_map, min_cluster_size=100)
        
            # Iterate through elements and map the data
            for element in elements_1:
                ele_label = element.label
                if ele_label in element_clusters[0]:
                    # Get status data for the element
                    status = status_map[ele_label]

                    if status: # ignore if element is not active
                        connectivity = element.connectivity
                        list_of_element.append([ele_label] + list(connectivity))
                        
                        for conn in connectivity:
                            list_of_active_node.append(conn)

            
            list_of_active_node = sorted(set(list_of_active_node))
            list_of_element = sorted(list_of_element)


            if temp_1:
                # Cập nhật global max/min
                global_max_wp = max(global_max_wp, max(temp_1))

            if temp_2:
                # Cập nhật global max/min
                global_max = max(global_max, max(temp_2))
                global_min = min(global_min, min(temp_2))
                all_temps.extend(temp_2)
            
            
                
            
            
            # Populate extract_datas with relevant results before pickling
            
            
            
        global_avg = sum(all_temps) / len(all_temps) if all_temps else None

        result = {
            'max_temp': global_max,
            'min_temp': global_min,
            'avg_temp': global_avg,
            'global_max_wp': global_max_wp,
        }

        with open('result_step=' + '.txt', 'w') as file:
            file.write(str(result))
        odb.close()
        return global_max, global_min, global_avg
        
    except FileNotFoundError: 
        print(f"File '{filepath}' not found.")
        return None, None, None



def get_all_odb_files(directory):
    return [f for f in os.listdir(directory) if f.lower().endswith('.odb')]




if __name__ == "__main__":
    current_dir = os.getcwd()
    odb_files = get_all_odb_files(current_dir)
    for odb_file in odb_files:
        get_result(os.path.join(current_dir, odb_file))
    get_result('Grind_0.odb')
    sys.exit()
    session.exit()
