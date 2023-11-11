#!/bin/bash

# Making sure we have no leftover values from previous installations
unset TOKEN 
unset K8S_HOST

# Creating a kind cluster, according to a pre-defined kind.yaml config file 
kind create cluster --name playground --config ../manifests/kind.yaml 
sleep 10 

# Labels nodes as they're bootstraped with no worker node role 
kubectl get nodes | grep worker | awk '{print$1}' | xargs -I {} kubectl label node {} node-role.kubernetes.io/worker=worker --overwrite
sleep 5 

# Creates a namespace and initializes a service account with a long-lived token 
kubectl create namespace karchit8cture
kubectl create serviceaccount karchit8cture -n karchit8cture

cat <<EOF | kubectl create -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
 name: karchit8cture
 labels:
   k8s-app: karchit8cture
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: karchit8cture
  namespace: karchit8cture
EOF

cat <<EOF | kubectl create -f -
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
 name: karchit8cture
 namespace: karchit8cture
 annotations:
   kubernetes.io/service-account.name: karchit8cture
EOF

# Changes k8s_config.yaml values to suite to craeted service account's
export K8S_HOST=$(kubectl cluster-info --context kind-playground | grep "control plane" | grep -oP 'https:\/\/\d+\.\d+\.\d+\.\d+:\d+')
export TOKEN=$(kubectl get secrets karchit8cture -n karchit8cture -o jsonpath='{.data.token}' | base64 -d)
sed -i "s/api_token: .*/api_token: ${TOKEN}/" ../manifests/k8s_config.yaml
sed -i "s#host: .*#host: ${K8S_HOST}#" ../manifests/k8s_config.yaml

