import kubernetes
from kubernetes import client, config
import checks.core_info as core_info

def validate_k8s_cluster():
    try:
        # Load the Kubernetes configuration from your kubeconfig file
        config.load_kube_config()

        # Create a Kubernetes API client for nodes information gathering 
        nodes_v1 = client.CoreV1Api().list_node()

        # Collect results by executing a different check each time 
        results = {
            "Node Readiness": core_info.check_node_readiness(nodes_v1),
            "Minimum Control Plane Nodes": 
                core_info.check_control_plane_count(client.CoreV1Api().
                                                    list_node(label_selector='node-role.kubernetes.io/control-plane')),
            "Minimum Data Plane Nodes": 
                core_info.check_data_plane_count(client.CoreV1Api().
                                                    list_node(label_selector='node-role.kubernetes.io/worker')),
            "Node Capacity": core_info.verify_hardware_capacity(nodes_v1),
        }
        return results

    except Exception as e:
        print(f"Error while creating the Kubernetes context: {str(e)}")
        return {"error": True}

if __name__ == "__main__":
    validation_results = validate_k8s_cluster()

    print("Validation Results:")
    for check, result in validation_results.items():
        print(f"{check}: {'Passed' if result else 'Failed'}")