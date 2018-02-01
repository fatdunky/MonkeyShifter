'''
Created on 26Jun.,2017

@author: mcrick
'''
import cmd, logging
from lines.wordcategories.word_category import WordCategory


class WordCategoryCmd(cmd.Cmd):
    """Pass this class a list of unmatched words and line it belongs to. It will loop through providing matches"""
    
    prompt_start = 'Enter Choice: '
    prompt = ''
    intro = "Tuning mode enabled. Processing all unmatched words"

    doc_header = 'Available Commands'
    misc_header = 'Misc Commands'
    undoc_header = 'Undocumented Commands'
    
    ruler = '-'
     
    def __init__(self, unmatched_words_map):
        cmd.Cmd.__init__(self)
        self.__unmatched_words_map = unmatched_words_map
        self.__unmatched_lines = unmatched_words_map.keys()
        self.__unmatched_words = unmatched_words_map.values()
        self.__line_index = 0
        self.__unmatched_words_list_index = 0
        self.__current_line = self.__unmatched_lines[self.__line_index]
        self.__current_unmatched_words_list = self.__unmatched_words[self.__line_index]
        self.__current_unmatched_word = self.__current_unmatched_words_list[self.__unmatched_words_list_index]
                
        self.getUnmatchedWordChoices()

        
    def addDoWordCategory(self, wordCategory, wordCategoryNameShortCut ):
        def innerDo(self, line):
            "Select %s category for word" % wordCategory.__name__
            self.__current_unmatched_word.set_category(wordCategory())
            #self.__matched_words_map[self.__current_unmatched_word] = wordCategoryName
            logging.debug("Setting %s to word category: %s", self.__current_unmatched_word,wordCategory.__name__)          
            return self.next()  
    
        innerDo.__doc__ = "docstring for do_%s" % wordCategoryNameShortCut
        innerDo.__name__ = "do_%s" % wordCategoryNameShortCut
        setattr(WordCategoryCmd,innerDo.__name__,innerDo)
        logging.debug("Adding directory %s to %s", innerDo.__name__ ,WordCategoryCmd.__name__)
    
    def getUnmatchedWordChoices(self):
        wordShortCutMap = {"next":"", "back":"", "next_line":"", "previous_line":"", "EOF":"" ,"end":"", "quit":""}
       
        self.prompt = WordCategoryCmd.prompt_start
        for wordChoice in WordCategory.__subclasses__():
            i = 0
            wordChoiceString = wordChoice.__name__
            logging.debug("Found the following wordCategory for choices: %s", wordChoiceString)

            #pass 1 try all single characters
            #pass 2 try range 0 to i
            #after that, just use the whole word
            passCount = 0
            shortcutFound = False         
            while not shortcutFound :
                if (i >= len(wordChoiceString)):
                    logging.debug("Increasing passcount, resetting i")
                    i = 0
                    passCount += 1
                if (passCount == 0):                  
                    c = wordChoiceString[i]
                elif (passCount == 1):
                    c = wordChoiceString[:i]
                else:
                    logging.info("Out of options, just using whole word for wordChoiceString")
                    c = wordChoiceString
                
                if (c not in wordShortCutMap):                    
                    logging.debug("Setting shortcut char: %s for word category: %s", c, wordChoiceString)                  
                        
                    if (passCount == 0 or passCount == 1):
                        self.addDoWordCategory(wordChoice, c)
                        wordShortCutMap[c] = wordChoiceString
                    
                    if (wordChoiceString not in wordShortCutMap):
                        self.addDoWordCategory(wordChoice, wordChoiceString)
                        wordShortCutMap[wordChoiceString] = wordChoiceString
                        
                    self.prompt += "("+ c + ")" + wordChoiceString + ','
                    shortcutFound = True
                elif (passCount != 0 or passCount != 1):
                    logging.error("Passcount not equal to 0 or 1, and word is allready in map. breaking out of loop")
                    break                   
                i += 1
        self.prompt = self.prompt[:-1] + ": "
                    
    
    def printWordChoices(self):
        logging.info("===============================================")
        logging.info("The following line has unmatched words:")
        logging.info("'%s'",self.__current_line)
        logging.info("-----------------------------------------------")    
        for i, word in enumerate(self.__current_unmatched_words_list):
            if (i == self.__unmatched_words_list_index):
                logging.info("========[%s], current category=(%s)",word.get_text(),word.get_category().__class__.__name__)
            else:
                logging.info("        [%s], current category=(%s)",word.get_text(),word.get_category().__class__.__name__)
      
    def printWordChoiceHeader(self):     
        logging.info("Choose a word category for word [%s], current category=(%s)",self.__current_unmatched_word.get_text(),self.__current_unmatched_word.get_category().__class__.__name__)    
        logging.info("-----------------------------------------------")

    
    def help_back(self):
        logging.info("Go to previous word")
    
    def do_back(self, line):
        self.previous()
    
    def do_end(self, line):
        "Quit categorising Words"
        return True
        
    def do_quit(self, line):
        "Quit categorising Words"
        return True
       
    def help_next(self):
        logging.info("Go to next word")
    
    def do_next(self, line):
        self.next()
    
    def do_next_line(self, line):
        self.next_line()
    
    def do_previous_line(self, line):
        self.previous_line()
    
    def list(self):
        logging.info("**********List of lines**********")
        for i, line in enumerate(self.__unmatched_lines):
            if (i == self.__line_index):
                logging.info("*%s : %s*", line , self.__unmatched_words[i] )
            else:
                logging.info("%s : %s", line , self.__unmatched_words[i] )
        logging.info("*********************************")
    
    def do_list(self,line):
        self.list()
        
        
    def previous_line(self):
        if ((self.__line_index - 1) >= 0):
            self.__line_index-=1
            self.__unmatched_words_list_index = 0
            self.__current_line = self.__unmatched_lines[self.__line_index]
            self.__current_unmatched_words_list = self.__unmatched_words[self.__line_index]
            self.__current_unmatched_word = self.__current_unmatched_words_list[self.__unmatched_words_list_index]
    
    def next_line(self):
        if ((self.__line_index + 1) < len(self.__unmatched_lines)):
            self.__line_index+=1
            self.__unmatched_words_list_index = 0
            self.__current_line = self.__unmatched_lines[self.__line_index]
            self.__current_unmatched_words_list = self.__unmatched_words[self.__line_index]
            self.__current_unmatched_word = self.__current_unmatched_words_list[self.__unmatched_words_list_index]
            return False
        else:
            logging.debug("Reached the end of all lines, quitting loop")
            return True
   
    def next(self):
        if ((self.__unmatched_words_list_index + 1) < len(self.__current_unmatched_words_list)):
            self.__unmatched_words_list_index+=1
            self.__current_unmatched_word = self.__current_unmatched_words_list[self.__unmatched_words_list_index]
            return False
        else:
            logging.debug("Reached the of the current line, going to next line")
            return self.next_line()
        
            
    def previous(self):
        if ((self.__unmatched_words_list_index - 1) >= 0):
            self.__unmatched_words_list_index-=1
            self.__current_unmatched_word = self.__current_unmatched_words_list[self.__unmatched_words_list_index]
        else:
            self.previous_line()
    
    def preloop(self):
        self.printWordChoices()
        self.printWordChoiceHeader()
        
    def onecmd(self, s):
        self.printWordChoices()
        self.printWordChoiceHeader()
        return cmd.Cmd.onecmd(self, s)
    
    def do_EOF(self, line):
        "Exit"
        return True
