import logging

import uvicorn

DEV_VERPOSE_LOG = True
FORMAT: str = (
    "%(levelprefix)s %(message)s : %(asctime)s" if DEV_VERPOSE_LOG else
    "%(levelprefix)s %(message)s \n%(levelprefix)s %(asctime)s | %(name)s - %(module)s:%(lineno)s - %(funcName)s()"
)


def init_loggers(logger_name: str = "app-logs") -> None:
    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create file handler and set level to debug
    fh = logging.FileHandler("app.log", mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)

    formatter = uvicorn.logging.DefaultFormatter(
        FORMAT,  datefmt="%m-%d %H:%M:%S",
    )
    # add formatter to ch & fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch & fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    logger.debug('running logger which has been just initalized')
