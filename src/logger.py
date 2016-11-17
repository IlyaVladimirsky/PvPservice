import logging


def get_logger(name, path, level, formatter):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create a file handler
    handler = logging.FileHandler(path)
    handler.setLevel(level)

    # create a logging formatter
    formatter = logging.Formatter(formatter)
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger