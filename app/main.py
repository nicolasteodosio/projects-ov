import uvicorn
from fastapi import FastAPI
from nicelog import setup_logging
from router.projects import router as project_router

API_VERSION = "v1"

application = FastAPI()
application.router.redirect_slashes = True

application.include_router(project_router, prefix=f"/{API_VERSION}/projects", tags=["orders"], dependencies=[])


@application.on_event("startup")
async def startup_event():
    setup_logging()


@application.get("/healthcheck")
async def healthcheck():
    return {"message": "I'm alive"}


if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=8000)
