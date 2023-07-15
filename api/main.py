import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .logs.logconfig import init_loggers
from .routes import business_routes, businessdb_routes

# TODO REMOVE any senetive logging
# LOGs - This should run as soon as possible to catch all logs
# Run only one of these
init_loggers(logger_name="api-routes-logs")
app = FastAPI(
    title="Brand Booster API",
    description="""
    Brand Booster generate catchy tagline
    with SEO optimized keywords for your business.""",
    version="0.2.3",  # [TODO] 0.3.0 authentications
    contact={
        "name": "Yousef Dawoud",
        "email": "yousefdawoud.dev@outlook.com",
    },
)


# init our logger
log = logging.getLogger("api-routes-logs")

# [UPDATE] CORS Setup
origins = [
    # "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(business_routes.router)
app.include_router(businessdb_routes.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World!"}


@app.get("/logs")
def log_now() -> dict[str, str]:
    log.debug("Successfully hit the /log endpoint.")
    return {"result": "OK"}
