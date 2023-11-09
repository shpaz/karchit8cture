import kubernetes
from kubernetes import client, config
import checks.core_info as core_info

def validate_k8s_cluster():
    try:
        # Load the Kubernetes configuration from your kubeconfig file
        config.load_kube_config()

        # Create a Kubernetes API client
        v1 = client.CoreV1Api()

        results = {
            "Node Readiness": core_info.check_node_readiness(v1),
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