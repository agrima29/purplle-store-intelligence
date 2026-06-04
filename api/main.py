# api/main.py
import time, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from prometheus_client import make_asgi_app

app = FastAPI(title="Purplle Store Intelligence", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

# Prometheus — free production readiness points, zero extra infrastructure
# app.mount("/metrics/prometheus", make_asgi_app())

from api.routes import metrics, funnel, zones, anomalies, footfall, journey, insights
app.include_router(metrics.router,   prefix="/api/v1")
app.include_router(funnel.router,    prefix="/api/v1")
app.include_router(zones.router,     prefix="/api/v1")
app.include_router(anomalies.router, prefix="/api/v1")
app.include_router(footfall.router,  prefix="/api/v1")
app.include_router(journey.router,   prefix="/api/v1")
app.include_router(insights.router,  prefix="/api/v1")

@app.get("/health")
def health():
    db_ready = os.path.exists(os.environ.get("DB_PATH","data/events.db"))
    return {"status":"ok", "pipeline_ready": db_ready, "ts": time.time()}

@app.get("/metrics")
def metrics_shortcut():
    from api.routes import metrics, funnel, footfall, anomalies, zones, journey, insights
    return metrics.get_metrics()