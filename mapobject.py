import random;

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
    def symbol (self):
        return item.symbols[self.itemtype][self.itemvariant];
    def describe (self):
        if self.itemlevel == 0:
            return self.name;
        else:
            return (self.name + " (Lv. " + str(self.itemlevel) + ")");
# ~ #

class weapon_item (item):
    def __init__ (self, name, itemtype = 0, itemvariant = 0, itemlevel = 0, Atime = 3.0, dmg = 1):
        item.__init__(self, name, itemtype, itemvariant, itemlevel);
        self.Atime = Atime;
        self.dmg = dmg;
# ~ #

class potion_item (item):
    def __init__ (self, name, itemtype = 0, itemvariant = 0, itemlevel = 0, healthup = 0, fistbuff = 0, xpbonus = 0):
        item.__init__(self, name, itemtype, itemvariant, itemlevel);
        self.H = healthup;
        self.S = fistbuff;
        self.X = xpbonus;
    def attr():
        return (H, S, X);


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
    def describe (self):
        return "Generic Object";
    def ref (self):
        return self.describe();
#
class obj_terrent (obj_base):
    def __init__ (self, symbol):
        obj_base.__init__(self, symbol);
    def passable ():
        return False;
    def describe (self):
        "Obstacle";
#
class obj_item (obj_base):
    def __init__ (self, it):
        obj_base.__init__(self, it.symbol());
        self.item = it;
    def describe (self):
        return self.item.name;
#

class obj_body (obj_base):
    def __init__ (self, name = "@character", level = 15, defweapon = None):
        obj_base.__init__(self, name[0]);
        self.name = name;
        
        self.health =  2*level + 3;
        self.maxhealth = 2*level + 3;
        self.iskilled = False;
        
        self.level = level;
        self.xp = 0;
        
        self.maininv = [];
        if defweapon == None:
            self.defweapon = weapon_item("Fist");
        else:
            self.defweapon = defweapon;
        self.weapon = self.defweapon;
        
    def additem (self, toad):
        self.maininv.append(toad);
    def skillup (self, lvlkilled):
        lvup = 0;
        rat = (lvlkilled + 1)/self.level;
        self.xp += int(rat);
        rat -= int(rat);
        if random.uniform(0.0, 1.0) <= rat:
            self.xp += 1;
    def describe (self):
        if self.iskilled:
            return self.name + " (DEAD)"
        else:
            return self.name + " lv. " + str(self.level);
    def ref (self):
        return self.name;
    def attack (self, target):
        target.health -= self.weapon.dmg;
        if target.health <= 0:
            target.iskilled = True;
            target.symbol = "X";
            self.skillup(target.level);
    def drink (self, pot):
        self.health += pot.H;
        self.defweapon.dmg += pot.S;
        self.xp += pot.X;
        self.clean()
    def clean(self):
        lvup = self.xp // 4;
        self.xp %= 4;
        self.level += lvup;
        self.maxhealth += 2*lvup;
        if self.health >= self.maxhealth:
            self.health = self.maxhealth;
        
# ~ #
