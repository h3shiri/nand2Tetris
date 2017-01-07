

class JackParser:

    def __init__(self, infile, outfile):
        #Creates a new compliation engine with the given input and output
        #the next routine called must be compileClass()
        pass
    def compileClass(self):
        #compiles a complete class
        pass
    def compileClassVarDec(self):
        #Compiles a static or field declaration
        pass
    def compileSubRoutine(self):
        #compiles a method function or constructor
        pass
    def compileParametersList(self):
        #compiles a parameters list, not including the enclosing "()"
        pass
    def compileVarDec(self):
        #Compiles a var declaration
        pass
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
    def compileTerm(self):
        #See supplied API for more details
        pass
    def compileExpressionList(self):
        #compiled a (possibly empty) comma seperated list of expressions
        pass
