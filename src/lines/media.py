'''
Created on 5Mar.,2017

@author: fatdunky
'''
from lines.line import Line

class Media(object):
    '''
    classdocs
    '''
    
    

    def __init__(self):
        '''
        Constructor
        '''
        self.__absoluteFileName = ""
        self.__size = 0
        self.__fileName = ""
        self.__path = ""
        self.__lineObj = None
        self.__mediaType = None
        self.__wordCount = 0
        self.__fileExtension = ""

    def get_file_extension(self):
        return self.__fileExtension


    def set_file_extension(self, value):
        self.__fileExtension = value


    def del_file_extension(self):
        del self.__fileExtension


    def get_absolute_file_name(self):
        return self.__absoluteFileName


    def get_size(self):
        return self.__size


    def get_file_name(self):
        return self.__fileName


    def get_path(self):
        return self.__path


    def get_line_obj(self):
        return self.__lineObj


    def get_word_count(self):
        return self.__wordCount


    def set_absolute_file_name(self, value):
        self.__absoluteFileName = value


    def set_size(self, value):
        self.__size = value


    def set_file_name(self, value):
        self.__fileName = value


    def set_path(self, value):
        self.__path = value


    def set_line_obj(self, value):
        self.__lineObj = value


    def set_word_count(self, value):
        self.__wordCount = value


    def del_absolute_file_name(self):
        del self.__absoluteFileName


    def del_size(self):
        del self.__size


    def del_file_name(self):
        del self.__fileName


    def del_path(self):
        del self.__path


    def del_line_obj(self):
        del self.__lineObj


    def del_word_count(self):
        del self.__wordCount

    absolute_file_name = property(get_absolute_file_name, set_absolute_file_name, del_absolute_file_name, "absoluteFileName's docstring")
    size = property(get_size, set_size, del_size, "size's docstring")
    file_name = property(get_file_name, set_file_name, del_file_name, "fileName's docstring")
    path = property(get_path, set_path, del_path, "path's docstring")
    line_obj = property(get_line_obj, set_line_obj, del_line_obj, "nameWordsList's docstring")
    word_count = property(get_word_count, set_word_count, del_word_count, "wordCount's docstring")
    file_extension = property(get_file_extension, set_file_extension, del_file_extension, "file_extension's docstring")
        