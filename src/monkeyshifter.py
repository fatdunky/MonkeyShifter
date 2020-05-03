#!/usr/bin/python3

'''
Created on 3Dec.,2016

@author: fatdunky
'''

import os, sys, getopt, logging, random
from utilites.logger import Logger
from configuration import Configuration
from cmd_line.word_category_cmd import WordCategoryCmd
from utilites.io import *
from lines.line import Line
from mediatypes.media import Media
from wordcategories.word_category import WordCategory
from wordcategories.unmatched_word_category import UnmatchedWordCategory


DEFAULT_CONFIG_DIR='config'
DEFAULT_CONFIG_FILE='monkey_shifter.cfg'

DEFAULT_LOGGER_FORMAT='%(asctime)s|%(name)s|%(levelname)s|%(message)s'
DEFAULT_LOGGER_DATE_FORMAT='%Y%m%d|%H:%M:%S'
DEFAULT_LOG_DIR='logs'
DEFAULT_LOG_FILE='monkey_shifter.log'
DEFAULT_LOG_LEVEL=logging.DEBUG

DEFAULT_LOG_ROTATE_MODE='size'
DEFAULT_LOG_ROTATE_WHEN='midnight'
DEFAULT_LOG_ROTATE_INTERVAL=1
DEFAULT_LOG_ROTATE_BACKUP_COUNT=30
DEFAULT_CONSOLE_ONLY_MODE=False
DEFAULT_LOG_ROTATE_BYTES=1000000

def print_help():
    print('Usage: monkeyshifter.py [OPTION]... [TARGET DIRECTORY]...')
    print('MonkeyShifter will clean up movie and tv show avi names.')
    print('It will also move the files into their proper directories')
    print('\n')
    print('Options:')
    print('-h, -?, --help                            Show this output.')
    print('-c <file>, --configFile <file>            Configuration File')
    print('-d <directory>, --configDirectory <file>  Configuration File Directory')
    print('-t, --tuning                              Turn on tuning mode. In the mode the MonkeyShifter will only add words to words lists')
    print('                                          the application will not rename or move files into directories ')
    print('-v, --debug, --verbose                    Turn on verbose mode')
    print('-i <file>, --logDirectory <file>          Use the following directory for the log file')
    print('-l <file>, --logFile <file>               Log to the specified log file')
    print('-e, --logLevel                            Set logging level')
    print('-s <file>, --test <file>                  Turn on test mode. No changes will be made to filenames, no files will be moved.')
    print('-x, --console                             Log to console rather then log file')
    print('\n')

def setup_configuration(config_directory,config_file,default_config_dir,default_config_file):
    '''
    Setup configuration
    '''
    return Configuration(config_directory,config_file,default_config_dir,default_config_file)


def setup_logging(console_mode,log_file,log_directory, log_level, rotate_mode, when, interval, backup_count, rotate_bytes):
    '''
    Setup logging
    '''
    if (console_mode == None or console_mode == ""):
        console_mode = DEFAULT_CONSOLE_ONLY_MODE

    if (log_file == None or log_file == ""):
        log_file = DEFAULT_LOG_FILE

    if (log_directory == None or log_directory == ""):
        log_directory = DEFAULT_LOG_DIR

    if (log_level == None or log_level == ""):
        log_level = DEFAULT_LOG_LEVEL

    if (rotate_mode == None or rotate_mode == ""):
        rotate_mode = DEFAULT_LOG_ROTATE_MODE

    if (when == None or when == ""):
        when = DEFAULT_LOG_ROTATE_WHEN

    if (interval == None or interval == ""):
        interval = DEFAULT_LOG_ROTATE_INTERVAL

    if (backup_count == None or backup_count == ""):
        backup_count = DEFAULT_LOG_ROTATE_BACKUP_COUNT

    if (rotate_bytes == None or rotate_bytes == ""):
        rotate_bytes = DEFAULT_LOG_ROTATE_BYTES



    Logger.set_log_directory(log_directory)
    Logger.set_log_file(log_file)
    Logger.set_logging_level(log_level)
    #Logger.set_rotation_file(True, 'midnight', 1, 0)
    Logger.set_rotation_file(DEFAULT_LOG_ROTATE_MODE, when, int(interval), int(backup_count), int(rotate_bytes))
    Logger.update_handler()


