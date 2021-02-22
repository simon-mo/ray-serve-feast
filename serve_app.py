import feast
import os

import ray
from ray import serve
from starlette.requests import Request

ray.init(address="auto")
client = serve.connect()

if os.environ.get("KUBERNETES_SERVICE_HOST"):
    # Use Kubernetes support for services to access feast
    feast_options = {
        "FEAST_CORE_URL": "feast-release-feast-core:6565",
        "FEAST_SERVING_URL": "feast-release-feast-online-serving:6566",
    }
else:
    # Use local port forwarding to access feast
    feast_options = {
        "FEAST_CORE_URL": "localhost:6565",
        "FEAST_SERVING_URL": "localhost:6566",
    }


class FeatureServer:
    def __init__(self):
        print("Connecting to feast", feast_options)
        for k, v in feast_options.items():
            os.environ[k] = v

        self.feast_client = feast.Client()

    def __call__(self, request: Request):
        # Preprocess
        if request.query_params.get("show_stats"):
            features = [
                "driver_statistics:avg_daily_trips", "driver_trips:trips_today"
            ]
        else:
            features = ["driver_trips:trips_today"]

        # Retrieval from feature store
        resp = self.feast_client.get_online_features(
            feature_refs=features, entity_rows=[{
                'driver_id': 61757
            }]).to_dict()

        # Run through modeling
        resp["prediction"] = [resp["driver_trips:trips_today"][0] * 2]

        # Of course you can do post processing as well
        resp = {key: value[0] for key, value in resp.items()}

        return resp


client.create_backend("backend", FeatureServer, config={"num_replicas": 1})
client.create_endpoint("endpoint", backend="backend", route="/endpoint")
