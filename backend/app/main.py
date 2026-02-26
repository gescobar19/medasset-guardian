from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import assets, usage, inspections, reports

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(assets.router)
app.include_router(usage.router)
app.include_router(inspections.router)
app.include_router(reports.router)