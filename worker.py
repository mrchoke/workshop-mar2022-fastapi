from os import getenv

from uvicorn.workers import UvicornWorker


class Worker(UvicornWorker):
    CONFIG_KWARGS = {"proxy_headers": True, "root_path": getenv("ROOT_PATH", "") }
