import random;
from mapobject import *;

class area:
	"""Class containing all the data and numbers of an entire 32x32 terrain region plus objects"""
	# ~ #

	            #  0123
	terraindict = " ,.;";
	width = 16;
	height = 16;
	
	#Scale map attributes; should be separated into another class but cbf
	scale = [[]];
	scaleupdate = lambda s, x, y: None;

	def __init__ (self, tile = 0):
		# Terrain
		blank = [];
		self.terrain = [];
		for el in range(area.width):
			blank.append(tile);
		for row in range(area.height):
			self.terrain.append(blank);
		self.symbol = area.terraindict[tile];
		
		# Objects
		self.access = {};
	def fulldisplay(self):
		out = [];
		y = 0;
		for row in self.terrain:
			x = 0;
			curr = "";
			for el in row:
				char = "";
				if (x,y) in self.access: # is there anything at this location?
					char = obj_base.bestof(self.access[(x, y)]); # Yes? find the most relevant one.
				# No? just leave an empty string.
				if char == "": # Do I have an object more important than the terrain?
					char = area.terraindict[el]; # No? Just get the terrain to display then.
				curr += char;
				x += 1;
			out.append(curr);
			y += 1;
		return out;

	def rowdisplay(self, row):
		curr = "";
		for el in self.terrain[row]:
			curr += area.terraindict[el];
		return curr;

	def randomise(self, options):
		for row in range(area.height):
			line = [];
			for el in range(area.width):
				line.append(random.choice(options));
			self.terrain[row] = line;
		self.symbol = random.choice(options);
	# ~ #
	def randomise(options): #For initial generation, when blank areas are useless.
		self = area();
		for row in range(area.height):
			line = [];
			for el in range(area.width):
				line.append(random.choice(options));
			self.terrain[row] = line;
		self.symbol = random.choice(options);
		return self;
	# ~ #

	def addobject(self, object, coord):
		if coord in self.access:
			self.access[coord].append(object);
		else:
			self.access[coord] = [object];

	def moveobject(self, object, cofrom, coto):
		if cofrom in self.access:
			n = 0;
			for i in self.access[cofrom]:
				if i is object:
					del self.access[cofrom][n];
					self.addobject(object, coto);
					return True;
				n += 1;
		return False;
	# ~ #
	def removeobject(self, object, coord):
		self.access[coord].remove(object);
# ~ #