def create_media_object(line, delimeters, directory, test_mode):
    '''
    split line into words and create media object
    '''
    logging.info("Create Media Object")

    unmatched_list = []

    retVal =  Media()
    line_obj = Line()
    unmatched_list = line_obj.split_line(line, delimeters)
    logging.debug("Split line into %s",line_obj.get_words())
    retVal.set_line_obj(line_obj)
    retVal.set_file_extension(line_obj.get_last_right_of_dot_in_line())
    logging.debug("Got File Extension %s",retVal.get_file_extension())
    retVal.set_word_count(len(line_obj.get_words()))
    logging.debug("Got Word Count %s",retVal.get_word_count())
    retVal.set_file_name(line)
    logging.debug("Got File Name %s",retVal.get_file_name())
    if os.path.isfile(line):
        retVal.set_absolute_file_name(os.path.abspath(line))
        logging.debug("Line is file: Got Absolute File Name %s",retVal.get_absolute_file_name())
    else:
        retVal.set_absolute_file_name(os.path.abspath(directory + os.path.sep + line))
        logging.debug("Adding directory: Got Absolute File Name %s",retVal.get_absolute_file_name())
    retVal.set_path(os.path.basename(retVal.get_absolute_file_name()))
    logging.debug("Got Path %s",retVal.get_path())
    if(not test_mode):
        retVal.set_size(os.path.getsize(retVal.get_absolute_file_name()))
    else:
        retVal.set_size(random.randint(1024,1000000000))
    logging.debug("Got Size %s",retVal.get_size())

    logging.info("Finished Creating Media Object")

    return unmatched_list, retVal

def load_word_files(config, word_files):
    logging.info("Load word files")
    for word_file_name in list(config.get_word_file_names().values()):
        logging.debug("Loading %s",word_file_name)
        class_string = "wordcategories." + config.get_word_file_module_name(word_file_name) + "." + config.get_word_file_file_class(word_file_name)
        logging.debug("Loading %s",word_file_name)
        class_string = "wordcategories." + config.get_word_file_module_name(word_file_name) + "." + config.get_word_file_file_class(word_file_name)
        logging.debug("Loading class : %s",class_string)
        word_class = load_class(class_string)
        word_class = word_class()
        logging.debug("Setting file name : %s in %s",config.get_word_absolute_file_file_name(word_file_name), config.get_word_file_file_class(word_file_name))
        word_class.set_file(config.get_word_absolute_file_file_name(word_file_name))
        logging.debug("Setting class name : %s in %s",config.get_word_file_file_class(word_file_name), config.get_word_file_file_class(word_file_name))
        word_class.set_class_var(config.get_word_file_file_class(word_file_name))
        logging.debug("Setting delimiter : %s in %s",config.get_word_file_delimiter(word_file_name), config.get_word_file_file_class(word_file_name))
        word_class.set_delimiter(config.get_word_file_delimiter(word_file_name))
        logging.debug("Setting config_name : %s in %s", word_file_name, config.get_word_file_file_class(word_file_name) )
        word_class.set_config_name(word_file_name)
        logging.debug("Loading word file: %s", config.get_word_file_file_class(word_file_name))
        word_class.load_file()
        word_files[word_file_name] = word_class
        WordCategory.wordCategories[word_file_name] = word_class

    return word_files


