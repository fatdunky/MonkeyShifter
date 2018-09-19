'''
Created on 19Feb.,2017

@author: fatdunky
'''
import logging, os
from utilites.configuration_parser import ConfigurationParser

class Configuration(ConfigurationParser):
    '''
    class object of the configuration file
    '''
    SECTION_NAME_CONFIG_FILE="config_file"
    ITEM_CONFIG_DELIMITER="delimiter"

    SECTION_NAME_DIRECTORIES = "directories"
    DIRECTORY_NAME_DATA='data_directory'
    DIRECTORY_NAME_LOG='logging_directory'
    DIRECTORY_NAME_CONFIG='configuration_data'

    SECTION_NAME_FILE_NAME = "file_name"
    ITEM_FILE_NAME_DELIMITERS="delimiters"

    SECTION_NAME_MEDIA_TYPES="media_types"
    SECTION_NAME_MEDIA_SUB_TYPES="media_sub_types"
    ITEM_MEDIA_TYPES_SUBTYPES="subtypes"
    ITEM_MEDIA_TYPES_EXTENSIONS="extensions"
    ITEM_MEDIA_TYPES_DESTINATION_DIR="destination_dir"
    ITEM_MEDIA_TYPES_MODULE_NAME="module_name"
    ITEM_MEDIA_TYPES_MODULE_CLASS="class"
    ITEM_MEDIA_TYPES_KNOWN_NAMES_FILE="known_names_list"

    SECTION_NAME_WORD_FILE_NAMES = "word_file_names"
    ITEM_WORD_FILE_DELIMITER = 'delimiters'
    ITEM_WORD_FILE_FILE_NAME = 'file'
    ITEM_WORD_FILE_CLASS = 'class'
    ITEM_WORD_MODULE_NAME='module_name'

    SECTION_NAME_LOGGING = "logging"
    LOGGING_FORMAT='logging_format'
    LOGGING_DATE_FORMAT='logging_date_format'
    LOGGING_LEVEL='logging_level'
    LOGGING_CONSOLE_MODE='logging_console_mode'
    LOGGING_FILE='logging_file'
    LOGGING_WHEN='logging_when'
    LOGGING_INTERVAL='logging_interval'
    LOGGING_BACKUP_COUNT='logging_backup_count'
    LOGGING_ROTATE_MODE='logging_rotate_mode'
    LOGGING_BYTES='logging_bytes'


    def __init__(self, config_directory, config_file, default_config_directory, default_config_file):
        '''
        Constructor
        '''
        #self.config = ConfigParser.ConfigParser()
        #get config sections
        super(Configuration, self).__init__(default_config_directory,default_config_file)
        self.set_config_directory(config_directory)
        self.read_config(config_file)

        print ("config sections: {}".format(self.config.sections()))
        self.__config_file = dict(self.config.items(Configuration.SECTION_NAME_CONFIG_FILE))
        self.__directories = dict(self.config.items(Configuration.SECTION_NAME_DIRECTORIES))
        self.__file_name = dict(self.config.items(Configuration.SECTION_NAME_FILE_NAME))
        self.__media_type_names = dict(self.config.items(Configuration.SECTION_NAME_MEDIA_TYPES))
        self.__word_file_names = dict(self.config.items(Configuration.SECTION_NAME_WORD_FILE_NAMES))
        self.__logging = dict(self.config.items(Configuration.SECTION_NAME_LOGGING))
        self.__media_sub_type_names = dict(self.config.items(Configuration.SECTION_NAME_MEDIA_TYPES))

        #get variable config sections - word files
        self.__word_files = {}
        for word_file_name in list(self.__word_file_names.values()):
            self.__word_files[word_file_name] = self.config.items(word_file_name)

        #get variable config sections - media types
        self.__media_types = {}
        self.__media_sub_types = {"":[]}
        for media_type_name in list(self.__media_type_names.values()):
            self.__media_types[media_type_name] = self.config.items(media_type_name)
            sub_types = self.get_media_type_subtypes(media_type_name)
            sub_types_dict = {}
            for sub_media_type_name in sub_types:
                if (sub_media_type_name and sub_media_type_name.strip()):
                    sub_types_dict[sub_media_type_name] = self.config.items(sub_media_type_name)
            self.__media_sub_types[media_type_name] = sub_types_dict


    def get_config_file_delimiter(self):
        return self.__config_file[self.ITEM_CONFIG_DELIMITER]

    def get_file_name_delimiters(self):
        return self.__file_name[self.ITEM_FILE_NAME_DELIMITERS]

    def get_media_type_subtypes(self, media_type):
        if (media_type in self.__media_types):
            media_types_items = dict(self.__media_types[media_type])
            return_value = media_types_items[self.ITEM_MEDIA_TYPES_SUBTYPES]
            return return_value.split(self.get_config_file_delimiter())
        else:
            return []

    def get_media_type_extensions(self, media_type):
        if (media_type in self.__media_types):
            media_types_items = dict(self.__media_types[media_type])
            return_value = media_types_items[self.ITEM_MEDIA_TYPES_EXTENSIONS]
            return return_value.split(self.get_config_file_delimiter())
        else:
            return []

    def get_media_type_destination_dir(self, media_type):
        if (media_type in self.__media_types):
            media_types_items = dict(self.__media_types[media_type])
            return media_types_items[self.ITEM_MEDIA_TYPES_DESTINATION_DIR]
        else:
            return ""

    def get_media_type_module_name(self, media_type):
        if (media_type in self.__media_types):
            media_types_items = dict(self.__media_types[media_type])
            return media_types_items[self.ITEM_MEDIA_TYPES_MODULE_NAME]
        else:
            return ""

    def get_media_type_module_class(self, media_type):
        if (media_type in self.__media_types):
            media_types_items = dict(self.__media_types[media_type])
            return media_types_items[self.ITEM_MEDIA_TYPES_MODULE_CLASS]
        else:
            return ""

    def get_media_type_known_names_list(self, media_type):
        if (media_type in self.__media_types):
            media_types_items = dict(self.__media_types[media_type])
            return media_types_items[self.ITEM_MEDIA_TYPES_KNOWN_NAMES_FILE]
        else:
            return ""

    def get_media_sub_type_extensions(self, media_type, media_sub_type):
        if (media_type in self.__media_sub_types):
            sub_types_dict = self.__media_sub_types[media_type]
            if (media_sub_type in sub_types_dict):
                media_sub_types_items = dict(sub_types_dict[media_sub_type])
                return_value = media_sub_types_items[self.ITEM_MEDIA_TYPES_EXTENSIONS]
                return return_value.split(self.get_config_file_delimiter())
            else:
                return []
        else:
            return []

    def get_media_sub_type_destination_dir(self, media_type, media_sub_type):
        if (media_type in self.__media_sub_types):
            sub_types_dict = self.__media_sub_types[media_type]
            if (media_sub_type in sub_types_dict):
                media_sub_types_items = dict(sub_types_dict[media_sub_type])
                return media_sub_types_items[self.ITEM_MEDIA_TYPES_DESTINATION_DIR]
            else:
                return ""
        else:
            return ""

    def get_media_sub_type_module_name(self, media_type, media_sub_type):
        if (media_type in self.__media_sub_types):
            sub_types_dict = self.__media_sub_types[media_type]
            if (media_sub_type in sub_types_dict):
                media_sub_types_items = sub_types_dict[media_sub_type]
                media_sub_types_items_dict =  dict(media_sub_types_items)
                return media_sub_types_items_dict[self.ITEM_MEDIA_TYPES_MODULE_NAME]
            else:
                return ""
        else:
            return ""

    def get_media_sub_type_module_class(self, media_type, media_sub_type):
        if (media_type in self.__media_sub_types):
            sub_types_dict = self.__media_sub_types[media_type]
            if (media_sub_type in sub_types_dict):
                media_sub_types_items = dict(sub_types_dict[media_sub_type])
                return media_sub_types_items[self.ITEM_MEDIA_TYPES_MODULE_CLASS]
            else:
                return ""
        else:
            return ""

    def get_media_sub_type_known_names_list(self, media_type, media_sub_type):
        if (media_type in self.__media_sub_types):
            sub_types_dict = self.__media_sub_types[media_type]
            if (media_sub_type in sub_types_dict):
                media_sub_types_items = dict(sub_types_dict[media_sub_type])
                return media_sub_types_items[self.ITEM_MEDIA_TYPES_KNOWN_NAMES_FILE]
            else:
                return ""
        else:
            return ""


    def get_word_file_delimiter(self, word_file_name):
        if (word_file_name in self.__word_files):
            word_file_items = dict(self.__word_files[word_file_name])
            return word_file_items[self.ITEM_WORD_FILE_DELIMITER]
        else:
            return ""

    def get_word_file_file_name(self, word_file_name):
        if (word_file_name in self.__word_files):
            word_file_items = dict(self.__word_files[word_file_name])
            return word_file_items[self.ITEM_WORD_FILE_FILE_NAME]
        else:
            return ""

    def get_word_absolute_file_file_name(self, word_file_name):
        if (word_file_name in self.__word_files):
            word_file_items = dict(self.__word_files[word_file_name])
            return_value = self.get_data_directory() + os.path.sep + word_file_items[self.ITEM_WORD_FILE_FILE_NAME]
            return return_value
        else:
            return ""

    def get_word_file_file_class(self, word_file_name):
        if (word_file_name in self.__word_files):
            word_file_items = dict(self.__word_files[word_file_name])
            return word_file_items[self.ITEM_WORD_FILE_CLASS]
        else:
            return ""

    def get_word_file_module_name(self, word_file_name):
        if (word_file_name in self.__word_files):
            word_file_items = dict(self.__word_files[word_file_name])
            return word_file_items[self.ITEM_WORD_MODULE_NAME]
        else:
            return ""

    def get_data_directory(self):
        return self.__directories[self.DIRECTORY_NAME_DATA]

    def get_log_directory(self):
        return self.__directories[self.DIRECTORY_NAME_LOG]

    def get_config_data_directory(self):
        return self.__directories[self.DIRECTORY_NAME_CONFIG]

    def get_log_format(self):
        return self.__logging[self.LOGGING_FORMAT]

    def get_log_date_format(self):
        return self.__logging[self.LOGGING_DATE_FORMAT]

    def get_log_level(self):
        return self.__logging[self.LOGGING_LEVEL]

    def get_log_console_mode(self):
        return self.__logging[self.LOGGING_CONSOLE_MODE]

    def get_log_file(self):
        return self.__logging[self.LOGGING_FILE]


    def get_log_rotate_mode(self):
        try:
            return self.__logging[self.LOGGING_ROTATE_MODE]
        except KeyError:
            logging.info("No configuration item named %s found", self.LOGGING_ROTATE_MODE)
            return None


    def get_log_rotate_bytes(self):
        try:
            return self.__logging[self.LOGGING_BYTES]
        except KeyError:
            logging.info("No configuration item named %s found", self.LOGGING_BYTES)
            return None

    def get_config_file(self):
        return self.__config_file


    def get_directories(self):
        return self.__directories


    def get_file_name(self):
        return self.__file_name


    def get_media_type_names(self):
        return self.__media_type_names


    def get_word_file_names(self):
        return self.__word_file_names


    def get_logging(self):
        return self.__logging


    def set_config_file(self, value):
        self.__config_file = value


    def set_directories(self, value):
        self.__directories = value


    def set_file_name(self, value):
        self.__file_name = value


    def set_media_type_names(self, value):
        self.__media_type_names = value


    def set_word_file_names(self, value):
        self.__word_file_names = value


    def set_logging(self, value):
        self.__logging = value


    def del_config_file(self):
        del self.__config_file


    def del_directories(self):
        del self.__directories


    def del_file_name(self):
        del self.__file_name


    def del_media_type_names(self):
        del self.__media_type_names


    def del_word_file_names(self):
        del self.__word_file_names


    def del_logging(self):
        del self.__logging

    config_file = property(get_config_file, set_config_file, del_config_file, "get dictionary of config_file's section from configuration file")
    directories = property(get_directories, set_directories, del_directories, "get dictionary of directories section from configuration file")
    file_name = property(get_file_name, set_file_name, del_file_name, "get dictionary of file_names's section from configuration file")
    media_type_names = property(get_media_type_names, set_media_type_names, del_media_type_names, "get dictionary of media_type's section from configuration file")
    word_file_names = property(get_word_file_names, set_word_file_names, del_word_file_names, "get dictionary of word_file_names's section from configuration file")
    logging = property(get_logging, set_logging, del_logging, "get dictionary of logging section from configuration file")


