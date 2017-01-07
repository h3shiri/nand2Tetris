
from JackLanguage import *

class JackTokenizer:

    TOKEN_TYPES = ["KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"]

    def __init__(self, infile):
        #Opens the file and gets ready to tokenize
        pass

    def hasMoreTokens(self):
        #Do we have more tokens?
        pass

    def advance(self):
        #gets next token from input and makes it next token, only called if hasMoreTokens is true
        pass

    def keyWord(self):
        #returns the keyword which is the current token. Should be called only when tokenType() is KEYWORD
        pass

    def symbol(self):
        #Returns the char which is the cur token, called only if tokenType() is SYMBOL
        pass

    def identifier(self):
        #returns current token only if tokenType() is IDENTIFIER
        pass

    def intVal(self):
        #returns the int value only if tokenType() is INT_CONST
        pass

    def stringVal(self):
        #returns the string value only if tokenType() is STRING_CONST
        pass

    