def load_media_type_class(config, media_type_name,media_types):
    logging.debug("Loading %s",media_type_name)
    class_string = "mediatypes." + config.get_media_type_module_name(media_type_name) + "." + config.get_media_type_module_class(media_type_name)
    logging.debug("Loading class : %s",class_string)
    media_type_class = load_class(class_string)
    media_type_class = media_type_class()
    logging.debug("Loading media type(%s) extensions %s",media_type_name,config.get_media_type_extensions(media_type_name))
    media_type_class.set_extensions(config.get_media_type_extensions(media_type_name))
    logging.debug("Loading media type(%s) destinations directory %s",media_type_name,config.get_media_type_destination_dir(media_type_name))
    media_type_class.set_destination_dir(config.get_media_type_destination_dir(media_type_name))
    logging.debug("Loading media type(%s) known_names_list %s",media_type_name,config.get_media_type_known_names_list(media_type_name))
    media_type_class.set_known_names_file_name(config.get_media_type_known_names_list(media_type_name))
    media_types[media_type_name] = media_type_class

    return media_types

def load_media_sub_type_class(config, media_sub_type_name,media_type_name,media_types):
    logging.debug("Loading %s - %s",media_type_name,media_sub_type_name)
    class_string = "mediatypes." + config.get_media_sub_type_module_name(media_type_name,media_sub_type_name) + "." + config.get_media_sub_type_module_class(media_type_name,media_sub_type_name)
    logging.debug("Loading subtype class : %s",class_string)
    media_type_class = load_class(class_string)
    media_type_class = media_type_class()
    #logging.debug("Loading media type(%s - %s) extensions %s",media_type_name,media_sub_type_name,config.get_media_sub_type_extensions(media_type_name,media_sub_type_name))
    #media_type_class.set_extensions(config.get_media_sub_type_extensions(media_type_name,media_sub_type_name))
    logging.debug("Loading media sub type(%s - %s) destinations directory %s",media_type_name,media_sub_type_name,config.get_media_sub_type_destination_dir(media_type_name,media_sub_type_name))
    media_type_class.set_destination_dir(config.get_media_sub_type_destination_dir(media_type_name,media_sub_type_name))
    logging.debug("Loading media sub type(%s - %s) known_names_list %s",media_type_name,media_sub_type_name,config.get_media_sub_type_known_names_list(media_type_name,media_sub_type_name))
    media_type_class.set_known_names_file_name(config.get_media_sub_type_known_names_list(media_type_name,media_sub_type_name))
    media_types[media_type_name] = media_type_class

    return media_types

def load_media_sub_types(config, media_type_name, media_sub_types):
    logging.info("Load media sub types")
    for media_sub_type_name in config.get_media_type_subtypes(media_type_name):
        if (media_sub_type_name and media_sub_type_name.split()):
            load_media_sub_type_class(config, media_sub_type_name,media_type_name,media_sub_types)
    return media_sub_types

def load_media_types(config, media_types):
    logging.info("Load media_types")
    for media_type_name in list(config.get_media_type_names().values()):
        load_media_type_class(config, media_type_name,media_types)
        load_media_sub_types(config, media_type_name,media_types)
    return media_types

def parse_file_names(file_names, line_delimeters,target_directory,test_mode):
    logging.info("Parse file names")
    split_lines = []
    unmatached_words_map = {}

    for line in file_names:
        (current_unmatched_word_list, media) = create_media_object(line,line_delimeters,target_directory,test_mode)
        split_lines.append(media)
        if (len(current_unmatched_word_list) > 0):
            unmatached_words_map[line] = current_unmatched_word_list

    for line in split_lines:
        logging.debug("%s",line.get_line_obj().get_words())

    return (split_lines, unmatached_words_map)


