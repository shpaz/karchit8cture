import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint

class KubernetesApiClient:
    def __init__(self, api_token, host):
        self.configuration = client.Configuration()
        self.configuration.host = host
        self.configuration.api_key_prefix['authorization'] = 'Bearer'
        self.configuration.verify_ssl=False

        if api_token:
            self.configuration.api_key['authorization'] = api_token

        self.api_client = client.ApiClient(self.configuration)

class CoreV1ApiClient(KubernetesApiClient):
    def __init__(self, api_token, host):
        super().__init__(api_token, host)
        self.core_v1_api = client.CoreV1Api(self.api_client)

    def list_pod_for_all_namespaces(self):
        try:
            api_response = self.core_v1_api.list_pod_for_all_namespaces()
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)
    
    def list_namespaced_pod(self, namespace="default"):
        try:
            api_response = self.core_v1_api.list_namespaced_pod(namespace)
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
            

if __name__ == "__main__":
    # Read configuration from YAML file
    with open("k8s_config.yaml", "r") as yaml_file:
        config_data = yaml.safe_load(yaml_file)

    # Instantiate the core_v1_api with the configuration from the YAML file
    core_v1_api = CoreV1ApiClient(api_token=config_data.get('api_token'), host=config_data.get('host'))
    # Make API calls using the methods of KubernetesApiClient
    result1 = core_v1_api.list_pod_for_all_namespaces()
    #result2 = core_v1_api.list_namespaced_pod('kube-system')
    pprint(result1)
