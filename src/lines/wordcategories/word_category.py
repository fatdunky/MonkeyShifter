'''
Created on 23Nov.,2016

@author: fatdunky
'''
from lines.utilites.io import Io
import logging


class WordCategory(object):
    '''
    This class is the super class of the word categories
    '''
    #List of Maps that contain the word class in each category
    wordCategories = {}

    @staticmethod
    def match_word_category(text):
        '''
        Match the word to a correct word category
        '''
        
        for wordCategory in WordCategory.wordCategories:
            logging.debug("wordCategory: %s", wordCategory)
            if WordCategory.wordCategories[wordCategory].is_match(text) :
                return WordCategory.wordCategories[wordCategory]
        
        return None   
        
    
    def __init__(self):
        '''
        Constructor
        '''
        self._delimiter = ""
        self._file = ""
        self._class_var = ""
        self._config_name = ""
        self._map_of_words = {}
                    
    def get_delimiter(self):
        return self._delimiter

    def is_match(self, wordText):
        if wordText in self._map_of_words:
            return True
        else:
            return False
    
    def get_file(self):
        return self._file

    def get_config_name(self):
        return self._config_name


    def get_class_var(self):
        return self._class_var
    
    def get_map_of_words(self):
        return self._map_of_words


    def set_delimiter(self, value):
        self._delimiter = value


    def set_file(self, value):
        self._file = value
        
    def set_config_name(self, value):
        self._config_name = value

    def set_class_var(self, value):
        self._class_var = value


    def del_delimiter(self):
        del self._delimiter

    def del_config_name(self):
        del self._config_name

    def del_file(self):
        del self._file


    def del_class_var(self):
        del self._class_var
    
    def add_new_word(self, word):
        if not self._map_of_words.has_key(word):
            self._map_of_words[word] = word
        else:
            logging.warn("Word [%s] allready existing in category [%s]", word, self.__class__.__name__)
    
    def load_file(self):
        file_lines = []
        try:
            file_lines = Io.read_gz_file(self._file)
        except (OSError, IOError) as e:
            #assuming its file not found
            Io.writeGzFile("\n", self._file)
            
        for line in file_lines:
            self._map_of_words[line] = line
    
    def save_file(self):
        try:
            Io.write_gz_file(self._map_of_words.values(),self._file)
        except (OSError, IOError) as e:
            logging.error("exception writting to file: %s, %s", self._file, e)

            
    config_name = property(get_config_name, set_config_name, del_config_name , "config_name's docstring")
    delimiter = property(get_delimiter, set_delimiter, del_delimiter, "delimiter's docstring")
    file = property(get_file, set_file, del_file, "file's docstring")
    class_var = property(get_class_var, set_class_var, del_class_var, "class_var's docstring")
        
        