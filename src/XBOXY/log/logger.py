from loguru import logger
logger.remove()
logger.add(lambda msg: print(msg, end=""), 
           format="<green>[+]</green> | <cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> | <level>{level}</level> - <level>{message}</level>", 
           level="INFO", colorize=True)
