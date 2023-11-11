from kubernetes import client

class KubernetesApiClient:
    def __init__(self, api_token, host):
        self.configuration = client.Configuration()
        self.configuration.host = host
        self.configuration.api_key_prefix['authorization'] = 'Bearer'
        self.configuration.verify_ssl = False

        if api_token:
            self.configuration.api_key['authorization'] = api_token

        self.api_client = client.ApiClient(self.configuration)