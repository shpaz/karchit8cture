import kubernetes
from kubernetes import client, config

def check_node_readiness(v1):

    try:
        # Make sure to gather all nodes' status 
        nodes = v1.list_node()
        for node in nodes.items:
            if node.status.conditions[3].status != "True":
                return False

    except Exception as e:
        print(f"Error while checking node readiness: {str(e)}")
    
    return True

def check_node_crs(v1):

    try:
        # Make sure to gather all nodes' status 
        nodes = v1.list_node()
        for node in nodes.items:
            if node.status.conditions[3].status != "True":
                return False

    except Exception as e:
        print(f"Error while checking node readiness: {str(e)}")
    
    return True