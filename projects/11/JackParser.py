from JackTokenizer import *
from SymbolTable import *
import VMWriter
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
        self.popped = []
        # The outer class scope object, stays fixed throught the code.
        self.classScope = classRoot
        self.className = ''
        # current function scope. TODO:manage this properly from one subroutine to another.
        self.currentSubScope = None
        self.subRoutineCounter = 0
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
        self.popped.append(trashTOken)

    # TODO: acually erase this statement from the code.
    # Utility function for processing the next tokens simply as they are into the xml file.
    def writingSimpleToken(self):
        if len(self.rawTokens) == 0:
            return
        type, token = self.rawTokens.pop(0)
        self.popped.append(token)
        return type, token
        # We don't need to write anymore to the xml.

    
    # throwing several noncompiled elements to the trash basically.
    def writingFewSimpleTokens(self, iterations):
        tokens = []
        for i in range(iterations):
            tokens.append(self.writingSimpleToken())
        return tokens


    #compiles a complete class
    def compileClass(self):
        self.scopeType = "class"
        # getting the T('class'), K(name) and T('{')
        self.throwToken()
        type, token = self.popToken()
        self.className = token
        self.classScope.classTableRoot.setName(token)
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
                print("Non Valid format: within clasד scope"+'\n')
                return


    #Compiles a static or field declaration
    def compileClassVarDec(self):
        self.scopeType = "ClassVarDec"
        #writing the apprprpriate static/field string.
        self.writingSimpleToken()
        # dealing with the variables list.
        self.compileVariables()
        # Closing tag, scope has been reduced back in compileVariables.

    #compiles a method function or constructor        
    def compileSubRoutine(self):
        self.scopeType = "subroutineDec"
        # writing the fixed strings down such as 'constructor', type, name, '('
        tokens = self.writingFewSimpleTokens(4)
        # writing additional optional param list
        self.name = self.className + "." + tokens[2][1]
        self.classScope.startSubroutine(self.name)
        self.classScope.setCurScope(self.name)
        type = tokens[0][1] #type is function/method/constructor
        self.compileParametersList(type)

        #the closing brackets ')'
        self.writingSimpleToken()

        # entering the subroutine body.
        self.compileSubroutineBody(type)


    # compilation function for the subroutine body.
    def compileSubroutineBody(self, type):
        self.writingSimpleToken()

        self.scopeType = "subroutineBody"

        # covering all the variables declarations.
        nextTokenType, nextToken = self.rawTokens[0]

        while (nextToken == "var"):
            self.compileVarDec()
            nextTokenType, nextToken = self.rawTokens[0]

        numVars = self.classScope.getCurScope().VarCount('var')
        self.writer.writeFunction(self.name, numVars)
        if type == "method":
            self.writer.writePush('argument', 0)
            self.writer.writePop('pointer', 0)
        if type == 'constructor':
            globalVars = self.classScope.VarCount('field')
            self.writer.writePush('constant', globalVars)
            self.writer.writeCall('Memory.alloc', 1)
            self.writer.writePop('pointer', 0)
        # compiling the various statements
        self.compileStatements()

        self.writingSimpleToken() # '}'
        #closing tag
        self.scopeType = 'class'
        self.classScope.setCurScope('class')

    #compiles a parameters list, not including the enclosing "()"
    def compileParametersList(self, type):

        if type == 'method':
            self.classScope.getCurScope().AddLabel('argument', 'self', 'this')
        self.scopeType = "parameterList"
        nextTokenType, nextToken = self.rawTokens[0]

        while(nextToken != ')'):
            type = self.writingSimpleToken()
            if(type[1] == ","):
                type = self.writingSimpleToken()
            name = self.writingSimpleToken()
            self.classScope.getCurScope().addLabel('argument', type[1], name[1])
            nextTokenType, nextToken = self.rawTokens[0]


    # Compiling a sequence of variables including the ';'
    def compileVariables(self):
        self.scopeType = "variablesList"
        # begin by writing first mendatory first variable type and name.
        type, name = self.writingFewSimpleTokens(2)
        self.classScope.getCurScope().addLabel('var', type[1], name[1])
        #we are going to iterate until we reach a semicolon.
        nextTokenType, nextToken = self.writingSimpleToken()
        while (nextToken != ';'):
            name = self.writingSimpleToken()
            if(name[1] == ";"):
                break
            self.classScope.getCurScope().addLabel('var', type[1], name[1])
            nextTokenType, nextToken = self.writingSimpleToken()

    #Compiles a var declaration
    def compileVarDec(self):
        self.scopeType = "varDec"
        #writing the 'var' string.
        token = self.writingSimpleToken()
        self.compileVariables()


    #Compiles a sequence of statements, not including the enclosing "{}"
    def compileStatements(self):
        nextTokenType, nextToken = self.rawTokens[0]
        SOS = {"let", "if", "while", "do", "return"} # "abbreviation  StatementOpenerSet"
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


    #compiles a do statement
    def compileDo(self):
        self.scopeType = "doStatemnt"
       # self.writeOpenClause("doStatement")
        self.indentaionMark += 1
        # Unloading the 'do', subroutineName.
        self.writingSimpleToken()
        # compiling the subroutine.
        self.compileSubroutineCall()
        self.writer.writePop('temp', 0)
        self.writingSimpleToken() # "catching the semicolon from the do statement"
        # Closing the expression list
        self.indentaionMark -= 1

       # self.writeClosingClause("doStatement")

    def compileSubroutineCall(self):
        numLocals = 0
        left = right = full = ''
        nextTokenType, nextToken = self.rawTokens[0]
        left = nextToken
        followerType, followerToken = self.rawTokens[1]
        if followerToken == '(':
            # case one subroutine name and calling expList.
            self.writer.writePush('pointer', 0)
            numLocals += 1
            full =  self.classScope.getName() + left
            self.scopeType = "subroutineLocalMethodCall"
            self.writingFewSimpleTokens(2)
            self.classScope.startSubroutine()
            self.subRoutineCounter += 1

        elif followerToken == '.':
            self.scopeType = "foreignFunctionCall"
            # calling foreign method aka nameV + '.' + nameM + '('
            tokens = self.writingFewSimpleTokens(4)
            right = tokens[2][1]
            if left in self.classScope.getCurScope().elements or left in self.classScope.classTableRoot.elements:
                self.pushHelper(left)
                full = self.classScope.typeOf(left) + "." + right
                numLocals += 1
            else:
                full = left + '.' + right
            self.classScope.startSubroutine(full)
            table = self.classScope.getSubroutine(self.subRoutineCounter)
            self.subRoutineCounter += 1

        else:
            #TODO: non-valid function call ERROR
            pass
        numLocals += self.compileExpressionList()

        self.writer.writeCall(full, numLocals)
        self.writingSimpleToken() # "closing bracket for the expL ')"

    def pushHelper(self, left):
        if left in self.classScope.getCurScope().getLocalLabels():
            if self.classScope.getCurScope().KindOf(left) == 'var':
                self.writer.writePush('local', self.classScope.getCurScope().IndexOf(left))
            elif self.classScope.getCurScope().KindOf(left) == 'arg':
                self.writer.writePush('argument', self.classScope.getCurScope().IndexOf(left))
        else:
            if self.classScope.getCurScope().KindOf(left) == 'static':
                self.writer.writePush('static', self.classScope.getCurScope().IndexOf(left))
            else:
                self.writer.writePush('this', self.classScope.getCurScope().IndexOf(left))

    def popHelper(self, name):
        print(self.classScope.getCurScope().scopeName)
        if name in self.classScope.getCurScope().getLocalLabels():
            if self.classScope.getCurScope().KindOf(name) == 'var':
                self.writer.writePop('local', self.classScope.getCurScope().IndexOf(name))
            elif self.classScope.getCurScope().KindOf(name) == 'argument':
                self.writer.writePop('argument', self.classScope.getCurScope().IndexOf(name))
        else:
            if self.classScope.getCurScope().KindOf(name) == 'static':
                self.writer.writePop('static', self.classScope.getCurScope().IndexOf(name))
            else:
                self.writer.writePop('this', self.classScope.getCurScope().IndexOf(name))
    #compiles a let statement
    def compileLet(self):
        self.writingSimpleToken() # remove the let


        self.scopeType = "letStatement"
        # unloading the "let", and varName
        tokens = self.writingFewSimpleTokens(2)


        name = tokens[0][1]
        nextTokenType, nextToken = self.rawTokens[0]
        if (nextToken == '['): # " '[' exp ']' "
            self.scopeType = "arrayInLetStatement"
            self.writingSimpleToken()
            self.compileExpression()
            self.writingSimpleToken()

        # getting into the subsitution part
        self.compileExpression()
        self.writingSimpleToken() # "getting the semicolon"

        self.popHelper(name)

    # compiling the while condition
    def compileWhile(self):
        self.scopeType = "whileStatement"
        # unload the "while" and '('
        self.writingFewSimpleTokens(2)
        counter = self.classScope.getCurScope().whileCounter
        self.classScope.getCurScope().whileCounter += 1
        self.writer.writeLabel('WHILE_EXP' + str(counter))
        self.compileExpression()
        self.writer.writeArithmetic('not')
        self.writer.writeIf('WHILE_END' + str(counter))
        self.writingFewSimpleTokens(2) # "closing ')' and openning '{' "
        self.compileStatements()
        self.writer.writeGoto('WHILE_EXP' + str(counter))
        self.writer.writeLabel('WHILE_END' + str(counter))
        self.writingSimpleToken() # "closing '}' "

    # compiling a return statement
    def compileReturn(self):
        self.scopeType = "returnScope"
        # unloading the 'return' str
        self.writingSimpleToken()

        # probing for an expression.
        nextTokenType, nextToken = self.rawTokens[0]
        retFlag = True
        if nextToken == ";":
            retFlag = False
            self.writer.writePush('constant', 0)
            self.writer.writeReturn() #CHECK THIS TOMORROW
        #CONTINUE FORM HERE
        if nextToken != ';':
            self.compileExpression()
        self.writingSimpleToken() # "reaching for the semicolon"

    # compiling the if statement and including the possibility for else.
    def compileIf(self):
        self.scopeType = "ifStatement"
        self.writingFewSimpleTokens(2) # "if and '('"
        self.compileExpression()
        self.writingFewSimpleTokens(2) # "closing ')' and opening '{'"
        counter = self.classScope.getCurScope().ifCounter
        self.classScope.getCurScope().ifCounter += 1
        self.writer.writeIf('IF_TRUE' + str(counter))
        self.writer.writeGoto('IF_FALSE' + str(counter))
        self.writer.writeLabel('IF_TRUE' + str(counter))
        self.compileStatements()
        self.writingSimpleToken() # " closing '}' "
        # probing for an "else" token
        nextTokenType, nextToken = self.rawTokens[0]
        if nextToken == "else":
            self.writingFewSimpleTokens(2)
            self.writer.writeGoto('IF_END' + str(counter))
            self.writer.writeLabel('IF_FALSE' + str(counter))
            self.compileStatements()
            self.writingSimpleToken()
            self.writer.writeLabel('IF_END' + str(counter))
        else:
            self.writer.writeLabel('IF_FALSE' + str(counter))

    # compiling an expression we have atleast one term, not including out most encapsulating ().
    def compileExpression(self):

        nextTokenType, nextToken = self.rawTokens[0]

        while (nextToken not in {')', ',', ']', ';'}):
            self.scopeType = "insideAnExp"
       #     self.wrappingNonTerminalFunc("expression", "compileTerm")
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
            for x in range(length):
                # pushing the argument for the String.appendChar(nextChar).
                self.writer.writePush("constant", nextToken[x])
                self.writer.writeCall("String.appendChar", 1)
            self.popToken()
        elif nextTokenType == "integerConstant":
            self.writer.writePush("constant", nextToken)
            self.popToken()
        elif nextToken in {"null", "false"}:
            # null and flase are mapped to 0
            self.writer.writePush("constant", 0)
            self.popToken()
        elif nextToken == "true":
            # true is mapped to -1.
            self.writer.writePush("constant", 0)
            self.writer.writeArithmetic("not")
            self.popToken()

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
            numLocals = 0
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
                self.writer.writeArithmetic(vmOp)
            elif binaryOp in {'*', '/'}:
                ARGS = 2
                self.writer.writeCall(vmOp, ARGS)

        # self reference should be indurable here due to stack poping, checking for op.
               

    # compiles a (possibly empty) comma seperated list of expressions, not including the ()
    def compileExpressionList(self):
        num = 0
        nextTokenType, nextToken = self.rawTokens[0]

        while(nextToken != ')'): # "breaking value adjacent to ';' "
            num += 1
            self.compileExpression()
            nextTokenType, nextToken = self.rawTokens[0]
            if nextToken == ",":
                self.throwToken() # "getting to the next exp, removing the , "
        return num
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
    writerObj = VMWriter.Translator(outFile)
    classRoot = clssNode()
    parser = JackParser(listOfTokens, writerObj,classRoot)
    parser.initProcess()

if __name__ == "__main__":
    main()

def parseOneFile(fileName):
    listOfTokens = PassingTokenArray(fileName)
    outFile = fileName[:-5] + ".vm"
    writerObj = VMWriter.Translator(outFile)
    classRoot = clssNode()
    parser = JackParser(listOfTokens, writerObj, classRoot)
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
    