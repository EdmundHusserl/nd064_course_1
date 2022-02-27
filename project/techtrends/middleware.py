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

    def increment(self, what: str):
        def increment_attribute(func):
            @wraps(func)
            def wrapped_func(*args, **kwargs):
                res = func(*args, **kwargs)
                try:
                    self.__setattr__(
                        what,
                        int(getattr(self, what)) + 1
                    )
                except AttributeError as e:
                    self.logger.warning(f"{e.args}")
                    pass
                return res
            return wrapped_func
        return increment_attribute

    def set_post_count(self, count: int):
        self.post_count = count
