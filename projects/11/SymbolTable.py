import xml.etree.ElementTree as ET
#TODO: parse the xml tree in a neat and organize way.

class SymbolTable:
	"""
	This class represents an aymbol or the equivalent of a given node.
	where each node is a given 
	All tree traversing should be done with such objects as nodes.
	"""

	def __init__(self, fatherScope = None):
		# We have 
		self.fatherScope = fatherScope
		self.staticCounter = 0
		self.fieldCounter = 0
		self.argumentCounter = 0
		self.varCounter = 0
		# Each element has a label and points to an array of flags and values.
		self.elements = dict()

	# returns all the local elements.
	def getLocalLabels(self):
		return self.elements.keys()

	"""
	This is an important function fetching a target label,
	in case we don't find it in the local scope we shall start traversing.
	"""
	def getElement(self, target):
		pass

	# Checks whether this node has a parent, useful in all recursions.
	def hasParent(self):
		if self.fatherScope != None:
			return True

#TODO: check the scope limitation is it actually just class and subroutine scopes (2)
#which means no internal declarations this makes our ordeal significantly simpler??
class Tree:
	"""
	This class represent our parsing tree.
	Each Node is a symbol Table, and has internal methods for
	fetching variables along the tree.
	The leaves in this tree represent various terminals.
	"""
	def __init__(self, xmlFile):
		self.tree = ET.parse(xmlFile)
		self.root = tree.getroot() # actually a fancy dict.
		self.treeTableRoot = SymbolTable()


	"""from here on is the book API suggestion for symbol table"""
	#TODO: move most of the internal scope functions into the SymbolTable node.
	

	def startSubroutine(self):
		pass

	"""
	@name: A new identifier representing the label name
	@type: The given type for this terminal if applicable.
	Static and field have class scope.
	Arg and Var have a subroutine scope.
	This should make our life simple.
	"""
	def Define(self, name, type, kind,):
		pass

	def VarCount(self, ):
		pass

	def KindOf
