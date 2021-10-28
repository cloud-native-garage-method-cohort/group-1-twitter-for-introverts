from diagrams import Cluster, Diagram
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka


def get_example_diagram() -> bytes:
    result = None
    with Diagram("Example Diagram", show=False) as diag_out:
        ingress = Nginx("ingress")

        metrics = Prometheus("metric")
        metrics << Grafana("monitoring")

        with Cluster("Service Cluster"):
            grpcsvc = [Server("grpc1"), Server("grpc2"), Server("grpc3")]

        with Cluster("Discovery"):
            main = Redis("session")
            main - Redis("replica") << metrics
            grpcsvc >> main

        with Cluster("Database HA"):
            main = PostgreSQL("users")
            main - PostgreSQL("replica") << metrics
            grpcsvc >> main

        aggregator = Fluentd("logging")
        aggregator >> Kafka("stream") >> Spark("analytics")

        ingress >> grpcsvc >> aggregator
        result: bytes = diag_out.dot.pipe(format="png")
    return result
