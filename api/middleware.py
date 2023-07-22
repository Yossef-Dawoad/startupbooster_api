from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from .middlewares.redirect_resource import RedirectsMiddleware
from .middlewares.timed_request import TimedRequestASGIMiddleware

# docs:  https://www.starlette.io/middleware/

######################## Cors Setup ########################
# UPDATE CORS Setup
origins = [
    "*",  # replace  "http://localhost:3000",
]

MyCustomCORSMiddleware = Middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
)
#############################################################

redirections = {
    "/login": "/auth/login",
    "/sign_up": "/auth/register",
    "/docs": "/",
}


middlewareStack = [
    MyCustomCORSMiddleware,
    Middleware(TimedRequestASGIMiddleware),
    Middleware(RedirectsMiddleware, path_mapping=redirections),
]
