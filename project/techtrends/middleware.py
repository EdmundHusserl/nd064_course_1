import logging
from functools import wraps
from dataclasses import (
    dataclass,
    field
)


@dataclass
class AppLogger:
    name: str
    level: int
    post_count: int = 0
    db_connection_count: int = 0
    logger: logging.Logger = field(init=False)

    def __post_init__(self):
        self.logger = self.create_logger(self.name, self.level)

    def create_logger(self, name: str, level: int = 10) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)

        ch = logging.StreamHandler()
        ch.setLevel(level)

        formatter = logging.Formatter(
            "%(levelname)s %(name)s %(asctime)s %(message)s"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger

    def increment_db_connection_count(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            res = func(*args, **kwargs)
            self.db_connection_count += 1
            return res
        return wrapped_func

    def increment_post_count(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            res = func(*args, **kwargs)
            self.post_count += 1
            return res
        return wrapped_func

    def set_post_count(self, count: int):
        self.post_count = count
