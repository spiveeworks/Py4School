import random;

from mapobject import *;
from maparea import *;
import misc;

class item:
	symbols = { # Each key refers to the itemtype, and each value is a string in which character.trackers refer to symbols of itemvariants of that index.
		0 : "*",
		1 : "/", 
		2 : "!" 
	};
	def __init__ (self, name, itemtype = 0, itemvariant = 0, itemlevel = 0):
		self.itemtype = itemtype;
		self.itemvariant = itemvariant;
		self.itemlevel = itemlevel;
		self.name = name;
		if len(item.symbols[self.itemtype]) >= self.itemvariant:
			self.itemvariant = 0; # may need a try-except-keyerror to add extra security in the future.
	def makeobj (self):
		return obj_item(item.symbols[self.itemtype][self.itemvariant], self);
	def describe (self):
		if self.itemlevel == 0:
			return self.name;
		else:
			return (self.name + " (Lv. " + str(self.itemlevel) + ")");
# ~ #






def randcoord ():
	return (random.randrange(area.width), random.randrange(area.height));
# ~ #


class character:
	def __init__(self, region = (0, 0), chararg = (1,), locarg = None):
		if isinstance(chararg, tuple):
			charobj = obj_body(*chararg);
		else:
			charobj = chararg;
		if locarg is None:
			charloc = randcoord();
		else:
			charloc = locarg;
		self.scope = character.tracker(region, charobj, charloc);
		self.body = charobj;
	class wrapobject:
		def __init__ (self, obj, loc):
			self.obj = obj;
			self.loc = loc;
		def data(self):
			return (self.obj, self.loc);
	class tracker:
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
				DO NOT USE THIS FUNCTION. USE character.tracker.changefocus(self, region, newloc) INSTEAD.
			"""
			if region not in world:
				toad = area.randomise(options = [1,2]);
				area.scaleupdate(toad.symbol, *region);
				world[region] = toad;
			if region in self.markers:
				self.markers[region] += '@';
			else:
				self.markers[region] = "@";
			self.region = region;
			self.area = world[region];
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
		
		def addobject(self, object, coord):
			next = 0;
			while next in self.objset:
				next += 1;
			self.objset[next] = character.wrapobject(object, coord);
			self.area.addobject(object, coord);
			return next;
		def removeobject(self, id):
			data = self.objset[id].data();
			self.area.removeobject(*data);
			return(data[0]);
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
	global error;
	error = "Enter a travel direction: north, south, east or west.";
	return (0, 0);
# ~ #

def sumvect(left, right):
	xl, yl = left;
	xr, yr = right;
	return (xl + xr, yl + yr);

#  BEGIN init
world = {}; #  Maps (x, y) tuples as keys to maparea.area objects as values, meaning unexplored areas do not take up any memory.

player = character(); #  all default arguments are used for the start of the game.
area.scale = misc.drawmap(world, -7, -7, 15, 15);  # start with a world drawn 7 cells out from the centre in all directions
area.scaleupdate = lambda s, x, y: misc.updatemap(area.scale, -7, -7, s, x, y);  # create a lambda function that calls a more complicated function, but with some default arguments.

text = ["","","","","","","",""]; #  eight empty lines
error = "" #  nothing has gone wrong yet!
#  END

def display(line):
	text.extend(line.split("\n"));
	del text[:-8];


def printregion ():
	newscale = misc.assemblemap(player.scope.markers, area.scale, -7, -7);
	print("World: ");
	for i in newscale:
		print(i);
	out = player.scope.area.fulldisplay();
	print("\nRegion: ");
	for i in out:
		print (i);
	print("\nHistory: ");
	for i in text:
		print (i);
	print(error);
# ~ #

def unsplit(seq):
	out = seq.pop();
	while len(seq) > 0:
		out += ' ' + seq.pop();
	return out;

class command:
	def getobj(test):
		unformatted = player.scope.objset.items()               # retrieve objects in the form of [(numkey, wrapper)...]
		formatted = map(lambda tup: tup[1].data(), unformatted);    # format wrapper into (object, (x, y)) and then assemble [(object, (x, y))...]
		filtered = filter(lambda data: test(*data), formatted);       # filter out any objects that don't pass the test()
		discrete = list(filtered);								# turn an iterable filter object into a list, since random.choice() needs a length.
		try:	# try rather than an external check, because an internal check is what throws the error, so why not use that
			return random.choice(discrete);                     # -> try returning an object at random
		except(IndexError):
			return None;                                        # -> no objects left to pass the test, so pass a None.
	def getobjid(test):
		items = player.scope.objset.items();
		filtered = filter(lambda tup: test(*tup[1].data()), items); # This time keep the id around because we want it later... so don't world at all, and call data() at the same time as the filter
		discrete = list(filtered);
		try:
			return random.choice(discrete)[0];                  # -> as before, but strip off the actual object details... which must be determined externally. leave only the index within the scope.
		except(IndexError):
			return None;


	def move(words):
		newco = (None);  # initialise with a unique value that wouldn't occur otherwise
		if len(words) == 0:  # -> no directions, choose randomly
			newco = randcoord(); # set for later
			display("Moved nowhere in particular");
		elif words.pop() == "to":  # user wants to specify a destination
			word = unsplit(words);
			goto = command.getobj(lambda obj, loc: obj.describe().lower() == word.lower());
			if goto is None:
				return("Need to specify an object in the current region.");
			newco = goto[1];
			display("Moved to a " + word);
		else:
			return("Need to specify an object in the current region, using 'to' keyword.");
		player.scope.move(newco);
		return "";
	def collect(words):
		word = unsplit(words);
		get = command.getobjid(lambda obj, loc: isinstance(obj, obj_item) and obj.describe().lower() == word.lower());
		if get == None:
			return("Need to specify an object in the current region.");
		player.scope.move(player.scope.objset[get].loc);
		obj = player.scope.removeobject(get);
		player.body.maininv.append(obj);
		display ("Collected a " + word);
		return "";
	def travel(words):
		delta = getvect(words);
		if delta == (0, 0):
			return error;
		player.scope.changefocus(region = sumvect(player.scope.region, delta), newloc = randcoord());
		display("Travelled");
		return "";
	def spawn(words):
		player.scope.addobject(item("Generic").makeobj(), randcoord());
		return "";
	def debug(words):
		print(player.scope.markers);
		print ("SCALE MAP:")
		for i in area.scale:
			print(i);
	def look(words):
		under = [];
		around = [];
		coord = player.scope.objset[0].loc;
		for num, objwrap in player.scope.objset.items():
			if num != 0:
				if objwrap.loc == coord:
					under.append(objwrap.obj.describe());
				else:
					around.append(objwrap.obj.describe());
		print("Under yourself, you find: ");
		for i in under:
			print("    ", i);
		print("\nand elsewhere: ");
		for i in around:
			print ("    ", i);
		input("\nEnter to Continue . . . ");
		return "";
	def viewinv(words):
		print("You possess the following: ");
		for i in player.body.maininv:
			print("    ", i.describe());
		input("\nEnter to Continue . . . ");
		return "";
command_set = { "move" : command.move, "collect": command.collect, "travel" : command.travel, "spawn" : command.spawn, "look": command.look, "view": command.viewinv, "debug" : command.debug };
# abreviation_set = {"T" : "travel"};
# ~ #

while True:
	inline = "";
	while inline == "":
		printregion();
		inline = input("> ");
	parse = inline.split();
	parse.reverse();
	bit = parse.pop();
	if bit == "exit":
		break;
	elif bit in command_set:
		error = command_set[bit](parse);
	else:
		error = "Try again."
# ~ #

