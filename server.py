from flask import Response, Flask, request
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time
app = Flask(__name__)

graphs = {}
graphs['c'] = Counter('sample_external_url_up','external url is up')
graphs['h'] = Histogram('sample_external_url_response_ms','Response latency in seconds',buckets=(1, 2, 5, 6, 10))
@app.route("/200")
def UP():
    start = time.time()
    graphs['c'].inc()
    time.sleep(0.600)
    end = time.time()
    graphs['h'].observe(end - start)
    return "Webserver is UP!"

@app.route("/503")
def down():
    start = time.time()
    graphs['c'].inc()
    time.sleep(0.600)
    end = time.time()
    graphs['h'].observe(end - start)
    return "Webserver is Down!"

@app.route("/metrics")
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")

~                                                  