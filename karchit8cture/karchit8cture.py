import yaml
from pprint import pprint
from checks.corev1apiclient import CoreV1ApiClient
from checks.certificatesv1apiclient import CertificatesV1ApiClient

if __name__ == "__main__":
    # Read configuration from YAML file
    with open("k8s_config.yaml", "r") as yaml_file:
        config_data = yaml.safe_load(yaml_file)

    # Instantiate the core_v1_api with the configuration from the YAML file
    core_v1_api = CoreV1ApiClient(api_token=config_data.get('api_token'), host=config_data.get('host'))
    certificates_v1_api = CertificatesV1ApiClient(api_token=config_data.get('api_token'), host=config_data.get('host'))
    
    # Make API calls using the methods of KubernetesApiClient
    results = {
           "Node Readiness": core_v1_api.check_node_readiness(),
            "Minimum Control Plane Nodes": core_v1_api.check_control_plane_count(),
            "Minimum Data Plane Nodes": core_v1_api.check_data_plane_count(),
            "Node Capacity": core_v1_api.verify_hardware_capacity(),
            "Kube System Pods": core_v1_api.check_kubesystem_pods(),
            "Default Namespace Pods Existence": core_v1_api.check_default_pods_existence(),
            "Default kubeadmin secret exists": core_v1_api.check_default_kubeadmin_user(),
            "All PVCs are in Bound State": core_v1_api.check_all_persistent_volumes_bound(),
            "There are no pending CSRs": certificates_v1_api.check_for_pending_csrs(),
        }
    print("Validation Results:")
    for check, result in results.items():
        print(f"{check}: {'Passed' if result else 'Failed'}")
