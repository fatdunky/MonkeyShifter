'''
Created on 3Dec.,2016

@author: fatdunky
'''
import logging, os, time
from lines.utilites.constants import Constants

from logging.handlers import TimedRotatingFileHandler
from logging import FileHandler

class Logger(object):
    '''
    This class handles the logging for the application
    '''
    _consoleLogging = False
    _rotateLog = True
    _logDirectory = os.getcwd() + os.path.sep + Constants.DEFAULT_LOG_DIR
    _logFile = Constants.DEFAULT_LOG_FILE_START
    _logLevel = logging.DEBUG
    _formatString = Constants.DEFAULT_LOGGER_FORMAT
    _formatDateString = Constants.DEFAULT_LOGGER_DATE_FORMAT
    _logFileDate = time.strftime("%Y%m%d")
    

    def __init__(self):
        '''
        Constructor
        '''
    
    @staticmethod
    def setConsoleLogging(booleanValue):
        '''
        set console logging value
        '''
        if type(booleanValue) == bool:
            Logger._consoleLogging = booleanValue
            logging.debug("Setting consoleLogging to %s", booleanValue)    
        else:
            Logger._consoleLogging = False
            logging.error("Non boolean value passed setting console to False")     
        
    @staticmethod
    def getConsoleLogging():
        return Logger._consoleLogging       
    
    @staticmethod
    def setLogDirectory(logDirectory):
        '''
        set logging Directory
        '''
        if os.path.isdir(logDirectory):
            Logger._logDirectory = logDirectory
            logging.debug("Setting logging directory to: %s",logDirectory)
        else:
            _defaultDirectory = os.getcwd() + os.path.sep + Constants.DEFAULT_LOG_DIR
            Logger._logDirectory = _defaultDirectory
            logging.error("Specified logging directory %s, did not exist. Using default directory: %s",logDirectory,_defaultDirectory)
    
    @staticmethod           
    def getLogDirectory():
        return Logger._logDirectory
    
    @staticmethod              
    def setLogFile(logFile):
        '''
        set logging file
        '''
        includedPath = os.path.dirname(logFile)
        logFile = os.path.basename(logFile)
        
        if includedPath != "":
            Logger.setLogDirectory(includedPath)
        
        if logFile is None or logFile == "":
            #defaultLogFile = Constants.DEFAULT_LOG_FILE_START +  self.logFileDate +  Constants.DEFAULT_LOG_FILE_SUFFIX
            _defaultLogFile = Constants.DEFAULT_LOG_FILE_START +  Constants.DEFAULT_LOG_FILE_SUFFIX
            Logger._logFile = _defaultLogFile
            logging.error("Specified logging file was null. Using default file: %s",_defaultLogFile)
        else:
            Logger._logFile = logFile
            logging.debug("Setting logging logFile to: %s",logFile)
    
    @staticmethod             
    def getLogFile():
        return Logger._logFile 
    
    @staticmethod
    def getFullPathLogFile():
        return Logger.getLogDirectory() + os.path.sep + Logger.getLogFile()
        
    @staticmethod
    def setFormatString(stringValue):
        '''
        set logging format string
        '''
        if stringValue is None or stringValue == "":
            Logger._formatString = Constants.DEFAULT_LOGGER_FORMAT
            logging.error("Empty value passed to setFormatString, using default value")     
        
        Logger._formatString=stringValue
               
    @staticmethod
    def getFormatString():
        return Logger._formatString
    
    @staticmethod
    def setDateFormatString(stringValue):
        '''
        set logging format date string
        '''
        if stringValue is None or stringValue == "":
            Logger._formatDateString = Constants.DEFAULT_LOGGER_DATE_FORMAT
            logging.error("Empty value passed to setDateFormatString, using default value")     
        
        Logger._formatDateString=stringValue
               
    @staticmethod
    def getDateFormatString():
        return Logger._formatDateString
    
    @staticmethod
    def setLoggingLevel(level):
        '''
        sets the logging level
        '''
        if level.upper() in ["CRITICAL","ERROR", "WARNING", "INFO", "DEBUG"]:
            logging.getLogger().setLevel(level)
            Logger._logLevel = level
            logging.info("Setting log level to %s",level)
        else:
            logging.error("Unknown logging level specified: %s, setting to %s",level,Constants.DEFAULT_LOG_LEVEL)
            logging.getLogger().setLevel(Constants.DEFAULT_LOG_LEVEL)
            Logger._logLevel = Constants.DEFAULT_LOG_LEVEL
    
    @staticmethod
    def getLoggingLevel():
        return Logger._logLevel
    
    @staticmethod
    def setRotationFile(booleanValue, when, interval, backupCount):
        Logger._rotateLog = booleanValue
        Logger._when = when
        Logger._interval = interval
        Logger._backupCount = backupCount
        
    @staticmethod        
    def updateHandler():
        '''
        configure the logger
        '''

        if Logger._logDirectory is None or Logger._logDirectory == "":
            Logger.setLogDirectory("")
            
        if Logger._logFile is None or Logger._logFile == "":
            Logger.setLogFile("")
        
        
        else:
            if Logger._rotateLog:        
                #handler = TimedRotatingFileHandler(self.getFullPathLogFile(), when='midnight', interval=1, backupCount=0, encoding=None, delay=False, utc=False)
                Logger._handler = TimedRotatingFileHandler(Logger.getFullPathLogFile(), when=Logger._when, interval=Logger._interval, backupCount=Logger._backupCount, encoding=None, delay=False, utc=False)
            else:
                Logger._handler = logging.FileHandler(Logger.getFullPathLogFile(), encoding=None, delay=False)
                
        if Logger._formatString is None or Logger._formatString == "":
            Logger.setFormatString("")
        
        if Logger._logLevel is None or Logger._logLevel == "":
            Logger.setLoggingLevel("")
        
        formatter = logging.Formatter(fmt=Logger.getFormatString(), datefmt=Logger.getDateFormatString())
        Logger._handler.setFormatter(formatter)
        Logger._handler.setLevel(Logger.getLoggingLevel())
        logging.getLogger().addHandler(Logger._handler)

        
        #logging.basicConfig(filename=self.getFullPathLogFile(),format=self.formatString,level=self.logLevel)     
    
    @staticmethod
    def rotateLog():
        '''
        TODO: Setup logrotation 
        '''
        logging.info("LogRotation")