'''
Created on 23Nov.,2016

@author: fatdunky
'''
import gzip, logging, sys
from pydoc import locate

class Io(object):
    '''
    Class responsible for reading and writing files
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
    @staticmethod  
    def read_gz_file(file_name):
        input_file = gzip.open(file_name, 'rt') 
        try:
            return_lines=input_file.readlines()        
        finally:
            input_file.close()
            return return_lines
    
    @staticmethod  
    def read_file(file_name):
        input_file = open(file_name, 'rt') 
        try:
            return_lines=input_file.readlines()        
        finally:
            input_file.close()
            return return_lines
    
    @staticmethod  
    def write_gz_file(data, filename):
        output = gzip.open(filename, 'wt')
        try:
            for line in data:
                output.write(line)
        finally:
            output.close()
    
    @staticmethod
    def load_class(class_name):
        return_value = locate(class_name)
        if return_value == None:
            logging.error("%s not found!",class_name)
            exit(1)
            #TODO: throw exception here instead
        return return_value
    
