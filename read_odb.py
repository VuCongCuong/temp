import sys
import pickle
import numpy as np

import odbAccess
from abaqusConstants import *
from model.merge_node import cluster_elements_optimized

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
