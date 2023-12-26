import logging
import os
from logging import Formatter, StreamHandler

LOG_LEVEL = "INFO"


if os.environ.get("LOG_LEVEL"):
    LOG_LEVEL = str(os.environ.get("LOG_LEVEL"))


def getLogger(log_name: str) -> logging.Logger:
    logger = logging.getLogger(log_name)
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False
    formatter = Formatter(
        fmt="%(asctime)s.%(msecs)03d %(levelname)7s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )

    # 標準出力用 設定
    sthandler = StreamHandler()
    sthandler.setLevel(LOG_LEVEL)
    sthandler.setFormatter(formatter)
    logger.addHandler(sthandler)

    return logger
