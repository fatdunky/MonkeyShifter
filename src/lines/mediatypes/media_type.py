'''
Created on 29Mar.,2017

@author: mcrick
'''
from lines.utilites.io import Io

class MediaType(object):
    '''
    super class for media types
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__subtypes = []
        self.__extensions = []
        self.__destination_dir= ""
        self.__known_names_file_name = ""
        self.__known_names_list = {}
    
    
    def get_subtypes(self):
        return self.__subtypes


    def get_extensions(self):
        return self.__extensions


    def get_destination_dir(self):
        return self.__destination_dir


    def get_known_names_list(self):
        return self.__known_names_list
    
    def get_known_names_file_name(self):
        return self.__known_names_file_name


    def set_subtypes(self, value):
        self.__subtypes = value


    def set_extensions(self, value):
        self.__extensions = value


    def set_destination_dir(self, value):
        self.__destination_dir = value


    def set_known_names_list(self, value):
        self.__known_names_list = value
        
    def set_known_names_file_name(self, value):
        self.__known_names_file_name = value

    def del_subtypes(self):
        del self.__subtypes


    def del_extensions(self):
        del self.__extensions


    def del_destination_dir(self):
        del self.__destination_dir


    def del_known_names_list(self):
        del self.__known_names_list
        
    def del_known_names_file_name(self):
        del self.__known_names_file_name
        
    def load_file(self):
        file_lines = []
        try:
            file_lines = Io.read_gz_file(self.__known_names_list)
        except (OSError, IOError) as e:
            #assuming its file not found
            Io.write_gz_file("\n", self.__known_names_list)
            
        for line in file_lines:
            self.__known_names_list[line] = line

    subtypes = property(get_subtypes, set_subtypes, del_subtypes, "list of subtype names")
    extensions = property(get_extensions, set_extensions, del_extensions, "list of extensions that match this media type")
    destination_dir = property(get_destination_dir, set_destination_dir, del_destination_dir, "destination directory for media type")
    known_names_list = property(get_known_names_list, set_known_names_list, del_known_names_list, "file name of known names for media type")
    known_names_file_name = property(get_known_names_file_name, set_known_names_file_name, del_known_names_file_name, "file name of list of known names for this media type")
