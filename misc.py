from maparea import *


def dobattle (self, target): 
	wname1 = self.weapon;
	wname2 = target.weapon;
	time = 0;
	next1 = time + wname1.Atime;
	next2 = time + wname2.Atime;
	while (not self.isdead) and (not target.isdead):
		if next1 < next2:
			self.attack(target);
			next1 += wname1.Atime;
		else:
			target.attack(self);
			next2 += wname2.Atime;
"""  
Slight slight bias towards the first argument in a battle... 
	only if they are effectively equal in power will they win. 
	They will also receive no damage if they manage to instakill when attackspeeds are equal.
"""
# ~ #  BATTLE DONE.




def drawmap (map, Cx, Cy, wid, hei): #  Where map[Cx, Cy] refers to the area in the toppest leftest corner.
	BCx = Cx + wid;
	BCy = Cy + hei;
	display = [];
	for y in range(Cy, BCy):
		row = [];
		for x in range(Cx, BCx):
			if (x, y) in map: 
				row.append(map[x, y].symbol); 
			else: 
				row.append(0);
		display.append(row);
	return display;

#  drawmap (map, -9, -9, 21, 21); # gives a base map upon which things like goal or @ can be added

def assemblemap(overlay, display, Cx, Cy):
	ret = [];
	yI = Cy;
	
	for row in display:
		line = "";
		xI = Cx;
		for el in row:
			if (xI, yI) in overlay:
				line += overlay[xI, yI][-1:];
			else:
				line += area.terraindict[ display[yI-Cx][xI-Cy] ];
			xI += 1;
		ret.append(line);
		yI += 1;
	return ret;
#~#

def updatemap(display, Cx, Cy, symbol, xI, yI):
	
	widths = map(len, display);
	width = max(widths);
	height = len(display);
	
	if xI < Cx or yI < Cy or xI >= Cx + width or yI >= Cy + height:
		return None;
	display[yI-Cx][xI-Cx] = symbol;

	

"""
map(func, argset1, argset2...)

xs = [0, 1, 2, 3];
ys = [0, 2, 4, 6];
def add(x, y):
	return x + y;

print (map (add, xs, ys););
	#	[0, 3, 6, 9]

"""