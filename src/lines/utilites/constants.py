'''
Created on 3Dec.,2016

@author: fatdunky
'''

class Constants(object):
    '''
    A class containing all the constants in one place
    '''
    DEFAULT_LOGGER_FORMAT='%(asctime)s|%(name)s|%(levelname)s|%(message)s'
    DEFAULT_LOGGER_DATE_FORMAT='%Y%m%d|%H:%M:%S'
    DEFAULT_CONFIG_DIR='config'
    DEFAULT_CONFIG_FILE='renamer.cfg'
    DEFAULT_DATA_DIR='data'
    DEFAULT_LOG_DIR='logs'
    DEFAULT_LOG_FILE_START='reorganiser'
    DEFAULT_LOG_FILE_SUFFIX='.log'
    DEFAULT_LOG_LEVEL='DEBUG'

    def __init__(self):
        '''
        Constructor
        '''
        