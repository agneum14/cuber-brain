from fastapi import FastAPI

from controllers import general, health

app = FastAPI(title="Cuber Brain", description="Cube that brain dude.")
for router in [health.router, general.router]:
    app.include_router(router)
