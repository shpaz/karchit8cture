import yaml
import kubernetes
from kubernetes import client, config
import checks.core_node_info as core_node_info
import checks.core_pod_info as core_pod_info

def validate_k8s_cluster():
    try:
      # Load both bearer token and kubernetes host from a config file
      with open("../manifests/k8s_config.yaml", "r") as yaml_file:
        config_data = yaml.safe_load(yaml_file)

        # Load the Kubernetes configuration according to a pre-created service account bearer token 
        configuration = client.Configuration()
        configuration.api_key['authorization'] = config_data.get('api_token')
        configuration.api_key_prefix['authorization'] = 'Bearer'
        configuration.host = 'https://localhost:35675'
        configuration.verify_ssl=False
        api_client = client.ApiClient(configuration)

        # Create a Kubernetes API client for nodes information gathering 
        nodes_v1 = client.CoreV1Api(api_client).list_node()
        pods_v1 = client.CoreV1Api(api_client)

        # Collect results by executing a different check each time 
        results = {
            "Node Readiness": core_node_info.check_node_readiness(nodes_v1),
            "Minimum Control Plane Nodes": 
                core_node_info.check_control_plane_count(client.CoreV1Api().
                                                    list_node(label_selector='node-role.kubernetes.io/control-plane')),
            "Minimum Data Plane Nodes": 
                core_node_info.check_data_plane_count(client.CoreV1Api().
                                                    list_node(label_selector='node-role.kubernetes.io/worker')),
            "Node Capacity": core_node_info.verify_hardware_capacity(nodes_v1),
            "Kube System Pods": core_pod_info.check_kubesystem_pods(pods_v1.list_namespaced_pod('kube-system')),
            "Default Namespace Pods Existence": core_pod_info.check_default_pods_existence(pods_v1.list_namespaced_pod('default')),
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