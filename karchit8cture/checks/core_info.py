import kubernetes
from kubernetes import client, config

def check_node_readiness(v1):

    try:
        # Make sure to gather all nodes' status 
        for node in v1.items:
            if node.status.conditions[3].status != "True":
                return False

    except Exception as e:
        print(f"Error while checking node readiness: {str(e)}")
    
    return True

def check_control_plane_count(v1):

    minimum_control_plane_nodes = 3 # In an HA based cluster, minimum number is 3 

    try:
        # Return flase if control plane node count is less than 3
        if len(v1.items) < minimum_control_plane_nodes:
            return False

    except Exception as e:
        print(f"Error while checking control plane nodes count: {str(e)}")
    
    return True

def check_data_plane_count(v1):

    minimum_data_plane_nodes = 2 # In an HA based cluster, minimum number is 3 

    try:
        # Return false if data plane node count is less than 2
        if len(v1.items) < minimum_data_plane_nodes:
            return False

    except Exception as e:
        print(f"Error while checking data plane nodes count: {str(e)}")
    
    return True
def verify_hardware_capacity(v1):

    min_memory = 16 
    min_cpu = 4

    try:
        # Make sure to gather all nodes' status 
        for node in v1.items:
           memory = int(node.status.capacity['memory'].rstrip("Ki")) / (1000**2) 
           cpu = int(node.status.capacity['cpu'])

           # Return false if node capacity is less than expected 
           if memory < min_memory or cpu < min_cpu:
            return False

    except Exception as e:
        print(f"Error while checking node capacity resources: {str(e)}")
    
    return True