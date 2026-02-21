from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import general, health

app = FastAPI(title="Cuber Brain", description="Cube that brain dude.")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

for router in [health.router, general.router]:
    app.include_router(router)
