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
            "%(name)s %(levelname)s %(asctime)s %(message)s"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger

    def increment(self, *fields):
        def increment_attribute(func):
            @wraps(func)
            def wrapped_func(*args, **kwargs):
                res = func(*args, **kwargs)
                try:
                    for field in fields:
                        self.__setattr__(
                            str(field),
                            int(getattr(self, field)) + 1
                        )
                except AttributeError as e:
                    self.logger.warning(f"{e.args}")
                    pass
                return res
            return wrapped_func
        return increment_attribute

    def set_post_count(self, count: int):
        self.post_count = count
