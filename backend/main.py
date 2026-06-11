from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import mbr

app = FastAPI(
    title="TraceKit v2",
    description="Pharma MES Recipe Designer API — MBR/EBR Lifecycle, Deviations, Audit Trail",
    version="2.0.0"
)

# Allow React frontend to talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(mbr.router)

@app.get("/")
def root():
    return {
        "app": "TraceKit v2",
        "status": "running",
        "docs": "/docs"
    }