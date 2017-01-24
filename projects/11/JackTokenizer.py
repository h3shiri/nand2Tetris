# from JackLanguage import *
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
        "field",
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
    multi = False

    def __init__(self, infile):
        #Opens the file and gets ready to tokenize
        self.original = ""
        self.file = open(infile)
        self.strings = []
        self.token = ""
        self.p1_comments = re.compile(r"^\s*\/?\*")
        self.tokens = self.parseFile()
        self.multi = False
        self.identifiers = []
        self.isFirstQuot = False
        self.isSecondQuot = False
    def removeCommentsFromLine(self, line):
        if line[0] == "/":
            return None
        if line[0] == "*":
            return None

        else:
            return line.split("//", 1)[0].strip(' \t\n\r')

    def removeCommentsFromLine2(self, line):
        if "/*" in line:
            self.multi = True
        if self.multi and "*/" in line:
            line = line.split("*/", 1)[1]
            self.multi = False
            return self.removeCommentsFromLine2(line)
        if self.multi:
            return None
        if self.p1_comments.search(line) != None:
            return None
        if line.strip().endswith("*/"):
            line = line.split("*", 1)[0].strip(' \t\n\r')
            return line
        else:
            return line.split("//", 1)[0].strip(' \t\n\r')

    def fixString(self, toFix):
        global symbols
        stripped = toFix.strip()

        symbol = stripped[-1:]
        if (symbol.isalpha() or symbol.isdigit()):
            print("|" + stripped + "|")
            print("|" + toFix + "|")
            print(self.strings)
            if toFix.strip() in self.strings:
                return toFix.strip()
            if stripped[:-1] in self.strings:
                return stripped
            elif stripped in self.strings:
                return stripped
            elif (stripped + " ") in self.strings:
                return stripped + " "
            return stripped
        stripped = stripped[:-2]
        stripped +=symbol + " "
        return stripped


    def fixTokens(self,tokens):
        fixedTokens = []
        quotOpen = False
        stringWithSpaces = ""
        start = 0
        end = 0
        for token in tokens:
            if token == "<":
                fixedTokens.append("&lt;")
            elif token == ">":
                fixedTokens.append("&gt;")
            elif token == "&":
                fixedTokens.append("&amp;")
            else:
                fixedTokens.append(token)
        return fixedTokens

    def findStrings(self, line):
        open = False
        curString = ""
        for char in line:
            if char ==  '"':
                if open == False:
                    open = True
                    continue
                elif open == True:
                    self.strings.append(curString)
                    open = False
            elif open == True:
                curString += char


    def parseFile(self):
        #This parses the file and returns array of tokens
        cleanLines = []
        tokens = []
        for line in self.file.readlines():
            cleanLine = self.removeCommentsFromLine2(line)
            if cleanLine != None:
                self.findStrings(cleanLine)
            if cleanLine != None:
                cleanLines.append(cleanLine)

        curToken = ""
        for cleanLine in cleanLines:
            #tokens += re.split(r"(\W+)", cleanLine)
            openString = False
            curString = ""
            if curToken != "" and curToken != " ":
                tokens.append(curToken)
            curToken = ""
            i = 0
            for char in cleanLine:

                if char == '"':
                    if openString:
                        tokens.append(curString)
                        openString = False
                    else:
                        openString = True
                else:

                    if openString:
                        curString += char
                    elif char in symbols:
                        if curToken != "" and curToken!= " ":
                            tokens.append(curToken)
                            curToken = ""
                            tokens.append(char)
                        else:
                            if char != " ":
                                tokens.append((char))
                    elif char == " ":
                        if curToken != " ":
                            tokens.append(curToken)
                        curToken = ""
                    else:
                        curToken += char


        return self.fixTokens(list(filter(bool, tokens)))
            #tokens += [token for token in re.split(r"(\W)", cleanLine) if token.strip()]

        #tokens = [x.strip(' ') for x in tokens]

        #return self.fixTokens(list(filter(bool, tokens)))

    def hasMoreTokens(self):
        #Do we have more tokens?
        return len(self.tokens) > 0

    def advance(self):
        self.token = self.tokens[0]
        self.tokens.pop(0)

    def getTypeOfToken(self):
        global keywords, symbols
        if self.token in self.strings:
            return "stringConstant"
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
    #Changed the name to T2 so we don't get some override issues.
    filename = jackFile[:-5] + "T2.xml"
    xml = open(filename, 'w')
    xml.write("<tokens>\n")
    return xml

def PassingTokenArray(jackFile):
    resArray = []
    tokenizer = JackTokenizer(jackFile)
    while (tokenizer.hasMoreTokens()):
        tokenizer.advance()
        data = tokenizer.token
        type = tokenizer.getTypeOfToken()
        tup = (type, data)
        resArray.append(tup)
    return resArray

#This function writes to the XML file
#Evtually shall be commented out, we only need an array of token objects.

def main():
    tokenizer = JackTokenizer(sys.argv[1])
    xml = getXmlFromJack(sys.argv[1])
    while (tokenizer.hasMoreTokens()):
        tokenizer.advance()
        token = tokenizer.token
        type = tokenizer.getTypeOfToken()
        writeToXML(xml, type, token)
    xml.write("</tokens>")

#main()