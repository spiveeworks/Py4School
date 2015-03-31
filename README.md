# Py4School
https://spiveeworks.wordpress.com/2015/02/09/new-blog-not-really/

This is the Git repo for my python project: "Extradite".

It is now finished ready for school.

Commands:

look
    lists all objects sitting on the terrain nearby.
    Names listed here are used by other commands, however enemies' levels/death state are not used in commands.
  e.g.
>look
Under yourself, you find:
    axe
and elsewhere:
    Nymph lv. 4
>attack nymph
Conquered the nymph
>look
Under yourself, you find:
    Nymph (dead)
and elsewhere:
    axe



move
    Moves to a random cell in the region.
    This command is not needed as other commands automatically move you to your target.
move [to <objectname>]
    Moves on top of a specific object.

    
    
collect <objectname>
    Picks up an item on the ground. Only works on item based objects.

    
    
attack <creaturename>
    Initiates a battle with one creature.
    Either you or the creature will die as a result.
    
    
    
loot <creaturename>
    Removes a dead creature, adding its weapon and potion to your inventory.
    
    
    
travel [north | south | east | west]
    Moves to a different region within the world map.
    Regions are saved, so you can come back to any place at any time.



view
    Lists items in your inventory.
    Any items above level 0 will also have their level listed.
    This is usually the level of the enemy whence they were looted.

    
    
drink <item name>
    Drinks a potion in your inventory.
    e.g. >drink health pot
    
    
    
equip
    Overwrites your weapon using one from inventory.
    Your old weapon is lost, but you couldn't have sold it anyway.
    
    
drop
    Places an item on the ground at your feet.
    The item can be picked up later, but there is no inventory limit so you probably don't need to.
    
    
    
exit
    Humanely terminates the program.
    

