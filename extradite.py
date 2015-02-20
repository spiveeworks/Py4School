import random

from mapobject import *
from maparea import *

class item:
	symbols = { # Each key refers to the itemtype, and each value is a string in which characters refer to symbols of itemvariants of that index.
		0 : "*",
		1 : "/", 
		2 : "!" 
	};
	def __init__ (self, itemdata):
		self.itemtype = 0;
		self.itemlevel = 0;
		self.itemvariant = 0;
		self.itemtype, self.itemlevel, self.itemvariant = itemdata;
		if len(item.symbols[self.itemtype]) >= self.itemvariant:
			self.itemvariant = 0; # may need a try-except-keyerror to add extra security in the future.
	def makeobj (self):
		return obj_item(item.symbols[self.itemtype][self.itemvariant], self);
# ~ #






def randcoord ():
	return (random.randrange(area.width), random.randrange(area.height));
# ~ #


class character:
	class wrapobject:
		def __init__ (self, obj, loc):
			self.obj = obj;
			self.loc = loc;
		def data(self):
			return (self.obj, self.loc);
	def __init__ (self, region, charobj, charloc):
		self.objset = {0 : character.wrapobject(charobj, charloc)};
		self.setfocus(region, charloc);
	def remove(self, id):
		obj, coord = self.objset[id].data();
		areain.removeobject (obj, coord);
		del self.objset[id];
		return obj;
	def setfocus(self, region, newloc):
		if region not in map:
			map[region] = area.randomise(options = [1,2]);
		self.region = region;
		self.area = map[region];
		self.objnum = 1;
		self.objset = {0 : self.objset[0]};
		i = 1;
		for loc, obj in self.area.access.items():
			self.objset[i] = character.wrapobject(obj, loc);
			i += 1;
		self.area.addobject(*self.objset[0].data());
		return self.area;
	def changefocus(self, **kwargs):
		self.area.removeobject(*self.objset[0].data());
		return self.setfocus(**kwargs);
	
	def move(self, newloc, subject = 0):
		self.area.moveobject(*self.objset[0].data(), coto = newloc);
		self.objset[subject].loc = newloc;
# ~ #

def getvect(words):
	if words[0] == "north":
		return (0, -1);
	elif words[0] == "south":
		return (0, +1);
	elif words[0] == "east":
		return (+1, 0);
	elif words[0] == "west":
		return (-1, 0);
	return (0, 0);
# ~ #

def sumvect(left, right):
	xl, yl = left;
	xr, yr = right;
	return (xl + xr, yl + yr);

map = {};

player = character(region = (0,0), charobj = obj_body(symbol = 1), charloc = randcoord());
player.area.addobject (object = item((0, 0, 0)).makeobj(), coord = randcoord());

def printregion ():
	out = player.area.fulldisplay();
	for i in out:
		print (i);
# ~ #

printregion ();

while True:
	inline = "";
	while inline == "":
		inline = input("> ");
	parse = inline.split();
	try:
		if parse[0] == "move":
			newco = randcoord();
			player.move(newco);
			charloc = newco;
		elif parse[0] == "travel":
			del parse[0];
			newreg = sumvect(left = player.region, right = getvect(parse));
			player.changefocus(region = newreg, newloc = randcoord());
		elif parse[0] == "spawn":
			del parse[0];
			player.area.addobject(item((0, 0, 0)).makeobj(), randcoord());
		elif parse[0] == "exit":
			break;
	except IndexError:
		pass;
	
	printregion();
# ~ #

