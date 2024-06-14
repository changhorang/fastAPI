import logging.handlers

class logWriter():
    log = logging.getLogger("logWriter")
    formatter = logging.Formatter('[%(asctime)s][%(levelname)-8s] %(message)s : (%(filename)s:%(lineno)s)',datefmt='%H:%M:%S')
    
    fileHandler = None

    @staticmethod
    def setLogLevel(level):
        if level == "INFO":
            logWriter.log.setLevel(logging.INFO)
        elif level == "WARNING":
            logWriter.log.setLevel(logging.WARNING)
        elif level == "ERROR":
            logWriter.log.setLevel(logging.ERROR)
        elif level == "CRITICAL":
            logWriter.log.setLevel(logging.CRITICAL)
        else:
            logWriter.log.setLevel(logging.DEBUG)

    @staticmethod
    def setFile(logFile):
        logWriter.fileHandler = logging.handlers.TimedRotatingFileHandler(logFile, when='midnight', backupCount=0, interval=1)

        logWriter.fileHandler.setFormatter(logWriter.formatter)
        logWriter.log.addHandler(logWriter.fileHandler)

    @staticmethod
    def removeFile():
        logWriter.log.removeHandler(logWriter.fileHandler)