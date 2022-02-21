import logging 

def create_logger(name: str, level: int = 10) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter("%(levelname)s %(name)s %(asctime)s %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger