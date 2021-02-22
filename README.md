## Ray Serve + Feast Demo

This is a quick demo of using Ray Serve with Feast. 

You can use `infra/eks_cluster.yaml` to start the eks cluster and set up Feast using their helm chart.

```
.
├── Dockerfile # Docker file to build the Ray container
├── README.md 
├── infra
│   └── eks_cluster.yaml # Use eksctl to start the eks cluster
├── operator # These are the config required to deploy Ray operators
│   ├── cluster_crd.yaml
│   └── operator.yaml
├── prod_cluster.yaml # Creates a Ray cluster resource
└── serve_app.py # Serve app

2 directories, 9 files
```

### Setup
```bash
eksctl create cluster -f infra/eks_cluster.yaml
# run the helm charts to setup feast
# run feast minimal example to setup features
...
kubectl apply -f operator/*
```

### Local development
1. Port forward the `feast-core:6565` port and `feast-online-serving:6566` via kubectl port-forward
2. Run `ray start --head` and `serve start` to start the local ray serve instance
3. Run `python serve_app.py` to deploy the local app. You can now query it by `curl localhost:8000/endpoint` (optionally with the HTTP parameters `?show_stats=true`.


### Production development
1. Build the container `docker build -t your-image-name .`
2. Change the image name in `prod_cluster.yaml` to your image.
3. Apply the cluster to create the Ray cluster running the job. `kubectl apply -f prod_cluster.yaml`
