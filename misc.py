from maparea import *;
import random;


def dobattle (self, target): 
    wname1 = self.weapon;
    wname2 = target.weapon;
    time = 0;
    next1 = time + wname1.Atime;
    next2 = time + wname2.Atime;
    while (not self.iskilled) and (not target.iskilled):
        if next1 < next2:
            self.attack(target);
            next1 += wname1.Atime;
        else:
            target.attack(self);
            next2 += wname2.Atime;
    return target.iskilled;
"""  
Slight slight bias towards the first argument in a battle... 
    only if they are effectively equal in power will they win. 
    They will also receive no damage if they manage to instakill when attackspeeds are equal.
"""
# ~ #  BATTLE DONE.




def drawmap (world, Cx, Cy, wid, hei): #  Where world[Cx, Cy] refers to the area in the toppest leftest corner.
    BCx = Cx + wid;
    BCy = Cy + hei;
    display = [];
    for y in range(Cy, BCy):
        row = [];
        for x in range(Cx, BCx):
            if (x, y) in world: 
                row.append(world[x, y].symbol); 
            else: 
                row.append(0);
        display.append(row);
    return display;

#  drawmap (map, -9, -9, 21, 21); # gives a base world upon which things like goal or @ can be added

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





enchoice = ["Nymph"]
weppresets = [
    {'name' : "Axe", 
        'itemtype' : 1, 
        'itemvariant' : 0, 
        'Atime' : 3.0,
        'Dmult' : 5,
    },
    {'name' : "Screw Driver",
        'itemtype': 1,
        'itemvariant' : 0,
        'Atime' : 0.4,
        'Dmult' : 1,
    },
    ]

potpresets = [
    {'name' : "Health Pot",
        'itemtype' : 2,
        'itemvariant' : 0,
        'healthup' : 20,
    },
    {'name' : "Skill Pot",
        'itemtype' : 2,
        'itemvariant' : 0,
        'xpbonus' : 12,
    },
    {'name' : "Pot of Edge",
        'itemtype' : 2,
        'itemvariant' : 0,
        'xpbonus' : 4,
        'healthup' : 5,
    },
    ]
    
def getweapon (level):
    wep = random.choice(weppresets).copy();
    wep['dmg'] = wep.pop('Dmult') * level;
    wep['itemlevel'] = level;
    return (weapon_item(**wep));
def getpotion ():
    pot = random.choice(potpresets);
    return (potion_item(**pot));
    
def makeenlist (region):
    ret = [];
    num = random.randrange(1,6);
    lvl = sum(map(abs, region)) // num;
    en = random.choice(enchoice);
    for i in range(num):
        toad = obj_body(en, lvl);
        toad.weapon = getweapon(lvl+1);
        toad.maininv.append(getpotion());
        ret.append(toad);
    return ret;
    
# ~ #

















