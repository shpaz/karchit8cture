import kubernetes
from kubernetes import client, config

def check_kubesystem_pods(v1):
    try:
        # Make sure to check if all kube-system pods are up and running 
        for pod in v1.items: 
          if pod.status.phase != "Running":
            return False
    except Exception as e:
        print(f"Error while checking kube-system pod status: {str(e)}")    
    return True

def check_default_pods_existence(v1):
    try:
        # Make sure to check if all kube-system pods are up and running 
        if len(v1.items) > 0:
          return False
    except Exception as e:
        print(f"Error while checking default namespace pod existence: {str(e)}")    
    return True