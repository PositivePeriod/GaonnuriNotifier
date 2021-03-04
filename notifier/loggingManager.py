import logging

loggingPath = 'notifier/private/logging.log'
with open(loggingPath, 'a') as f:
    f.write('')

logger = logging.getLogger()

formatType = '%(asctime)s | %(levelname)8s | %(filename)s-%(funcName)s-%(lineno)s | %(message)s'
formatter = logging.Formatter(formatType)

fileHandler = logging.FileHandler(loggingPath)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug Example")
    logger.info("Info Example")
    logger.warning("Warning Example")
    logger.error("Error Example")
    logger.critical("Critical Example")
