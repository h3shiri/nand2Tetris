class Translator:
	"""
	This class should have plenty of utility method for translating
	various statemnt to basic VM language pop/push the whole party.
	"""

	def __init__(self, outfileName):

		self.outFile = open(outfileName, 'w')
		"""
		Due to potential bugs we are going to keep track of the original jack code,
		and each time we generate code we will comment a reference to the source.
		"""


	"""
	writing a push command in the vm syntax, with an optional debug flag for comments.
	"""
	def writePush(self, segment, index, debug = None):
		if segment not in {"constant", "this", "that", "argument", "static", "local", "temp", "pointer"}:
			print("non valid segment")
			return
		string = "push" + " " + segment + " " + str(index)
		string = self.commentIntoVMCode(string, debug)
		self.outFile.write(string)

	"""
	writing a pop command in the vm syntax, with an optional debug flag for comments.
	"""
	def writePop(self, segment, index, debug = None):
		if segment not in {"constant", "this", "that", "argument", "static", "local", "temp", "pointer"}:
			print("non valid segment")
			return
		string = "pop" + " " + segment + " " + str(index)
		string = self.commentIntoVMCode(string, debug)
		self.outFile.write(string)

	# writing an arithmetic command on the vm
	def writeArithmetic(self, command, debug = None):
		if command not in {"add", "sub", "and", "or", "neg", "not", "eq", "gt", "lt"}:
			print("non supported arithmetic command")
			return
		else:
			string = command
			string = self.commentIntoVMCode(string, debug)
			self.outFile.write(string)

	# Writing a vm label command.
	def writeLabel(self, label, debug = None):
		string = "label" + " " + label
		string = self.commentIntoVMCode(string, debug)
		self.outFile.write(string)

	# writing a vm goto command (unconditional)
	def writeGoto(self, label, debug = None):
		string = "goto" + " " + label
		string = self.commentIntoVMCode(string, debug)
		self.outFile.write(string)

	# writing a vm if-goto command (conditional goto).
	def writeIf(self, label, debug = None):
		string = "if-goto" + " " + label
		string = self.commentIntoVMCode(string, debug)
		self.outFile.write(string)

	# writing a function call, note that this is a call to simple VM function.
	def writeCall(self, funcName, nArgs, debug = None):
		string = "call" + " " + funcName + " " + str(nArgs)
		string = self.commentIntoVMCode(string, debug)
		self.outFile.write(string)

	# Writing a vm function declaration.
	def writeFunction(self, funcName, nLocals, debug = None):
		string = "function" + " " + funcName + " " + str(nLocals)
		string = self.commentIntoVMCode(string, debug)
		self.outFile.write(string)

	# writing  a VM return statement.
	def writeReturn(self, debug = None):
		string = "return"
		string = self.commentIntoVMCode(string, debug)
		self.outFile.write(string)

	# Closing the file.
	def closeStream(self):
		self.outFile.close()

	# A utility function for editing an exisiting string according to a debug flag.
	def commentIntoVMCode(self, strTarget, debug = None):
		if debug != None:
			strTarget += (" //" + str(debug) + '\n')
		else:
			strTarget += '\n'
		return strTarget
