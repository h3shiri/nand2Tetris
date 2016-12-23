import sys
import os

sysInput = sys.argv[1]

class Parser:
    """
    Parser class as suggested in the project architecture
    """
    def __init__(self, fileToParse):
        #open the file first only to initialze self.fileLength to the file length
        self.file = open(fileToParse, 'r')
        self.fileLength
        self.file.readlines()
        self.fileLength = self.file.tell()
        self.file.close()
        #Now open the file again for parsing, and initialize self.pos to 0
        self.file = open(fileToParse, "r")
        self.pos = 0
        self.curCommand = []
        self.commandsDict = { #ca stands for C_ARITHMETIC
            'add': "ca", 'sub': "ca", 'neg': "ca", 'eq': "ca", 'gt': "ca", 'ls': "ca", 'and': "ca", 'or': "ca",
            'not': "ca",
            'push': "push", 'pop': "pop"
        }

    def hasMoreCommands(self):
        """
        boolean function checks if there are more commands
        :return:
        """
        return  self.pos < self.fileLength

    def advance(self):
        line = self.file.readline()
        self.pos = self.file.seek()
        lineWithoutComments = line.split("/")[0]
        if len(lineWithoutComments) == 0:
            self.advance()
        else:
            self.curCommand = lineWithoutComments.split(" ")

    def commandType(self):
        command = self.curCommand[0]
        if command == None:
            pass
            #TO-DO: HOW WOULD WE HANDLE THIS? maybe pass is enough. NEED TO CHECK!
        else:
            return command

    def arg1(self):
        return self.curCommand[1]

    def arg2(self):
        return self.curCommand[2]


class CodeWriter:
    """
    CodeWriter class as suggested in the project architecture
    """
    def __init__(self, file):
        self.fileToWrite = open(file, 'w')
        self.begin = False
        self.fileName = ''

    def setFileName(self, fileName):
        self.begin = True
        self.fileName = fileName

    def writeArithmetic(self, command):
        pass

    def writePushPop(self, command, segment, index):
        pass

    def close(self):
        self.fileToWrite.close()

def runOneFile(file):
    """
    This function creates 1 asm file out of a vm file.
    :param file:
    :return:
    """
    global sysInput
    parser = Parser(file) #set a new Parser object with the input file
    fileName = file.split('.vm')[0] #parse the name and give to a new CodeWriter
    codeWrite = CodeWriter(fileName)
    while(parser.hasMoreCommands()):
        parser.advance()
        command = parser.commandType()
        arg1 = parser.arg1()
        arg2 = parser.arg2()

        if command == "ca":
            codeWrite.writeArithmetic(arg1)
        elif command == "push" or command == "pop":
            codeWrite.writePushPop(command, arg1, arg2)
        else:
            pass # More options in project 8

def main():
    """
    Main program, check if input is a directory or just a vm file, and perform the task on files/file.
    :return:
    """
    global sysInput
    def listVmInDir(dir):
        """
        Nested function to get the list of VM files(if its a directory)
        :param dir:
        :return:
        """
        files = []
        for file in os.listdir(sysInput):
            if file.endswith(".vm"):
                files.append(file)
        return files

    isDir = os.path.isdir(sysInput)
    if isDir:
        listOfVm = listVmInDir(sysInput)
        for file in listOfVm:
            runOneFile(file)
    else:
        runOneFile(sysInput)



if __name__ == '__main__': main()
