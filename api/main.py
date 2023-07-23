import logging

from fastapi import FastAPI

from .logs.logconfig import init_loggers
from .middleware import middlewareStack
from .routes import auth_routes, business_routes, businessdb_routes, experiments_routes

# TODO REMOVE any senetive logging
# LOGs - This should run as soon as possible to catch all logs
# Run only one of these
init_loggers(logger_name="api-routes-logs")
app = FastAPI(
    title="StartUP Booster API",
    description="""
    StartUP Booster generate catchy tagline
    with SEO optimized keywords for your business.""",
    version="0.3.0",  # [TODO] 0.3.0 authentications
    contact={
        "name": "Yousef Dawoud",
        "email": "yousefdawoud.dev@outlook.com",
    },
    docs_url="/",
    middleware=middlewareStack,
)

# TODO make use to initialize the llms
# @app.on_event("startup")
# async def startup_event():
#     # run start-up script here


# init our logger
log = logging.getLogger("api-routes-logs")


app.include_router(business_routes.router)
app.include_router(businessdb_routes.router)
app.include_router(experiments_routes.router)
app.include_router(auth_routes.router)


@app.get("/logs")
def log_now() -> dict[str, str]:
    log.debug("Successfully hit the /log endpoint.")
    return {"result": "OK"}
