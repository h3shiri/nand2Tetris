from JackTokenizer import *
from SymbolTable import *
from VMWriter import *
#TODO: EX11 - upgarde the xml to include new vals for the proper tree building process.
#TODO: switch from xml output to the proper vm output, and slowly change this code (debuging the vm would be inconvenient) 

"""
new vals:
identifier category : (var, argument, static, field, class, subroutine).
presently being defined : aka declaration or call for an existing variable.
flag : whether the variable represnt one of the 4 (var, argument, static, field) 
index : aka the running index assigned by the symbol table.
"""

"""
#Symbols
symbols = [
        "{","}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~",
        "&lt;", "&gt;", "&amp;", "&quot"
    ]
"""
# All the various scope options aka non-terminals.
"""
ScopeTypes = [
    "class", "classVarDec", "subroutineDec", "parameterList", "subroutineBody", "VarDec",
    "statements", "whileStatement", "ifStatement", "returnStatement", "letStatement", "doStatement"
    "expression", "term", "expressionList"    
    ]
"""
class JackParser:

    """
    some guide lines to rewrite of the class
    K(arg) - we keep this argument, should be used in the vm code somehow.
    T(arg) - through this to the trash.
    """
    #Creates a new compliation engine with the given input and output
    def __init__(self, listOfTokens, VMWriter, classRoot):
        # Handles all the output for the VM. 
        self.writer = VMWriter
        # The outer class scope object, stays fixed throught the code.
        self.classScope = classRoot
        # current function scope. TODO:manage this properly from one subroutine to another.
        self.currentSubScope = None 
        # all the actual tokens, stright from the tokenizer.
        self.rawTokens = listOfTokens
        # one and not zero due to initial wrappers of XML.
        self.indentaionMark = 0
        # the given delimeter. TODO: check if you can use a library to fix possible indentation.
        self.delim = "  "
        # Refering to the relational scope location
        self.scopeType = ""
        #the next routine called must be compileClass() which in inside initProcess.

    # terminal_types = ["stringConstant", "keyword", "symbol", "integerConstant", "identifier"]
    
    # returns the requested token as (type, token).
    def popToken(self):
        type, token = self.rawTokens.pop(0)
        return (type, token)

    # Simple function for throwing out the non useful tokens.
    def throwToken(self):
        trashType, trashTOken = self.rawTokens.pop(0)

    # TODO: acually erase this statement from the code.
    # Utility function for processing the next tokens simply as they are into the xml file.
    def writingSimpleToken(self):
        type, token = self.rawTokens.pop(0)
        # We don't need to write anymore to the xml.
        # self.writeWithIndentation(type, token)

    
    # throwing several noncompiled elements to the trash basically.
    def writingFewSimpleTokens(self, iterations):
        for i in range(iterations):
            self.writingSimpleToken()

    #compiles a complete class
    def compileClass(self):
        self.scopeType = "class"
        # getting the T('class'), K(name) and T('{')
        self.throwToken()
        type, token = self.popToken()
        self.classScope.setName(token)
        self.throwToken()

        #In case we have more tokens we proceed, to the classVarDec or subroutineDec 
        while(self.hasAnyTokensLeft()):
            
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

            # EmptyClass or closing the class.
            elif token == '}':
                self.throwToken()
            else:
                print("Non Valid format: within clas scope"+'\n')
                return


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
        # writing the fixed strings down such as 'constructor', type, name, '('
        self.writingFewSimpleTokens(4)
        # writing additional optional param list
        self.compileParametersList()
        #the closing brackets ')'
        self.writingSimpleToken()
        # entering the subroutine body.
        self.compileSubroutineBody()

    # compilation function for the subroutine body.
    def compileSubroutineBody(self):
        self.scopeType = "subroutineBody"
        self.writeOpenClause("subroutineBody")
        self.indentaionMark += 1
        self.writingSimpleToken() # '{'
        # covering all the variables declarations.
        nextTokenType, nextToken = self.rawTokens[0]
        while (nextToken == "var"):
            self.compileVarDec()
            nextTokenType, nextToken = self.rawTokens[0]

        # compiling the various statements
        self.compileStatements()

        self.writingSimpleToken() # '}'
        #closing tag
        self.indentaionMark -= 1
        self.writeClosingClause("subroutineBody")

    #compiles a parameters list, not including the enclosing "()"
    def compileParametersList(self):
        self.scopeType = "parameterList"
        self.writeOpenClause("parameterList")
        self.indentaionMark += 1
        nextTokenType, nextToken = self.rawTokens[0]
        while(nextToken != ')'):
            self.writingSimpleToken()
            nextTokenType, nextToken = self.rawTokens[0]
        self.indentaionMark -= 1
        self.writeClosingClause("parameterList")
            
    # Compiling a sequence of variables including the ';'       
    def compileVariables(self):
        self.scopeType = "variablesList"
        # begin by writing first mendatory first variable type and name.
        self.writingFewSimpleTokens(2)
        #we are going to iterate until we reach a semicolon.
        nextTokenType, nextToken = self.rawTokens.pop(0)
        while (nextToken != ';'):
            self.writeWithIndentation(nextTokenType, nextToken)
            nextTokenType, nextToken = self.rawTokens.pop(0)
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
        
    #Compiles a sequence of statements, not including the enclosing "{}"
    def compileStatements(self):
        self.writeOpenClause("statements")
        self.indentaionMark += 1
        nextTokenType, nextToken = self.rawTokens[0]
        SOS = {"let", "if", "while", "do", "return"} # "abbreviation  StatementOpennerSet"
        while nextToken in SOS:
            if nextToken == "let":
                self.compileLet()
            elif nextToken == "if":
                self.compileIf()
            elif nextToken == "do":
                self.compileDo()
            elif nextToken == "return":
                self.compileReturn()
            elif nextToken == "while":
                self.compileWhile()
            else:
                #TODO: crazy error.
                pass
            # Updating for next iteration.
            nextTokenType, nextToken = self.rawTokens[0]

        self.indentaionMark -= 1
        self.writeClosingClause("statements")

    #compiles a do statement
    def compileDo(self):
        self.scopeType = "doStatemnt"
        self.writeOpenClause("doStatement")
        self.indentaionMark += 1
        # Unloading the 'do', subroutineName.
        self.writingSimpleToken()
        # compiling the subroutine.
        self.compileSubroutineCall()
        self.writingSimpleToken() # "catching the semicolon from the do statement"
        # Closing the expression list
        self.indentaionMark -= 1
        self.writeClosingClause("doStatement")

    def compileSubroutineCall(self):
        nextTokenType, nextToken = self.rawTokens[0]
        followerType, followerToken = self.rawTokens[1]
        if followerToken == '(':
            # case one subroutine name and calling expList.
            self.scopeType = "subroutineLocalMethodCall"
            self.writingFewSimpleTokens(2)
        elif followerToken == '.':
            self.scopeType = "foreignFunctionCall"
            # calling foreign method aka nameV + '.' + nameM + '('
            self.writingFewSimpleTokens(4)
        else:
            #TODO: non-valid function call ERROR
            pass

        self.compileExpressionList()
        self.writingSimpleToken() # "closing bracket for the expL ')"

    #compiles a let statement
    def compileLet(self):
        self.scopeType = "letStatement"
        self.writeOpenClause("letStatement")
        self.indentaionMark += 1
        # unloading the "let", and varName
        self.writingFewSimpleTokens(2)
        nextTokenType, nextToken = self.rawTokens[0]
        if (nextToken == '['): # " '[' exp ']' "
            self.scopeType = "arrayInLetStatement"
            self.writingSimpleToken()
            self.compileExpression()
            self.writingSimpleToken()

        # getting into the subsitution part
        self.writingSimpleToken() # "the equality"
        self.compileExpression()
        self.writingSimpleToken() # "getting the semicolon"
        self.indentaionMark -= 1
        self.writeClosingClause("letStatement")

    # compiling the while condition
    def compileWhile(self):
        self.scopeType = "whileStatement"
        self.writeOpenClause("whileStatement")
        self.indentaionMark += 1
        # unload the "while" and '('
        self.writingFewSimpleTokens(2)
        self.compileExpression()
        self.writingFewSimpleTokens(2) # "closing ')' and openning '{' "
        self.compileStatements()
        self.writingSimpleToken() # "closing '}' "
        self.indentaionMark -= 1
        self.writeClosingClause("whileStatement")

    # compiling a return statement
    def compileReturn(self):
        self.scopeType = "returnScope"
        self.writeOpenClause("returnStatement")
        self.indentaionMark += 1
        # unloading the 'return' str
        self.writingSimpleToken()
        # probing for an expression.
        nextTokenType, nextToken = self.rawTokens[0]
        if nextToken != ';':
            self.compileExpression()
        self.writingSimpleToken() # "reaching for the semicolon"
        self.indentaionMark -= 1
        self.writeClosingClause("returnStatement")

    # compiling the if statement and including the possibility for else.
    def compileIf(self):
        self.scopeType = "ifStatement"
        self.writeOpenClause("ifStatement")
        self.indentaionMark += 1
        self.writingFewSimpleTokens(2) # "if and '('"
        self.compileExpression()
        self.writingFewSimpleTokens(2) # "closing ')' and opening '{'"
        self.compileStatements()
        self.writingSimpleToken() # " closing '}' "
        # probing for an "else" token
        nextTokenType, nextToken = self.rawTokens[0]
        if nextToken == "else":
            self.writingFewSimpleTokens(2)
            self.compileStatements()
            self.writingSimpleToken()

        self.indentaionMark -= 1
        self.writeClosingClause("ifStatement")

    # compiling an expression we have atleast one term, not including out most encapsulating ().
    def compileExpression(self):
        nextTokenType, nextToken = self.rawTokens[0]
        while (nextToken not in {')', ',', ']', ';'}):
            self.scopeType = "insideAnExp"
            self.wrappingNonTerminalFunc("expression", "compileTerm")
            self.compileTerm()
            nextTokenType, nextToken = self.rawTokens[0]
    
    # A utility function helping to clear up the the compileTerm routine.
    # TODO: fix the 'this' option, perhaps pass the follower token as well for obj refrences.
    def compileConstantToken(self, nextTokenType, nextToken):
        if nextTokenType == "stringConstant":
            # OS: String.new(length)
            length = len(nextToken)
            self.writer.writePush("constant", length)
            self.writer.writeCall("String.new", 1)
            for x in xrange(length):
                # pushing the argument for the String.appendChar(nextChar).
                self.writer.writePush("constant", nextToken[x])
                self.writer.writeCall("String.appendChar", 1)

        elif nextTokenType == "integerConstant":
            self.writer.writePush("constant", nextToken)

        elif nextToken in {"null", "false"}:
            # null and flase are mapped to 0
            self.writer.writePush("constant", 0)
        elif nextToken == "true":
            # true is mapped to -1.
            self.writer.writePush("constant", 1)
            self.writer.writeArithmetic("neg")
        elif nextToken == "this":
            #TODO: check whether to return the pointer 0, or other obj by the vm. (p.234)
            pass
        else:
            print("non valid constant defenition error"+'\n')
            return

    #See supplied API for more details
    # differentiating between various scenarios (3) using a look ahead token.
    # We also compile additional terms and operands in between.
    def compileTerm(self):
        self.scopeType = "probing For terminals"
        opSet = {'+', '-', '*', '/', "&lt;", "&gt;", "&amp;", '|', '='} # Supported op's
        opDic = {'+': "add", '-':"sub", '*': "Math.multiply", '/':"Math.divide", "&lt;": "lt", "&gt;": "gt",
                "&amp;": "and", '|': "or", '=': "eq", '-':"neg", '~':"not"}
        nextTokenType, nextToken = self.rawTokens[0]
        followTokenType, followToken = self.rawTokens[1]
        # In such a case we should simply push the argument.
        if (nextTokenType in {"integerConstant", "stringConstant"} or nextToken in {"true", "false", "null", "this"}):
            self.scopeType = "simpleTerminal"
            self.compileConstantToken(nextTokenType, nextToken)
            
        #documented in the API   
        elif nextTokenType == "identifier":
            symbols1 = [
            "{","}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~",
            "&lt;", "&gt;", "&amp;", "&quot"]
            if followToken == '[':
                self.scopeType = "arrayProbing"
                # "nameArr , '[' "
                type, nameArr = self.popToken()
                # retrive memory location from symbolTable.
                arrAtt = self.currentSubScope.getElementAttributes(nameArr) # [Type, Kind (segment), index]
                debugMsg = "accessing array:" + nameArr
                # set pointer 1, to the base address of the array from the scope symbol table.
                self.writer.writePush(arrAtt[1], arrAtt[2], debugMsg) 
                self.writer.writePop("pointer", 1)
                self.throwToken() # '['
                self.compileExpression() # calculating the index.
                self.throwToken() # "]"
            elif (followToken in {'(', '.'}): # "dot leads to object calling a function as well"
                self.scopeType = "callToFunctionFromTerm"
                self.compileSubroutineCall()
            # "weak condition, meant just to have a vague feeling"
            elif (followToken in symbols1):
                self.writingSimpleToken()

            else:
                #TODO: print ERROR here for non valid format.
                pass

        # Another expression inside
        elif nextToken == '(':
            self.throwToken() # "moving the openner '(' "
            self.compileExpression()
            self.throwToken() # "closing the exp with ')' "
        #unaryOp case
        elif nextToken in { '-', '~'}:
            # Pushing the term and then activing the unary operand.
            typeToken, opernad = self.popToken()
            vmOp = opDic[opernad]
            self.compileTerm()
            self.writer.writeArithmetic(vmOp)
        else:
            pass
            #TODO: error we should have atleast one term.

        nextTokenType , nextToken = self.rawTokens[0]
        if nextToken in opSet:
            # we push the next term and then call the binary operand on it.
            typeToken, binaryOp = self.popToken()
            self.compileTerm()
            vmOp = opDic[binaryOp]
            if binaryOp in {'+', "&lt;", "&gt;", "&amp;", '|', '='}:
                self.writer.writeArithmetic()
            elif binaryOp in {'*', '/'}:
                ARGS = 2
                self.writer.writeCall(vmOp, ARGS)

        # self reference should be indurable here due to stack poping, checking for op.
               

    # compiles a (possibly empty) comma seperated list of expressions, not including the ()
    def compileExpressionList(self):
        nextTokenType, nextToken = self.rawTokens[0]
        while(nextToken != ')'): # "breaking value adjacent to ';' "
            self.compileExpression()
            nextTokenType, nextToken = self.rawTokens[0]
            if nextToken == ",":
                self.throwToken() # "getting to the next exp, removing the , "

    # Small function for initiating the project.
    def initProcess(self):
        self.compileClass()


    #Check whether we have additional tuples.
    def hasAnyTokensLeft(self):
        return (len(self.rawTokens) > 0)

# TODO: add functionality handling directories, relative paths and the whole family (see ex8).
def main():
    # remove from garbage testing.
    fileName = sys.argv[1]
    listOfTokens = PassingTokenArray(fileName)
    outFile = fileName[:-5] + ".vm"
    writerObj = VMWriter(outFile)
    parser = JackParser(listOfTokens, writerObj)
    parser.initProcess()

if __name__ == "__main__":
    main()

def parseOneFile(fileName):
    listOfTokens = PassingTokenArray(fileName)
    outFile = fileName[:-5] + ".vm"
    writerObj = VMWriter(outFile)
    classRoot = clssNode()
    parser = JackParser(listOfTokens, writerObj)
    parser.initProcess()


    """
    out of office, we only output to the vm now
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
    """
    # Wrapping function for non-terminal type.
    """
    out of order, no xml output in thix ex
    def wrappingNonTerminalFunc(self, nonTerminalName, internalFunc):
        self.writeOpenClause(nonTerminalName)
        self.indentaionMark += 1
        tFunc = getattr(self, internalFunc)
        tFunc()
        self.indentaionMark -= 1
        self.writeClosingClause(nonTerminalName)
    """
    