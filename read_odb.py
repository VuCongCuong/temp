import sys
import pickle
import numpy as np

import odbAccess
from abaqusConstants import *

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

def update_range(nodes):
    node_data = np.array(nodes)
    xrange = [np.min(node_data[:, 1]), np.max(node_data[:, 1])]
    yrange = [np.min(node_data[:, 2]), np.max(node_data[:, 2])]
    zrange = [np.min(node_data[:, 3]), np.max(node_data[:, 3])]
    # convert numpy to float
    xrange = [float(i) for i in xrange]
    yrange = [float(i) for i in yrange]    
    zrange = [float(i) for i in zrange]
    return [xrange, yrange, zrange]

def get_result(filepath, part_name):
    base_information = []
    
    try:    
        odb         = odbAccess.openOdb(filepath)
        instance    = odb.rootAssembly.instances['BASE']
        elements    = instance.elements

        # Access the first step
        step_name   = odb.steps.keys()[-1]
        step        = odb.steps[step_name]
        for i, frame in enumerate(step.frames):
            extract_datas = {}
            # Create dictionaries to map element data
            status_map  = {value.elementLabel: value.data for value in frame.fieldOutputs['STATUS'].getSubset(region=instance).values}
            stress_map  = {value.elementLabel: value.data for value in frame.fieldOutputs['S'].getSubset(region=instance).values}
            pls_map     = {value.elementLabel: value.data for value in frame.fieldOutputs['PE'].getSubset(region=instance).values}
            damage_map  = {value.elementLabel: value.data for value in frame.fieldOutputs['PEEQ'].getSubset(region=instance).values}
            coord_map   = {value.nodeLabel: value.data for value in frame.fieldOutputs['COORD'].getSubset(region=instance).values}  
            temp_map    = {value.nodeLabel: value.data for value in frame.fieldOutputs['NT11'].getSubset(region=instance).values}
            vel_map     = {value.nodeLabel: value.data for value in frame.fieldOutputs['V'].getSubset(region=instance).values}  
            acc_map     = {value.nodeLabel: value.data for value in frame.fieldOutputs['A'].getSubset(region=instance).values}
            force_map   = {value.nodeLabel: value.data for value in frame.fieldOutputs['RF'].getSubset(region=instance).values}

        
            # Prepare a dictionary to store the element data
            list_of_element = []
            list_of_active_node = []
            
            # Optional: Convert sets back to lists if needed
            node_clusters, element_clusters = cluster_elements_optimized(elements, status_map, min_cluster_size=100)
        
            # Iterate through elements and map the data
            for element in elements:
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
            
            
            extract_datas['nodes'] = [[label, *coord_map[label], temp_map[label], 
                            *vel_map[label], *acc_map[label], 
                            *force_map[label]] for label in list_of_active_node]
            extract_datas['elements']  = [[*ele, *stress_map[ele[0]], *pls_map[ele[0]], 
                                damage_map[ele[0]], status_map[ele[0]]] for ele in list_of_element]
            base_information.append(extract_datas.copy()) # append the data to the list
            # update part range
            with open('result_step=' + str(i) + '.json', 'wb') as file:
                pickle.dump(extract_datas, file)

        odb.close()
        return base_information
        
    except FileNotFoundError: 
        print(f"File '{filepath}' not found.")


get_result('Grind_0.odb')
sys.exit()
