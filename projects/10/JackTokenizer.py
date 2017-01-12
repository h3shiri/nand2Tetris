
from JackLanguage import *
import os
import sys
import re

#Keywords
keywords = [
        "int",
        "char",
        "boolean",
        "method",
        "function",
        "constructor",
        "void",
        "var",
        "static",
        "filed",
        "let",
        "do",
        "if",
        "else",
        "while",
        "return",
        "true",
        "false",
        "null",
        "this",
        "class",
    ]
#Symbols
symbols = [
        "{","}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~", "&lt;", "&gt;",
        "&amp;", "&quot"
    ]
class JackTokenizer:

    TOKEN_TYPES = ["KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"]


    def __init__(self, infile):
        #Opens the file and gets ready to tokenize
        self.file = open(infile)
        self.token = ""
        self.tokens = self.parseFile()
        self.identifiers = []
        self.isFirstQuot = False
        self.isSecondQuot = False
    def removeCommentsFromLine(self, line):
        if line[0] == "/":
            return None
        else:
            return line.split("//", 1)[0].strip(' \t\n\r')

    def fixString(self, toFix):
        global symbols
        stripped = toFix.strip()
        symbol = stripped[-1:]
        if (symbol.isalpha()):
            return stripped
        stripped = stripped[:-2]
        stripped +=symbol
        return stripped


    def fixTokens(self,tokens):
        fixedTokens = []
        quotOpen = False
        isString = False
        stringWithSpaces = ""
        for token in tokens:
            if token == "<":
                fixedTokens.append("&lt;")
            elif token == ">":
                fixedTokens.append("&gt;")
            elif token == "&":
                fixedTokens.append("&amp;")
            elif token == '"' or token == '”' :
                if(quotOpen == False):
                    quotOpen = True
                    #fixedTokens.append("&quot")
                    continue
                elif(quotOpen == True):
                    fixedTokens.append(self.fixString(stringWithSpaces))
                    stringWithSpaces = ""
                    quotOpen = False
            else:
                if (quotOpen == True):
                    stringWithSpaces += token + " "
                    continue
                fixedTokens.append(token)
        return fixedTokens

    def parseFile(self):
        #This parses the file and returns array of tokens
        cleanLines = []
        tokens = []
        for line in self.file.readlines():
            cleanLine = self.removeCommentsFromLine(line)
            if cleanLine != None:
                cleanLines.append(cleanLine)
        for cleanLine in cleanLines:
            #tokens += re.split(r"(\W+)", cleanLine)
            tokens += [token for token in re.split(r"(\W)", cleanLine) if token.strip()]

        tokens = [x.strip(' ') for x in tokens]
        return self.fixTokens(list(filter(bool, tokens)))

    def hasMoreTokens(self):
        #Do we have more tokens?
        return len(self.tokens) > 0

    def advance(self):
        self.token = self.tokens[0]
        self.tokens.pop(0)

    def getTypeOfToken(self):
        global keywords, symbols
        if (self.isFirstQuot == True and self.isSecondQuot == False):
            self.isSecondQuot = True
            return "stringConstant"
        elif (self.token == "&quot"):
            if(self.isFirstQuot == False and self.isSecondQuot == False):
                self.isFirstQuot = True
            elif(self.isFirstQuot == True and self.isSecondQuot == True):
                self.isFirstQuot = False
                self.isSecondQuot = False
        if (self.token in keywords):
            return "keyword"
        elif (self.token in symbols):
            return "symbol"
        elif (self.token.isdigit()):
            return "integerConstant"
        else:
            if( self.token.__contains__(" ")):
                return "stringConstant"
            return "identifier"

    def keyWord(self):
        #returns the keyword which is the current token. Should be called only when tokenType() is KEYWORD
        return

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


def writeToXML(file, type, token):
    file.write ("<" + type + "> " + token + " <" + "/" + type + ">\n")

def getXmlFromJack(jackFile):
    filename = jackFile[:-5] + "T.xml"
    xml = open(filename, 'w')
    xml.write("<tokens>\n")
    return xml

def main():
    #This function writes to the XML file
    tokenizer = JackTokenizer(sys.argv[1])
    xml = getXmlFromJack(sys.argv[1])
    while (tokenizer.hasMoreTokens()):
        tokenizer.advance()
        token = tokenizer.token
        type = tokenizer.getTypeOfToken()
        writeToXML(xml, type, token)
    xml.write("</tokens>")
main()