from JackTokenizer import *

#Symbols
symbols = [
        "{","}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~",
        "&lt;", "&gt;", "&amp;", "&quot"
    ]

# All the various scope options aka non-terminals.
ScopeTypes = [
    "class", "classVarDec", "subroutineDec", "parameterList", "subroutineBody", "VarDec",
    "statements", "whileStatement", "ifStatement", "returnStatement", "letStatement", "doStatement"
    "expression", "term", "expressionList"    
    ]

class JackParser:

    #Creates a new compliation engine with the given input and output
    def __init__(self, listOfTokens, outfileName):
        self.outFile = open(outfileName, 'w')
        self.rawTokens = listOfTokens
        # one and not zero due to initial wrappers of XML.
        self.indentaionMark = 0
        # the given delimeter. TODO: check if you can use a library to fix possible indentation.
        self.delim = "  "
        # Refering to the relational scope location
        self.scopeType = ""


        #the next routine called must be compileClass() which in inside initProcess.

    # terminal_types = ["stringConstant", "keyword", "symbol", "integerConstant", "identifier"]
    #A utility function which I'm not using, there was a recursive notion here.
    def parseNextToken(self, type, token):
        basicTypes = {"stringConstant", "integerConstant", "identifier", "symbol", "keyword"}
        if type in basicTypes:
            self.writeWithIndentation(type, token)
        elif type == "symbol":
            pass
        elif type == "keyword":
            pass
        else:
            #TODO: print a colorful error here.
            pass

    # Utility function for processing the next tokens simply as they are into the xml file.
    def writingSimpleToken(self):
        type, token = self.rawTokens.pop(0)
        self.writeWithIndentation(type, token)
    # Extension for multi iteration.
    def writingFewSimpleTokens(self, iterations):
        for i in range(iterations):
            self.writingSimpleToken()

    #compiles a complete class
    def compileClass(self):
        self.scopeType = "class"
        # getting the 'class', name and '{'
        self.writingFewSimpleTokens(3)

        #In case we have more tokens we proceed, to the classVarDec or subroutineDec 
        while(self.hasAnyTokensLeft()):
            # TODO: remove debugging.
            print(self.scopeType+'\n')
            type, token = self.rawTokens[0]
            # Variables declarations.
            if token in {"field", "static"}:
                self.scopeType = "classVarDec"
                self.compileClassVarDec()
                
            # subroutines declarations.
            elif token in {"constructor", "function", "method"}:
                self.scopeType = "subroutineDec"
                self.compileSubRoutine()
                
            elif token in {"let", "if", "while", "do", "return"}:
                self.scopeType = "StatementsAtClassOuterScope"
                self.compileStatements()

            # EmptyClass
            elif token == '}':
                self.writeWithIndentation(type, token)
            else:
                #TODO: appropriate error, for non valid syntax.
                pass


    #Compiles a static or field declaration
    def compileClassVarDec(self):
        self.scopeType = "ClassVarDec"
        self.writeOpenClause("classVarDec")
        self.indentaionMark += 1
        #writing the apprprpriate static/field string.
        self.writingSimpleToken()
        # dealing with the variables list.
        self.compileVariables()
        self.indentaionMark -= 1
        # Closing tag, scope has been reduced back in compileVariables.
        self.writeClosingClause("classVarDec")

    #compiles a method function or constructor        
    def compileSubRoutine(self):
        self.scopeType = "subroutineDec"
        self.writeOpenClause("subroutineDec")
        self.indentaionMark += 1
        # writing the fixed strings down such as 'constructor', type, name, '('
        self.writingFewSimpleToken(4)
        # writing additional optional param list
        self.indentaionMark += 1
        self.compileParametersList()
        self.indentaionMark -= 1
        #the closing brackets ')'
        self.writingSimpleToken()
        # entering the subroutine body.
        self.compileSubroutineBody()

        # Closing tag, TODO: make sure scope is back in place.
        self.indentaionMark -= 1
        self.writeClosingClause("subroutineDec")

    # compilation function for the subroutine body.
    def compileSubroutineBody(self):
        self.scopeType = "subroutineBody"
        self.writeOpenClause("subroutineBody")
        self.indentaionMark += 1
        self.writingSimpleToken() // '{'
        # covering all the variables declarations.
        nextTokenType, nextToken = self.rawTokens[0]
        while (nextToken == "var"):
            self.compileVarDec()
            nextTokenType, nextToken = self.rawTokens[0]

        # compiling the various statements
        self.compileStatements()

        self.writingSimpleToken() // '}'
        #closing tag
        self.indentaionMark -= 1
        self.writeClosingClause("subroutineBody")

    #compiles a parameters list, not including the enclosing "()"
    def compileParametersList(self):
        self.scopeType = "paramList"
        nextTokenType, nextToken = self.rawTokens[0]
        while(nextToken != ')'):
            nextTokenType, nextToken = self.pop(0)
            self.writeWithIndentation(nextTokenType, nextToken)
            
    # Compiling a sequence of variables including the ';'       
    def compileVariables(self):
        self.scopeType = "variablesList"
        # begin by writing first mendatory first variable type and name.
        self.writingFewSimpleTokens(2)
        #we are going to iterate until we reach a semicolon.
        nextTokenType, nextToken = self.rawTokens[0]
        while (nextToken != ';'):
            nextTokenType, nextToken = self.rawTokens.pop(0)
            self.writeWithIndentation(nextTokenType, nextToken)
        # inserting the semicolon
        self.writeWithIndentation(nextTokenType, nextToken)

    #Compiles a var declaration
    def compileVarDec(self):
        self.scopeType = "varDec"
        self.writeOpenClause("varDec")
        self.indentaionMark += 1
        #writing the 'var' string.
        self.writingSimpleToken()
        self.compileVariables()
        self.indentaionMark -= 1
        self.writeClosingClause("varDec")
        

    def compileStatements(self):
        #Compiles a sequence of statements, not including the enclosing "{}"
        pass

    def compileDo(self):
        #compiles a do statement
        pass

    def compileLet(self):
        #compiles a let statement
        pass

    def compileWhile(self):
        pass

    def compileReturn(self):
        pass

    def compileIf(self):
        pass

    def compileExpression(self):
        pass

    #See supplied API for more details
    def compileTerm(self):
        pass

    #compiled a (possibly empty) comma seperated list of expressions
    def compileExpressionList(self):
        pass

    # Small function for initiating the project.
    def initProcess(self):
        self.outFile.write("<class>\n")
        self.indentaionMark += 1
        self.compileClass()
        self.outFile.write("</class>")

    # Writing into the output file with proper indentation the relevant terminal token.
    def writeWithIndentation(self, type, token):
        delim = self.delim
        offset = self.indentaionMark * delim
        self.outFile.write(offset + "<" + type + "> " + token + " <" + "/" + type + ">\n")

    # Opening clause for a non-terminal type.
    def writeOpenClause(self, type):
        delim = self.delim
        offset = self.indentaionMark * delim
        self.outFile.write(offset + "<" + type + ">" +'\n')

    def writeClosingClause(self, type):
        delim = self.delim
        offset = self.indentaionMark * delim
        self.outFile.write(offset + "</" + type + ">\n")
    #Check whether we have additional tuples.
    def hasAnyTokensLeft(self):
        return (len(self.rawTokens) > 0)

# TODO: add functionality handling directories, relative paths and the whole family (see ex8).
def main():
    # remove from garbage testing.
    fileName = sys.argv[1]
    listOfTokens = PassingTokenArray(fileName)
    outFile = fileName[:-5] + "_test.xml"
    parser = JackParser(listOfTokens, outFile)
    parser.initProcess()

main()
