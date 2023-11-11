# Kubernetes Architecture Analyzer (Karchit8cture)

karchit8cture (Kuberenetes Architecture) is a Kubernetes-native tool that will help platform administrators get a better understanding on whether their Kubernetes clusters are aligned with availability, scalability, durability and performance production demands.   

## Installation

In order to start interacting with `karchit8cture`, you can run the `bootstrap.sh` command, that will perform the following steps: 
* Create a `kind` based Kubernetes cluster for you, using the `manifests/kind.yaml` file 
* Apply all the manifests that are relevant for `karchit8cture` to interact with your Kubernetes cluster 
* Auto-edit the `karchit8cture/k8s_info.yaml` file, that as of now is being used by `karchit8cture.py` in order to fetch both Kubernertes host and API token 

Run the `bootstrap.sh` script: 
```bash
$ ./bootstrap.sh
```

Once you have all prerequisites met, you can run the following in order for `karchit8cture` to start testing your cluster: 
```bash
$ python3 karchit8cture.py
```

In case you want to work with `Python Virtual Envvironments (venv)`, make sure the follow the following procedure.

Create and activate a `venv` on your local computer:
```bash
$ python -m venv env
$ source env/bin/activate
```
Install needed depednecies for running `k8archit8cture`: 

```bash
$ pip3 install -r requirements.txt
```

# Contributing to karchit8cture

Thank you for considering contributing to this project! Follow these guidelines to contribute:

## How to Contribute

- Fork the repository
- Clone the forked repository
- Create a new branch
- Make your changes
- Submit a pull request
