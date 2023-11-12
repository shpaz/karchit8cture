from kubeapiclient import KubernetesApiClient
import kubernetes
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

class CoreV1ApiClient(KubernetesApiClient):
    def __init__(self, api_token, host):
        super().__init__(api_token, host)
        self.core_v1_api = client.CoreV1Api(self.api_client)

    def check_kubesystem_pods(self):
        try:
            api_response = self.core_v1_api.list_namespaced_pod(namespace='kube-system')
            for pod in api_response.items:
                if pod.status.phase != "Running":
                    return False
        except ApiException as e:
            print("Exception when calling CoreV1Api->List Pods in kube-system namespace: %s\n" % e)
        return True
    
    def check_default_pods_existence(self):
        try:
            api_response = self.core_v1_api.list_namespaced_pod(namespace='default')
            if len(api_response.items) > 0:
                return False
        except ApiException as e:
            print("Exception when calling CoreV1Api->Pods exist in default namespace: %s\n" % e)
        return True    
    def check_node_readiness(self):
        try:
            # Make sure to gather all nodes' status 
            api_response = self.core_v1_api.list_node()
            for node in api_response.items:
                if node.status.conditions[3].status != "True":
                    return False
        except Exception as e:
            print(f"Error while checking node readiness: {str(e)}")    
        return True

    def check_control_plane_count(self):
        minimum_control_plane_nodes = 3 # In an HA based cluster, minimum number is 3 
        try:
            # Return flase if control plane node count is less than 3
            api_response = self.core_v1_api.list_node(label_selector='node-role.kubernetes.io/control-plane')
            if len(api_response.items) < minimum_control_plane_nodes:
                return False
        except Exception as e:
            print(f"Error while checking control plane nodes count: {str(e)}")
        return True

    def check_data_plane_count(self):
        minimum_data_plane_nodes = 2 # In an HA based cluster, minimum number is 3 
        try:
            # Return false if data plane node count is less than 2
            api_response = self.core_v1_api.list_node(label_selector='node-role.kubernetes.io/worker')
            if len(api_response.items) < minimum_data_plane_nodes:
                return False
        except Exception as e:
            print(f"Error while checking data plane nodes count: {str(e)}")  
        return True

    def verify_hardware_capacity(self):

        min_memory = 16 
        min_cpu = 4
        try:
            # Make sure to gather all nodes' status 
            api_response = self.core_v1_api.list_node()
            for node in api_response.items:
               memory = int(node.status.capacity['memory'].rstrip("Ki")) / (1000**2) 
               cpu = int(node.status.capacity['cpu'])

               # Return false if node capacity is less than expected 
               if memory < min_memory or cpu < min_cpu:
                return False
        except Exception as e:
            print(f"Error while checking node capacity resources: {str(e)}")
        return True

### reference the check https://docs.openshift.com/container-platform/4.10/authentication/remove-kubeadmin.html
    def check_default_kubeadmin_user(self):
        try:
            api_response = self.core_v1_api.read_namespaced_secret(namespace='kube-system', name='kubeadmin')
            if api_response:
                return False
        except ApiException as e:
            pass
        return True
    