def main(argv):

    config_file = ''
    config_directory = ''
    data_directory = ''

    tuning_mode = False
    verbose_mode = False

    log_file=''
    log_directory=''
    log_level= "DEBUG"

    test_mode = False
    test_file = ''
    console_mode = False
    config = None

    word_files = {}
    words = {}

    #We want a map of to module
    media_types = {}


    names_to_parse = []
    target_directory = ""

    unmatched_words_map = {}

    base_folder = os.path.abspath(os.path.dirname(__file__))

    DEFAULT_CONFIG_DIR = os.path.join(base_folder, "../config")
    DEFAULT_CONFIG_FILE = "monkey_shifter.cfg"

    config_file = DEFAULT_CONFIG_FILE

    '''
    Handle command line arguments
    '''

    try:
        opts, args = getopt.getopt(argv,"h?c:d:tvls:i:",["help","config_file=","config_directory=","tuning","debug","verbose","log_file=","log_level","log_directory=","test"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help", "-?"):
            print_help()
            sys.exit()
        elif opt in ("-c", "--config_file"):
            config_file = arg
        elif opt in ("-d", "--config_directory"):
            config_directory = arg
        elif opt in ("-t"):
            tuning_mode = True
        elif opt in ("-v", "--debug", "--verbose"):
            verbose_mode = True
        elif opt in ("-l", "--log_file"):
            log_file = arg
        elif opt in ("-e", "--log_level"):
            log_level = arg
        elif opt in ("-s", "--test"):
            test_mode = True
            test_file = arg
        elif opt in ("-x", "--console"):
            console_mode = True

    if (len(args) > 1):
        print_help()
        sys.exit(1)
    elif (len(args) == 1):
        target_directory = args[0]
        if ( not os.path.isdir(target_directory)):
            logging.error("Specified directory does not exits or is not a directory. Defaulting to current directory")
            target_directory = os.getcwd()
    else:
        logging.error("No directory specified. Using current directory")
        target_directory = os.getcwd()


    config = setup_configuration(config_directory,config_file, DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_FILE)
    if (config_directory == ""): config_directory = config.get_config_directory()
    if (data_directory == ""): data_directory = config.get_data_directory()
    if (log_directory == ""): log_directory = config.get_log_directory()

    if (console_mode == False): console_mode = bool(config.get_log_console_mode())
    if (log_file == ""): log_file = config.get_log_file()
    if (log_level == ""): log_level = config.get_log_level()
    #def setup_logging(console_mode,log_file,log_directory, log_level, rotate_mode,
    # when, interval, backup_count, rotate_bytes):

    setup_logging(console_mode,log_file,log_directory, log_level, None, None, None, None, None)

    line_delimeters = config.get_file_name_delimiters()

    #load word files
    word_files = load_word_files(config, word_files)

    #load media types
    media_types = load_media_types(config, media_types)



    if (test_mode and test_file != ""):
        logging.info("Load test list of file names from %s",test_file)

        names_to_parse = read_file(test_file)

        #Split each line into words
        logging.info("Found %i test file names",len(names_to_parse))
    else:
        #Load list of file names

        logging.info("Load target list of file names in %s",target_directory)
        names_to_parse = os.listdir(target_directory)

        #Split each line into words
        logging.info("Found %i file names",len(names_to_parse))


    (split_lines, unmatched_words_map) = parse_file_names(names_to_parse, line_delimeters, target_directory, test_mode)


    if (not tuning_mode):
        logging.info("Tuning mode enabled. Processing all unmatched words")
        inputCmd = WordCategoryCmd(unmatched_words_map)
        inputCmd.cmdloop()

    #logging.debug("done, newMatchedwords=[%s]",unmatched_words_map)

    for key, value_list in list(unmatched_words_map.items()):
        #logging.debug("Word word [%s], list [%s]", key, list)
        for word in value_list:
            logging.debug("Adding [%s] to word list, category [%s]", word.get_text(),word.get_category().get_config_name())
            #word.get_category().add_new_word(word.get_text)
            #existing_list = word_files[word.get_category().get_config_name()]
            #existing_list.append(word.get_text)

    logging.debug("%s", word_files)
    for word_category_name, word_category in list(word_files.items()):
        logging.debug("%s wordCat [%s]", word_category ,word_category_name)
    
  
    for line in split_lines:
        logging.debug("split_lines [%s]", line)

    #add word diff score






if __name__ == '__main__':
    main(sys.argv[1:])