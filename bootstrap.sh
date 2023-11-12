#!/bin/bash

# Making sure we have no leftover values from previous installations
unset TOKEN 
unset K8S_HOST

# Function to deploy Kubernetes cluster
deploy_k8s_cluster() {
  # Creating a kind cluster, according to a pre-defined kind.yaml config file 
  kind create cluster --name playground --config manifests/kind.yaml 
  sleep 10 

  # Labels nodes as they're bootstrapped with no worker node role 
  kubectl get nodes | grep worker | awk '{print$1}' | xargs -I {} kubectl label node {} node-role.kubernetes.io/worker=worker --overwrite
  sleep 5 
}
apply_manifests() {
  # Applies all relevant manifests for the stratup of the cluster and execution of karchit8cture.py 
  kubectl apply -f manifests/01-namespace.yaml
  kubectl apply -f manifests/02-service-account.yaml
  kubectl apply -f manifests/03-clusterrolebinding.yaml
  kubectl apply -f manifests/04-secret.yaml
}
apply_tests() {
  # Applies all manifests relevant for testing extra tests that are not there in default 
  kubectl apply -f tests/
}
setup_kube_access() {
  # Changes k8s_config.yaml values to suite to craeted service account's
  export K8S_HOST=$(kubectl cluster-info --context kind-playground | grep "control plane" | grep -oP 'https:\/\/\d+\.\d+\.\d+\.\d+:\d+')
  export TOKEN=$(kubectl get secrets karchit8cture -n karchit8cture -o jsonpath='{.data.token}' | base64 -d)
  sed -i "s/api_token: .*/api_token: ${TOKEN}/" karchit8cture/k8s_config.yaml
  sed -i "s#host: .*#host: ${K8S_HOST}#" karchit8cture/k8s_config.yaml
}
# Prompt the user
read -p "Do you want to deploy Kubernetes? (yes/no): " answer

# Check if the argument is provided and is "yes" or "y"
if [ "$answer" == "yes" ] || [ "$answer" == "y" ]; then
  deploy_k8s_cluster
  apply_manifests
  setup_kube_access
  echo "Installation Finished Successfully"
else
  echo "Kubernetes deployment skipped."
  apply_manifests
  setup_kube_access
fi
