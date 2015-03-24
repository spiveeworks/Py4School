import random;

from mapobject import *;
from maparea import *;
import misc;

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
		self.markers = {};
		self.setfocus(region, charloc);
	def remove(self, id):
		obj, coord = self.objset[id].data();
		areain.removeobject (obj, coord);
		del self.objset[id];
		return obj;
	def setfocus(self, region, newloc): 
		"""\
			DO NOT USE THIS FUNCTION. USE character.changefocus(self, region, newloc) INSTEAD.
		"""
		if region not in map:
			toad = area.randomise(options = [1,2]);
			area.scaleupdate(toad.symbol, *region);
			map[region] = toad;
		if region in self.markers:
			self.markers[region] += '@';
		else:
			self.markers[region] = "@";
		self.region = region;
		self.area = map[region];
		self.objnum = 1;
		self.objset = {0 : self.objset[0]};
		i = 1;
		for loc, content in self.area.access.items():
			for obj in content:
				self.objset[i] = character.wrapobject(obj, loc);
				i += 1;
		self.area.addobject(*self.objset[0].data());
		return self.area;
	def changefocus(self, *args, **kwargs):
		self.area.removeobject(*self.objset[0].data());
		newmarks = "";
		for i in self.markers[self.region]:
			if i != '@':
				newmarks += i;
		if newmarks == "":
			del self.markers[self.region];
		else:
			self.markers[self.region] = newmarks;
		return self.setfocus(*args, **kwargs);
	
	def move(self, newloc, subject = 0):
		self.area.moveobject(*self.objset[0].data(), coto = newloc);
		self.objset[subject].loc = newloc;
# ~ #

def getvect(words):
	arg = words.pop();
	if arg == "north":
		return (0, -1);
	elif arg == "south":
		return (0, +1);
	elif arg == "east":
		return (+1, 0);
	elif arg == "west":
		return (-1, 0);
	print ("Enter a travel direction: north, south, east or west.");
	return (0, 0);
# ~ #

def sumvect(left, right):
	xl, yl = left;
	xr, yr = right;
	return (xl + xr, yl + yr);

map = {};

player = character(region = (0,0), charobj = obj_body(symbol = 1), charloc = randcoord());
player.area.addobject (object = item((0, 0, 0)).makeobj(), coord = randcoord());

area.scale = misc.drawmap(map, -7, -7, 15, 15);
area.scaleupdate = lambda s, x, y: misc.updatemap(area.scale, -7, -7, s, x, y);

def printregion ():
	newscale = misc.assemblemap(player.markers, area.scale, -7, -7);
	for i in newscale:
		print(i);
	out = player.area.fulldisplay();
	for i in out:
		print (i);
# ~ #

class command:
	def move(words):
		newco = randcoord();
		player.move(newco);

	def travel(words):
		newreg = sumvect(left = player.region, right = getvect(words));
		player.changefocus(region = newreg, newloc = randcoord());

	def spawn(words):
		player.area.addobject(item((0, 0, 0)).makeobj(), randcoord());
	
	def debug(words):
		print(player.markers);
		print ("SCALE MAP:")
		for i in area.scale:
			print(i);
command_set = { "move" : command.move, "travel" : command.travel, "spawn" : command.spawn, "debug" : command.debug };
# ~ #

while True:
	printregion();
	inline = "";
	parse = [""];
	while inline == "":
		inline = input("> ");
	parse = inline.split();
	parse.reverse();
	bit = parse.pop();
	if bit == "exit":
		break;
	elif bit in command_set:
		command_set[bit](parse);
	else:
		print ("Try again. \n");
# ~ #

