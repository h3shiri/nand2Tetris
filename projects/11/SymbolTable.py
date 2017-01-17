#import xml.etree.ElementTree as ET
#TODO: parse the xml tree in a neat and organize way.

class SymbolTable:
	"""
	This class represents an aymbol or the equivalent of a given node.
	where each node is a given 
	All tree traversing should be done with such objects as nodes. 
	"""
	TYPE = 0
	KIND = 1
	INDEX = 2
	def __init__(self, fatherScope = None, scopeType = None):
		# Here we have a ref to the father scope.
		self.fatherScope = fatherScope
		# Should be set on "class" or "subroutine".
		self.scopeType = scopeType 
		self.staticCounter = 0
		self.fieldCounter = 0
		self.argumentCounter = 0
		self.varCounter = 0
		# A dictionary, the keys are the labels names and they point to various flags.
		# name -> [Type, Kind, index]
		self.elements = dict()
		# offset dictionary
		self.offsets = {"static":0, "field":0, "argument":0, "var":0}
		
	# Addidng a label to the current scope.	 
	def addLabel(self, kind, type, name):
		classKinds = {"static", "field"}
		subroutineKinds = {"argument", "var"}
		# If we try to define an already existing label
		if name in self.getLocalLabels():
			pass
			#TODO: possible error overwriting an exisiting label.
		if kind not in (classKinds | subroutineKinds):
			pass
			#TODO: error non existing type.
		if ((kind in classKinds and self.scopeType != "class") or
		   (kind in subroutineKinds and self.scopeType != "subroutine")) :
			pass
			# TODO: non appropriate scope error.

		offset = self.VarCount(kind)
		#Updating the ofset value in this scope
		self.offsets[kind] += 1
		# Inserting the relevant values in our table.
		self.elements[name] = [type, kind, offset]
	
	# Returning how many of this kind we have already defined
	def VarCount(self, kind):
		return self.offsets[kind]
	
	# Returns relevent kind, if label exists in this Scope, else returns None.
	def KindOf(self, name):
		return self.localAttributeGetter(name, KIND)

	# Returns relevent type, if label exists in this Scope, else returns None.
	def TypeOf(self, name):
		return self.localAttributeGetter(name, TYPE)

	# Returns relevent index, if label exists in this Scope, else returns None.
	def IndexOf(self, name):
		return self.localAttributeGetter(name, INDEX)

	# A utility function for all the getter attributes functions (TypeOf, IndexOf, KindOf)
	def localAttributeGetter(self, name, attrIndex):
		if name not in self.getLocalLabels():
			return None
		else:
			attributes = self.elements[name]
			return attributes[attrIndex]

	# returns all the local labels.
	def getLocalLabels(self):
		return self.elements.keys()

	"""
	This is an important function fetching a target label,
	in case we don't find it in the local scope we shall start traversing.
	@return : relevant element attributes, return None if we failed to find it (plus error). 
	"""
	def getElementAttributes(self, target):
		if target in self.getLocalLabels():
			return self.elements[target]
		if self.hasFather():
			#We should oly be able to climb this tree once.
			return self.getFather().getElementAttributes(target)
		else:
			print("Non existing element")
			return None


	# Checks whether this node has a parent, useful in all recursions.
	def hasFather(self):
		if self.fatherScope != None:
			return True
		else:
			return False

	#Getter function for father scope
	def getFather(self):
		return self.fatherScope

	# Setting the father scope, note that we actually have only 2 scopes Class/Subroutine.
	def setFather(self, fatherScope):
		self.fatherScope = fatherScope




#TODO: check the scope limitation is it actually just class and subroutine scopes (2)
#which means no internal declarations this makes our ordeal significantly simpler??
class Tree:
	"""
	This class represent our parsing tree.
	Each Node is a symbol Table, and has internal methods for
	fetching variables along the tree.
	root scope should be class element, and respective leaves should be subroutines scopes.
	"""
	def __init__(self, xmlFile):
		self.classTableRoot = SymbolTable(None, "class") # Class Scope Node
		self.subroutineScopes = [] # fill this up as you parse the file.
	

	def startSubroutine(self):
		newSubroutineScope = SymbolTable(self.classTableRoot, "subroutine")
		self.subroutineScopes.append(newSubroutineScope)

	"""
	@name: A new identifier representing the label name
	@type: The given type for this terminal if applicable.
	Static and field have class scope.
	Arg and Var have a subroutine scope.
	This should make our life simple.
	"""
	
