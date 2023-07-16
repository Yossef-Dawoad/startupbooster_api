import logging

import uvicorn

DEV_VERPOSE_LOG = True  # SETTING this to true expose sensitive data
DEBUG_LEVEL = logging.DEBUG if DEV_VERPOSE_LOG else logging.INFO

FORMAT: str = (
    "%(levelprefix)s %(message)s : %(asctime)s"
    if not DEV_VERPOSE_LOG
    else "%(levelprefix)s %(message)s \n%(levelprefix)s %(asctime)s | %(name)s - %(module)s:%(lineno)s - %(funcName)s()"
)


def init_loggers(logger_name: str = "app-logs") -> None:
    # create logger
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)

    # # Get the stat_result object for the file
    # st = os.stat("app.log")
    # # Check if the file is writable by anyone
    # W_Ok = bool(st.st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = uvicorn.logging.DefaultFormatter(
        FORMAT,
        datefmt="%m-%d %H:%M:%S",
    )
    ch.setFormatter(formatter)

    # if W_Ok:     # create file handler and set level to debug of write_OK
    #     fh = logging.FileHandler("app.log", mode="a", encoding="utf-8")
    #     fh.setLevel(logging.DEBUG)
    #     fh.setFormatter(formatter)
    #     logger.addHandler(fh)

    # add ch & fh to logger
    logger.addHandler(ch)

    logger.debug("running logger which has been just initalized")
