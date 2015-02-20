
class obj_base:
			#  01 2
	objdict = "*@\\";
	def passable ():
		return True;
	def __init__ (self, symbol):
		if type(symbol) is int:
			self.symbol = obj_base.objdict[symbol];
		else:
			self.symbol = symbol;

	def bestof (objset): # chooses an object from the given array, in order to display the most useful information.
		out = "";
		for i in objset:
			out = i.symbol;
		return out;
#
class obj_terrent:
	def __init__ (self, symbol):
		obj_base.__init__(self, symbol);
	def passable ():
		return False;
#
class obj_item:
	def __init__ (self, symbol, item):
		obj_base.__init__(self, symbol);
		self.item = item;
#
class obj_body:
	def __init__ (self, symbol, health = 25):
		obj_base.__init__(self, symbol);
		self.health = health;
		self.maxhealth = health;
		self.maininv = [];
	def additem (self, toad):
		self.maininv.append(toad);
# ~ #
