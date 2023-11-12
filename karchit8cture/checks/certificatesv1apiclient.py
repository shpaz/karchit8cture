from kubeapiclient import KubernetesApiClient
import kubernetes
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

class CertificatesV1ApiClient(KubernetesApiClient):
    def __init__(self, api_token, host):
        super().__init__(api_token, host)
        self.certificates_v1_api = client.CertificatesV1Api(self.api_client)

    '''This function checks whether there are any CSRs in pending state'''
    def check_for_pending_csrs(self):
        try:
            api_response = self.certificates_v1_api.list_certificate_signing_request()
            for csr in api_response.items:
                if csr.status.conditions[0].type != "Approved":
                    return False
        except ApiException as e:
            print("Exception when calling CoreV1Api->Couldn't look our for pending CSRs: %s\n" % e)
        return True