from random import randint
from random import choice
from ast import literal_eval
import math

#Figure out how to build a list of separate units which can be called on independently. <---------#WORK IN PROGRESS; FUNCTIONAL BUT INCOMPLETE
    #Should starting_set() give baseline troops only, all randomized prefixes, or just a chance to get a prefix per troop?
#Flavour up the events, why not. Do something for the tyranny too, don't leave them out.
#Speaking of Tyranny events, fix the Necropolitan-specific events in the Tyranny event tables.
#Dress up the [EARN] system too, while you're at it.
#Implement a loot selling mechanic/Think of ways to utilise loot in general.
    #Deathdreg Ruiners can now be produced through buytroops() if the player's faction is The Necropolis and they possess at least one each of the three deathdreg relics.
#Maybe rework the project so the only way to earn points is through scavenging; set a lose condition when you have no troops and not enough points to buy more.
#Try finding a way to adjust outcomes based on which unit is dispatched.
#Implement a hit chance and damage adjustment mechanic into the battle module.
#Eventually find a way to unify the scav and battle modules, or at least mix/match certain features of them.

#Note: Any function or whatever which is listed as "Complete" is still subject to heavy revision further down the line. It just means they work as intended for the current overall iteration of the game.

run = True    #Initialises the game loop.

initial = True    #Defines whether the game loop is initialised - set to False to proceed past initialisation.

set_chosen = False

action_choice = ""    #Defined via input() to process the user's chosen command.

points = 100    #Keeps a tally of the user's current points.

light_units = 0    #Keeps a tally of the user's chosen faction's light units.

lightunitlist = []

mid_units = 0    #Keeps a tally of the user's chosen faction's medium units.

midunitlist = []

heavy_units = 0    #Keeps a tally of the user's chosen faction's heavy units.

heavyunitlist = []

dd_units = 0    #Keeps a tally of the user's deathdreg revenant units (only used if faction == Necropolis).

ddunitlist = []

unitlist = []    #Still working on integrating this. No purpose yet.

inventory = []    #Tracks the user's inventory of loot.

class Troop:    #Represents a single troop unit. Functional, but parameters need expansion to add depth to battle().

  #Unit loot tables. Format: [n/t][l/m/h/d]loot // n=necropolis t=tyranny // l=light, m=mid, h=heavy, d=deathdreg
  nlloot = {0:"Pile of Ancient Bones", 1:"Rusted Sword", 2:"Ruined Rifle"}    #legionnaire loot
  tlloot = {0:"Dogtag", 1:"Petrov Machete", 2:"Garrison Cap", 3:"Tyranny SMG"}    #petrov loot
  nmloot = {0:"Scrap of Spectral Cloth", 1:"Lock of Wet Hair", 2:"Bone Talisman", 3:"Beloved Memento"}    #vengeful dead loot
  tmloot = {0:"Tyranny Assault Rifle", 1:"Scrap Circuitry", 2:"Scrap of Damaged Ballistic Weave", 3:"Officer's Cap"}    #commando loot
  nhloot = {0:"Slab of Twitching Flesh", 1:"Vial of Promethid Blood", 2:"Pile of Fused Bones", 3:"Writhing Suture", 4:"Promethid Skull"}    #promethid loot
  thloot = {0:"Force Actuator", 1:"Ceramic Alloy Plate", 2:"Vial of Combat Stimulants", 3:"Siegebreaker Gauntlet", 4:"Bunch of High-Performance Cable"}    #siegebreaker loot
  ndloot = {0:"Deathdreg Nexus", 1:"Cursed Blade", 2:"Ruiner's Eye"}    #deathdreg loot
 

  def __init__(self, fct, cls, typ, atk, dfn, agl, spcl=0): #Example: Troop(0,1,1,6,5,3,7) - Caustic Tyranny Commando - is a (0)Tyranny (1)medium-class (1)Commando with an attack stat of (6), a defense stat of (5) and an agility stat of (3) with the prefix (7)Caustic.  
    self.fct = fct    #Designates the instanced troop faction -- 0=Tyranny, 1=Necropolis
    self.cls = cls    #Designates the instanced troop class -- 0=light, 1=mid, 2=heavy, 3=deathdreg
    self.typ = typ    #Designates the instanced troop type -- 0-6, see var troop_type below
    self.atk = atk    #Designates the instanced troop's base attack stat.
    self.dfn = dfn    #Designates the instanced troop's base defense stat.
    self.agl = agl    #Designates the instanced troop's base agility stat.
    self.spcl = spcl #Designates the instanced troop's special variation (optional, default = basic)
    
  faction_keys = ["Tyranny", "Necropolitan"]    #List for assigning a faction to the instanced troop via [fct].
  troop_type = ["Petrov", "Commando", "Siegebreaker", "Legionnaire", "Vengeful", "Promethid", "Deathdreg Ruiner"]    #List for assigning a type to the instanced troop via [typ].
  
  def stats(self):    #Method for printing the instanced troop's faction, type, and attack and defense ratings.
    if self.typ in range(0,6):    #Specifies stats for troops with type 0-5 (light, mid and heavy units).
      return "%s %s with attack rating %s and defence rating %s." % (Troop.faction_keys[self.fct],Troop.troop_type[self.typ],self.atk,self.dfn)
    elif self.typ == 6:    #Specifies stats for troops with type 6 (deathdreg units).
      return "Necropolitan Deathdreg Ruiner with attack rating %s and defence rating %s." % (self.atk, self.dfn)
  
  def loots(self):    #Method for assigning loot drops from defeated enemies in battle().
    if self.typ == 0:
      return choice(Troop.tlloot)
    elif self.typ == 1:
      return choice(Troop.tmloot)
    elif self.typ == 2:
      return choice(Troop.thloot)
    elif self.typ == 3:
      return choice(Troop.nlloot)
    elif self.typ == 4:
      return choice(Troop.nmloot)
    elif self.typ == 5:
      return choice(Troop.nhloot)
    elif self.typ == 6:
      return choice(Troop.ndloot)
    
  def name(self):    #Method for printing the unit type.
    return "%s" % Troop.troop_type[self.typ]
  
  def hp(self):    #Method for calculating troop HP.
    return self.dfn * 120
  
  def dmg(self):    #Method for calculating troop attack damage.
    return self.atk * 40
    
  def acc(self):
    return int(self.agl * self.atk)
    
  def evade(self):    #Method for calculating troop evasion chance (Still WIP).
    return int(self.agl * self.dfn)
  
  def special(self):
    if self.spcl == 0:
      return ""
    elif self.spcl == 1:
      return "Frenzied "
    elif self.spcl == 2:
      return "Stalwart "
    elif self.spcl == 3:
      return "Ruthless "
    elif self.spcl == 4:
      return "Keen "
    elif self.spcl == 5:
      return "Decrepit "
    elif self.spcl == 6:
      return "Incandescent "
    elif self.spcl == 7:
      return "Caustic "
    elif self.spcl == 8:
      return "Opportunistic "
    elif self.spcl == 9:
      return "Swift "

necro_unit_names = ["legionnaire", "vengeful", "promethid"]    #Establishes the list of available Necropolitan units, referenced in [scav()].

tyr_unit_names = ["petrov", "commando", "siegebreaker"]    #Establishes th list of available Tyranny units, referenced in [scav()].

unit_names = ["legionnaire", "vengeful", "promethid", "deathdreg", "petrov", "commando", "siegebreaker"]    #Not referenced anywhere, kept in place in case it's needed.

"""points references: light unit = 2pts, medium unit = 5pts, heavy unit = 10pts"""

def round_down(n, decimals=0): #Rounds any floating point down to the closest integer. Employed only in [buytroops()].
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

def round_up(n, decimals=0):    #Rounds any floating point up to the closest integer. Employed only in [scav()].
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

faction = ""    #Holds the string value for the user's faction.

faction_chosen = False    #Designates whether the faction has been chosen. Game loop won't progress until faction_chosen == True.

def starting_set():
  global light_units
  global mid_units
  global heavy_units
  global start_set
  global set_chosen
  

  deathdreg = Troop(1,3,6,(randint(1,10)),randint(1,10),randint(1,5),randint(0,9))

  
  
  print("Choose a starting unit set:")
  print("[SKIRMISHER]: 10 light units / 5 medium units / 1 heavy unit")
  print("[ASSAULT]: 5 light units / 10 medium units / 1 heavy unit")
  print("[SIEGE]: 5 light units / 5 medium units / 6 heavy units")
  while set_chosen == False:
    start_set = input(" >").upper()
    if start_set.lower() == "skirmisher":
      light_units = 10
      mid_units = 5
      heavy_units = 1
      set_chosen = True
    elif start_set.lower() == "assault":
      light_units = 5
      mid_units = 10
      heavy_units = 1
      set_chosen = True
    elif start_set.lower() == "siege":
      light_units = 5
      mid_units = 5
      heavy_units = 6
      set_chosen = True
    else:
      print("Invalid starting set.")
      
      
  for i in range(1,(light_units+1)):
    if faction == "TYRANNY":
      lightunitlist.append(Troop(0,0,0,3,2,5,randint(0,9)))
    else:
      lightunitlist.append(Troop(1,0,3,3,2,5,randint(0,9)))
  for i in range(1,(mid_units+1)):
    if faction == "TYRANNY":
      midunitlist.append(Troop(0,1,1,6,5,3,randint(0,9)))
    else:
      midunitlist.append(Troop(1,1,4,6,5,3,randint(0,9)))
  for i in range(1,(heavy_units+1)):
    if faction == "TYRANNY":
      heavyunitlist.append(Troop(0,2,2,10,7,1,randint(0,9)))
    else:
      heavyunitlist.append(Troop(1,2,5,10,7,1,randint(0,9)))

def faction_choice():    #Establishes the faction select at the beginning of the game and whenever faction_select() is called.
  global faction
  global faction_chosen

  faction_choice = input("Choose your faction (TYRANNY or NECROPOLIS): ")
  print("")
  if faction_choice.lower() == "tyranny":
    faction = "TYRANNY"
    print("You have chosen The Tyranny.")
    print("")
    faction_chosen = True

  elif faction_choice.lower() == "necropolis":
    faction = "NECROPOLIS"
    print("You have chosen The Necropolis.\n ")
    print("")
    faction_chosen = True

  else:
    print("Invalid faction.")
    print("")

  return(faction_chosen)
  return(faction)

def action_list():    #Defunct.
  global points
  global faction
  global faction_chosen
  global initial
  global light_units
  global mid_units
  global heavy_units
  global dd_units
  global unitlist

#[EARN] points
#[BUY] units
#[SHOW] points
#show [UNITS] in reserve
#change [FACTION]
#[DISPATCH] units to procure resources
#[QUIT] game
  


  action_choice = input(" >")
  
  if action_choice.lower() == "class":
    print(unitlist)

def faction_select():    #Allows the user to reset all progress and re-select their faction.
  
  global points
  global faction_chosen
  global initial
  global light_units
  global mid_units
  global heavy_units
  global dd_units
  global inventory
  global set_chosen
  
  print("You are currently aligned with THE %s." % faction)
  faction_switch = input("Are you sure you want to change? All currently held points and units will be lost. [YES/NO] ")
  print("")

  if faction_switch.lower() == "yes":    #Resets all game progress to initial state.
    faction_chosen = False
    initial = True
    set_chosen = False
    light_units = 0
    mid_units = 0
    heavy_units = 0
    dd_units = 0
    points = 0
    inventory = []

def help():    #Displays a complete list of user-ready commands.
  print("Available actions: \n#[EARN] points \n#[BUY] units \n#show [POINTS] \n#show [UNITS] in reserve \n#change [FACTION] \n#[DISPATCH] units to procure resources \n#[BATTLE] enemy units \n#Display [INVENTORY] \n#[INSPECT] inventory items \n#[SAVE] faction, troops & points \n#[LOAD] saved data \n#[QUIT] game")
  print("")

"""def earn(): #Old version of earn() which grants a random number of points with a 1/10 chance of getting a double bonus.

  global points

  gen = randint(1,10)
  bonus = randint(1, 10)
  points += gen
  if bonus == gen:
    points += bonus
    print("Resource trove uncovered!")
    print("%d points earned, plus %d bonus points." % (gen, bonus))
    print("")
  else:
    print("%d points earned." % gen)
    print("")
    return points"""
    
def earn():    #Grants 10 points. Placeholder function for generating points; will eventually implement a better-integrated means.

  global points

  points += 10
  print("10 points earned.")
  print("")
  return points

def showpoints():    #Displays the user's current points.

  global points

  print("You have %d available points." % points)
  print("")

def buytroops():    #Allows the user to purchase faction-specific units in user-specified quantities, as long as sufficient points are possessed.

  global points
  global faction
  global light_units
  global lightunitlist
  global mid_units
  global midunitlist
  global heavy_units
  global heavyunitlist
  global dd_units
  global ddunitlist
  global inventory

  #for i in range(1,(light_units+1)):
    #if faction == "TYRANNY":
    #else:
  #for i in range(1,(mid_units+1)):
    #if faction == "TYRANNY":
    #else:
  #for i in range(1,(heavy_units+1)):
    #if faction == "TYRANNY":
    #else:
  
  trooperlooper = True    #Governs whether the purchase menu loops. Remains true until a unit has been purchased or user chooses 0 as a number to buy.
  while trooperlooper == True:
    if faction.lower() == "tyranny": #Tyranny selected.
      type_choice = input("Choose a unit type to produce: [PETROV]: 2pts, [COMMANDO]: 5pts, [SIEGEBREAKER]: 10pts\n >")    #Sets the chosen unit type to the user-entered string.
      print("")
      
      try:    #Prevents the game from crashing if a non-numeric value is entered where one is required (in this command).
      
        if type_choice.lower() == "petrov":    #Branch for purchasing Petrov units (Tyranny, light).
        
          mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 2, 0)))    #Sets the amount of units the user wishes to purchase.
          print("")
          cost = (mult * 2)    #Defines the cost of the purchase by multiplying [mult] (the user's specified number of units to purchase) by the points cost of that unit.

          if cost > points:    #Prints the exception for trying to purchase more units than the user can afford, before looping back to the start.
            print("Insufficient points.")
            print("")

          else:
            points -= cost    #Subtracts the value of [cost] from [points].
            light_units += mult    #Adds the value of [mult] to [light_units].
            for i in range(1, mult+1):
              lightunitlist.append(Troop(0,0,0,3,2,5,randint(0,9)))
            print("Produced %d PETROV units." % mult)
            print("")
            trooperlooper = False    #Finalises the purchase and exits the loop.

        elif type_choice.lower() == "commando":    #Branch for purchasing Commando units (Tyranny, mid).
          mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 5, 0)))
          print("")
          cost = (mult * 5)

          if cost > points:
            print("Insufficient points.")
            print("")

          else:
            points -= cost
            mid_units += mult    #Adds the value of [mult] to [mid_units].
            for i in range(1, mult+1):
              midunitlist.append(Troop(0,1,1,6,5,3,randint(0,9)))
            print("Produced %d COMMANDO units." % mult)
            print("")
            trooperlooper = False

        elif type_choice.lower() == "siegebreaker":    #Branch for purchasing Siegebreaker units (Tyranny, mid).
          mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 10, 0)))
          print("")
          cost = (mult * 10)

          if cost > points:
            print("Insufficient points.")
            print("")

          else:
            points -= cost
            heavy_units += mult    #Adds the value of [mult] to [heavy_units]
            for i in range(1, mult+1):
              heavyunitlist.append(Troop(0,2,2,10,7,1,randint(0,9)))
            print("Produced %d SIEGEBREAKER units." % mult)
            print("")
            trooperlooper = False

        else:    #Prints the exception for an invalid unit type being entered, before looping to the start.
          print("Unit type not found.")
          print("")

      
      except:    #Prints the exception for a non-numeric value being entered where one is required, before looping to the start.
        print("Requires a numeric value.\n ")

    elif faction.lower() == "necropolis":
      ddkey = ["Deathdreg Nexus", "Ruiner's Eye", "Cursed Blade"]
      if all(item in inventory for item in ddkey):
        type_choice = input("Choose an undead type to raise: [LEGIONNAIRE]: 2pts \n[VENGEFUL]: 5pts \n[PROMETHID]: 10pts \n[DEATHDREG RUINER]: Cursed Blade + Deathdreg Nexus + Ruiner's Eye\n >")
      else:
        type_choice = input("Choose an undead type to raise: [LEGIONNAIRE]: 2pts \n[VENGEFUL]: 5pts \n[PROMETHID]: 10pts\n >")
      
      print("")

      try:
      
        if type_choice.lower() == "legionnaire":    #Branch for purchasing Legionnaire units (Necropolis, light).
          mult = int(input("Enter a number of undead to raise (max available = %d): \n >" % round_down(points / 2, 0)))
          print("")
          cost = (mult * 2)


          if cost > points:
            print("Insufficient points.")
            print("")

          else:
            points -= cost
            light_units += mult
            for i in range(1, mult+1):
              lightunitlist.append(Troop(1,0,3,3,2,5,randint(0,9)))
            print("Raised %d LEGIONNAIRE undead." % mult)
            print("")
            #unitlist.append(legionnaire)
            trooperlooper = False
            

        elif type_choice.lower() == "vengeful":    #Branch for purchasing Vengeful Dead units (Necropolis, mid).
          mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 5, 0)))
          print("")
          cost = (mult * 5)

          if cost > points:
            print("Insufficient points.")
            print("")

          else:
            points -= cost
            mid_units += mult
            for i in range(1, mult+1):
              midunitlist.append(Troop(1,1,4,6,5,3,randint(0,9)))
            print("Raised %d VENGEFUL DEAD." % mult)
            print("")
            trooperlooper = False

        elif type_choice.lower() == "promethid":    #Branch for purchasing Promethid units (Necropolis, heavy).
          mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 10, 0)))
          print("")
          cost = (mult * 10)

          if cost > points:
            print("Insufficient points.")
            print("")

          else:
            points -= cost
            heavy_units += mult
            for i in range(1, mult+1):
              heavyunitlist.append(Troop(1,2,5,10,7,1,randint(0,9)))
            for i in range(1, mult+1):
              heavyunitlist.append(Troop(1,2,5,10,7,1,randint(0,9)))
            print("Raised %d PROMETHID undead." % mult)
            print("")
            trooperlooper = False
            
        elif type_choice.lower() == "deathdreg ruiner":    #Branch for purchasing Deathdreg Ruiner units (Necropolis, special).
          if all(item in inventory for item in ddkey):
            matlist = []
            bladecount = inventory.count("Cursed Blade")
            eyecount = inventory.count("Ruiner's Eye")
            nexuscount = inventory.count("Deathdreg Nexus")
            matlist.extend([bladecount, eyecount, nexuscount])
            matlist.sort()
            mult = int(input("Enter a number of units to produce (max available = %d): \n >" % matlist[0]))
            print("")

            if mult > matlist[0]:
              print("Insufficient materials.")
              print("")

            else:
              counter = mult
              while counter > 0:
                inventory.remove("Cursed Blade")
                inventory.remove("Ruiner's Eye")
                inventory.remove("Deathdreg Nexus")
                counter -= 1
              dd_units += mult
              for i in range(1, mult+1):
                ddunitlist.append(Troop(1,3,6,(randint(1,10)),randint(1,10),randint(1,5),randint(0,9)))
              print("Raised %d DEATHDREG RUINER(S)." % mult)
              print("")
              trooperlooper = False
            
          else:
            print("You don't currently have the means to raise Ruiners.")
            print("")
            

        else:
          print("Undead class not found.")
          print("")
          
      except:
        print("Requires a numeric value.\n ")

def showunits():    #Displays faction-specific unit names and their quantities.
  
  if faction == "TYRANNY":
    print("Petrov units: %d" % light_units)
    for unit in lightunitlist:
      print("{}{}".format(unit.special(),unit.name()))

    print("Commandos: %d" % mid_units)
    for unit in midunitlist:
      print("{}{}".format(unit.special(),unit.name()))

    print("Siegebreaker units: %d" % heavy_units)
    for unit in heavyunitlist:
      print("{}{}".format(unit.special(),unit.name()))

  elif faction == "NECROPOLIS":
    print("Legionnaires: %d" % light_units)
    for unit in lightunitlist:
      print("{}{}".format(unit.special(),unit.name()))

    print("Vengeful Dead: %d" % mid_units)
    for unit in midunitlist:
      print("{}{}".format(unit.special(),unit.name()))
 
    print("Promethids: %d" % heavy_units)
    for unit in heavyunitlist:
      print("{}{}".format(unit.special(),unit.name()))

    if dd_units > 0:    #Displays Deathdreg units if the user's faction is "Necropolis" and their deathdreg unit count is 1 or more.
      print("Deathdreg Ruiners: %d" % dd_units)
  print("")

def scav():    #Allows the user to choose an available amount of a single purchased unit type, and dispatch them on scouting missions for up to 7 days. Returns an event for each day in the field which can affect purchased units, points or inventory.

  global points
  global faction
  global light_units
  global mid_units
  global heavy_units
  global dd_units
  global inventory
  totalunits = (light_units + mid_units + heavy_units)    #Sets the total number of units possessed by the player by calculating the sum of all light, mid and heavy units.
  
  if totalunits >= 1:    #Begins the function if [totalunits] is 1 or more.
    assigned_units = 0    #Initialises [assigned_units] at a value of 0.
    warrior = False    #Tracks whether the special event for dispatched Legionnaire units has been triggered.
    lover = False    #Tracks whether the special event for dispatched Vengeful Dead units has been triggered.
    master = False    #Tracks whether the special event for dispatched Promethid units has been triggered.
    petrov_s = False    #Tracks whether the special event (placeholder) for Petrov units has been triggered.
    comm_s = False    #Tracks whether the special event (placeholder) for Commando units has been triggered.
    siege_s = False    #Tracks whether the special event (placeholder) for Siegebreaker units has been triggered.
    dispatch_type = input("Choose a unit type to dispatch.\n >")    #Sets [dispatch_type] to the user-specified unit type for dispatch.
    print("")
    try:
      if faction == "NECROPOLIS":
        if dispatch_type.lower() in necro_unit_names:    #Checks if the chosen dispatch_type is present in the [necro_unit_names] list.
          assigned_units = int(input("Choose a number of units to dispatch.\n >"))    #Sets [assigned_units] to a user-specified quantity of units to dispatch.
          print("")
          if dispatch_type.lower() == "legionnaire" and assigned_units <= light_units:    #Checks if [dispatch_type] references Legionnaire, and then verifies whether there are enough units in [light_units] to populate [assigned_units].
            scav_duration = int(input("Choose a dispatch order duration. (max. 7 days) \n >"))    #Initialises [scav_duration] with the number of events to generate for the current dispatch.
            print("")
            if scav_duration <= 7:    #Checks that [scav_duration] doesn't exceed the maximum dispatch period of 7 days.
              scav_turns = 1    #Initialises [scav_turns] at 1, starting the first day of dispatch.
              light_units -= assigned_units    #Subtracts the value of [assigned_units] from [light_units].
              while scav_turns <= scav_duration:    #Loops while [scav_turns] is lower than the established value of [scav_duration].
                if assigned_units > 0:    #Checks that [assigned_units] isn't at 0, and proceeds if so.
                  if warrior == False:    #Checks that the legionnaire special event hasn't been triggered.
                    event = randint(1, 101)    #If it hasn't, [event] is set to a randomly selected integer between 1 and 100.
                  else:
                    event = randint(1, 100)    #If it has, [event] is limited to being between 1-99 in order to exclude the special event and prevent it from occurring twice in one dispatch.
                  
                  print("Units remaining: %d" % assigned_units)    #Prints the value of [assigned_units] before each event.
                  
                  if event == 1: #Team suffers heavy losses.
                    print("Day %s: Your %s team has run afoul of a natural disaster and suffered heavy losses. %d units lost." % (scav_turns, dispatch_type.lower(), round_up(assigned_units/4)))
                    print("")
                    assigned_units -= int(round_up(assigned_units / 4))    #Reduces [assigned_units] by 1/4, rounded up.
                    scav_turns += 1    #Increases the value of [scav_turns] by 1.
                    
                  elif event in range(2,11):    #Team intercepts an enemy squad escorting a resource cache.
                    print("Day %s: Your %s team has intercepted a small cache of resources being transported by a small enemy squad." % (scav_turns, dispatch_type.lower()))
                    outcome = randint(1, 5)    #Determines the outcome of the encounter by selecting a random integer between 1 and 5.
                    if outcome == 1:    #Team is repelled, suffering one loss.
                      print("Your unit did not fare well in the conflict. You were driven off, failing to claim the resources and losing 1 %s in the process." % dispatch_type.lower())
                      print("")
                      assigned_units -= 1    #Reduces the value of [assigned_units] by 1.
                    elif outcome in range(2, 5):    #Team is victorious, but damaged the cache.
                      print("Your unit successfully neutralised the enemy squad, but the resource cache was damaged in the conflict.")
                      print("+5 points.")
                      print("")
                      points += 5    #Increases [points] by 5.
                    elif outcome == 5:    #Team is victorious, and kept the cache untouched.
                      print("Your unit took the enemy by surprise, achieving a flawless victory and securing the resource cache.")
                      print("+10 points.")
                      print("")
                      points += 10    #Increases [points] by 10.
                    scav_turns += 1

                  elif event in range(11,31):    #Team ends the day empty-handed.
                    print("Day %s: Your unit has nothing to show for the day but covered ground." % scav_turns)
                    print("")
                    scav_turns += 1

                  elif event in range(31,50):    #Team finds the remains of a Tyranny patrol.
                    print("Day %s: Your %s team find the scattered remains of a Tyranny patrol." % (scav_turns, dispatch_type.lower()))
                    if event in range(31, 35):    #Trail leads to a survivor camp.
                      print("The trail leads to a small encampment of the patrol's survivors.") 
                      if event in range(31, 33):    #Survivors flee.
                        print("The survivors don't like their odds, and flee before your team can engage.")
                        print("")
                      if event == 33:    #Survivors resist.
                        print("The survivors were too well-prepared and fend you off, killing 1 %s in the process." % dispatch_type.lower())
                        print("")
                        assigned_units -= 1
                      if event == 34:    #Survivors eliminated.
                        print("The survivors are too devastated by their previous loss, and crumble under your assault. You recover a small cache of supplies. +5 points.")
                        print("")
                        points += 5
                    if event in range(35, 40):    #Trail leads to a Deathdreg Revenant.
                      print("The trail leads to an area choked with antilife; at its centre, an idling Deathdreg Revenant.")
                      if event in range(35, 38):    #Revenant is friendly.
                        print("The Revenant appears to recognize your team's state of undeath and begins following them.")
                        print("")
                        dd_units += 1
                      if event in range(38, 40):    #Revenant is hostile.
                        deathdreg = Troop(1,3,6,(randint(1,10)),randint(1,10),randint(1,5))    #Creates an instance of the Troop class set to Deathdreg Revenant parameters.
                        print("The Revenant is beyond sanity, and attacks. In putting it to rest, you lose 1 %s." % dispatch_type.lower())
                        print("")
                        assigned_units -= 1
                        inventory.append(deathdreg.loots())    #Adds one item of Deathdreg troop loot to user's inventory.
                    if event in range(40, 45):    #Trail goes cold.
                      print("The trail runs cold. Whoever killed those troops, they're long gone. Good on them.")
                      print("")
                    if event in range(45, 50):    #Team encounters a Deathseeker.
                      print("You find a recently returned Deathseeker, evidently killed in their encounter with the troops, though ultimately appears no worse for wear. They decline to join your squad, but gladly hand over a cut of their spoils. +5 points.")
                      print("")
                      points += 5
                    scav_turns += 1

                  elif event in range(50,80): #enemy ambush
                    print("Day %s: Your %s team is ambushed by a squad of Tyranny Commandos." % (scav_turns, dispatch_type.lower()))
                    if event in range(50,60): #heavy losses
                      print("You overcome the assault, but lose %d unit(s) in the conflict." % (round_up(assigned_units/2)))
                      print("")
                      assigned_units -= int(round_up(assigned_units / 2))
                    
                    if event in range(60,70): #flawless victory
                      print("Your team crushes the ambush with ease and spend the rest of the day basking in the glory of their victory. +10 points.")
                      print("")
                      points += 10
                      
                    if event in range(70,80): #annihilated
                      print("Your team is annihilated by the ruthless assault, fated never to return.")
                      print("")
                      #scav_turns += ((scav_duration - scav_turns) + 1)
                      assigned_units = 0
                    scav_turns += 1
                    
                  elif event in range(80,90): #petrov corpse
                    print("Day %s: Your %s team finds the weathered remains of a long-since ruined Tyranny Petrov unit." % (scav_turns, dispatch_type.lower()))
                    print("Despite just being another heap of broken hardware, it's somehow a rather mournful scene.")
                    print("")
                    points -= 1
                    scav_turns += 1

                  elif event in range(90,100): #claimed unguarded cache
                    print("Day %s: Your %s team has located and secured an unguarded cache of resources. Points +25." % (scav_turns, dispatch_type.lower()))
                    print("")
                    points += 25
                    scav_turns += 1
                  
                  elif event == 100: #the warrior
                    print("The Warrior graces your squad of Legionnaires with his presence. Under his leadership, they will be nigh unstoppable.")
                    print("")
                    #light_units += (assigned_units * 2)
                    assigned_units *= 2
                    warrior = True
                
                else:
                  print("No units remaining. Dispatch aborted.")
                  scav_turns = 8
              
              else:
                print("Dispatch complete.")
                print("")
                light_units = int(light_units + assigned_units)
                if light_units < 0:
                  light_units = 0
              
            else: #dispatch > 7
              print("Teams cannot be dispatched for longer than 7 days.") #10

          elif dispatch_type.lower() == "vengeful" and assigned_units <= mid_units: #dispatched vengeful
            scav_duration = int(input("Choose a dispatch order duration. (max. 7 days) \n >"))
            print("")
            if scav_duration <= 7:
              scav_turns = 1
              mid_units -= assigned_units
              while scav_turns <= scav_duration:
                if assigned_units > 0:
                  if lover == False:
                    event = randint(1, 101)
                  else:
                    event = randint(1, 100)
                  
                  print("Units remaining: %d" % assigned_units)
                  
                  if event == 1: #heavy losses
                    print("Day %s: Your %s team has run afoul of a natural disaster and suffered heavy losses. %d units lost." % (scav_turns, dispatch_type.lower(), round_up(assigned_units/4)))
                    print("")
                    assigned_units -= int(round_up(assigned_units / 4))
                    scav_turns += 1
                    
                  elif event in range(2,11): #intercept cache escort
                    print("Day %s: Your %s team has intercepted a small cache of resources being transported by a small enemy squad." % (scav_turns, dispatch_type.lower()))
                    outcome = randint(1, 5)
                    if outcome == 1: #repelled, one loss
                      print("Your unit did not fare well in the conflict. You were driven off, failing to claim the resources and losing 1 %s in the process." % dispatch_type.lower())
                      print("")
                      assigned_units -= 1
                    elif outcome in range(2, 5): #victory, damaged cache
                      print("Your unit successfully neutralised the enemy squad, but the resource cache was damaged in the conflict.")
                      print("+5 points.")
                      print("")
                      points += 5
                    elif outcome == 5: #victory, intact cache
                      print("Your unit took the enemy by surprise, achieving a flawless victory and securing the resource cache.")
                      print("+10 points.")
                      print("")
                      points += 10
                    scav_turns += 1

                  elif event in range(11,31): #empty-handed
                    print("Day %s: Your unit has nothing to show for the day but covered ground." % scav_turns)
                    print("")
                    scav_turns += 1

                  elif event in range(31,50): #tyranny troop remains
                    print("Day %s: Your %s team find the scattered remains of a Tyranny patrol." % (scav_turns, dispatch_type.lower()))
                    if event in range(31, 35): #survivor camp
                      print("The trail leads to a small encampment of the patrol's survivors.") 
                      if event in range(31, 33): #survivors flee
                        print("The survivors don't like their odds, and flee before your team can engage.")
                        print("")
                      if event == 33: #survivors resist
                        print("The survivors were too well-prepared and fend you off, killing 1 %s in the process." % dispatch_type.lower())
                        print("")
                        assigned_units -= 1
                      if event == 34: #survivors finished
                        print("The survivors are too devastated by their previous loss, and crumble under your assault. You recover a small cache of supplies. +5 points.")
                        print("")
                        points += 5
                    if event in range(35, 40): #deathdreg field
                      print("The trail leads to an area choked with antilife; at its centre, an idling Deathdreg Revenant.")
                      if event in range(35, 38): #revenant follows
                        print("The Revenant appears to recognize your team's state of undeath and begins following them.")
                        print("")
                        dd_units += 1
                      if event in range(38, 40): #revenant attacks
                        deathdreg = Troop(1,3,6,(randint(1,10)),randint(1,10),randint(1,5))
                        print("The Revenant is beyond sanity, and attacks. In putting it to rest, you lose 1 %s." % dispatch_type.lower())
                        print("")
                        assigned_units -= 1
                        inventory.append(deathdreg.loots())
                    if event in range(40, 45): #cold trail
                      print("The trail runs cold. Whoever killed those troops, they're long gone. Good on them.")
                      print("")
                    if event in range(45, 50): #deathseeker
                      print("You find a recently returned Deathseeker, evidently killed sometime during their scuffle with the troops -- albeit not before giving as good as they got. They decline to join your squad, but gladly hand over a cut of their spoils. +5 points.")
                      print("")
                      points += 5
                    scav_turns += 1

                  elif event in range(50,80): #enemy ambush
                    print("Day %s: Your %s team is ambushed by a squad of Tyranny Commandos." % (scav_turns, dispatch_type.lower()))
                    if event in range(50,60): #heavy losses
                      print("You overcome the assault, but lose %d unit(s) in the conflict." % round_up(assigned_units/2))
                      print("")
                      assigned_units -= int(round_up(assigned_units / 2))
                    
                    if event in range(60,70): #flawless victory
                      print("Your team crushes the ambush with ease and spend the rest of the day basking in the glory of their victory. +10 points.")
                      print("")
                      points += 10
                      
                    if event in range(70,80): #annihilated
                      print("Your team is annihilated by the ruthless assault, fated never to return.")
                      print("")
                      #scav_turns += ((scav_duration - scav_turns) + 1)
                      assigned_units = 0
                    scav_turns += 1
                    
                  elif event in range(80,90): #petrov corpse
                    print("Day %s: Your %s team finds the weathered remains of a long-since ruined Tyranny Petrov unit." % (scav_turns, dispatch_type.lower()))
                    print("Despite just being another heap of broken hardware, it's somehow a rather mournful scene.")
                    print("")
                    points -= 1
                    scav_turns += 1

                  elif event in range(90,100): #claimed unguarded cache
                    print("Day %s: Your %s team has located and secured an unguarded cache of resources. Points +25." % (scav_turns, dispatch_type.lower()))
                    print("")
                    points += 25
                    scav_turns += 1
                  
                  elif event == 100: #the lover
                    print("The Drowned Lover graces your squad of Vengeful Dead with her presence. Under her leadership, their fury will be nigh unstoppable.")
                    print("")
                    #mid_units += (assigned_units * 2)
                    assigned_units *= 2
                    lover = True
                
                else:
                  print("No units remaining. Dispatch aborted.")
                  scav_turns = 8
              
              else:
                print("Dispatch complete.")
                print("")
                mid_units = int(mid_units + assigned_units)
                if mid_units < 0:
                  mid_units = 0
              
            else: #dispatch > 7
              print("Teams cannot be dispatched for longer than 7 days.") #10

          elif dispatch_type.lower() == "promethid" and assigned_units <= heavy_units: #dispatched promethids
            scav_duration = int(input("Choose a dispatch order duration. (max. 7 days) \n >"))
            print("")
            if scav_duration <= 7:
              scav_turns = 1
              heavy_units -= assigned_units
              while scav_turns <= scav_duration:
                if assigned_units > 0:
                  if master == False:
                    event = randint(1, 101)
                  else:
                    event = randint(1, 100)
                  
                  print("Units remaining: %d" % assigned_units)
                  
                  if event == 1: #heavy losses
                    print("Day %s: Your %s team has run afoul of a natural disaster and suffered heavy losses. %d units lost." % (scav_turns, dispatch_type.lower(), round_up(assigned_units/4)))
                    print("")
                    assigned_units -= int(round_up(assigned_units / 4))
                    scav_turns += 1
                    
                  elif event in range(2,11): #intercept cache escort
                    print("Day %s: Your %s team has intercepted a small cache of resources being transported by a small enemy squad." % (scav_turns, dispatch_type.lower()))
                    outcome = randint(1, 5)
                    if outcome == 1: #repelled, one loss
                      print("Your unit did not fare well in the conflict. You were driven off, failing to claim the resources and losing 1 %s in the process." % dispatch_type.lower())
                      print("")
                      assigned_units -= 1
                    elif outcome in range(2, 5): #victory, damaged cache
                      print("Your unit successfully neutralised the enemy squad, but the resource cache was damaged in the conflict.")
                      print("+5 points.")
                      print("")
                      points += 5
                    elif outcome == 5: #victory, intact cache
                      print("Your unit took the enemy by surprise, achieving a flawless victory and securing the resource cache.")
                      print("+10 points.")
                      print("")
                      points += 10
                    scav_turns += 1

                  elif event in range(11,31): #empty-handed
                    print("Day %s: Your unit has nothing to show for the day but covered ground." % scav_turns)
                    print("")
                    scav_turns += 1

                  elif event in range(31,50): #tyranny troop remains
                    print("Day %s: Your %s team find the scattered remains of a Tyranny patrol." % (scav_turns, dispatch_type.lower()))
                    if event in range(31, 35): #survivor camp
                      print("The trail leads to a small encampment of the patrol's survivors.") 
                      if event in range(31, 33): #survivors flee
                        print("The survivors don't like their odds, and flee before your team can engage.")
                        print("")
                      if event == 33: #survivors resist
                        print("The survivors were too well-prepared and fend you off, killing 1 %s in the process." % dispatch_type.lower())
                        print("")
                        assigned_units -= 1
                      if event == 34: #survivors finished
                        print("The survivors are too devastated by their previous loss, and crumble under your assault. You recover a small cache of supplies. +5 points.")
                        print("")
                        points += 5
                    if event in range(35, 40): #deathdreg field
                      print("The trail leads to an area choked with antilife; at its centre, an idling Deathdreg Revenant.")
                      if event in range(35, 38): #revenant follows
                        print("The Revenant appears to recognize your team's state of undeath and begins following them.")
                        print("")
                        dd_units += 1
                      if event in range(38, 40): #revenant attacks
                        deathdreg = Troop(1,3,6,(randint(1,10)),randint(1,10),randint(1,5))
                        print("The Revenant is beyond sanity, and attacks. In putting it to rest, you lose 1 %s." % dispatch_type.lower())
                        print("")
                        assigned_units -= 1
                        inventory.append(deathdreg.loots())
                    if event in range(40, 45): #cold trail
                      print("The trail runs cold. Whoever killed those troops, they're long gone. Good on them.")
                      print("")
                    if event in range(45, 50): #deathseeker
                      print("You find a recently returned Deathseeker, evidently killed sometime during their scuffle with the troops -- albeit not before giving as good as they got. They decline to join your squad, but gladly hand over a cut of their spoils. +5 points.")
                      print("")
                      points += 5
                    scav_turns += 1

                  elif event in range(50,80): #enemy ambush
                    print("Day %s: Your %s team is ambushed by a squad of Tyranny Commandos." % (scav_turns, dispatch_type.lower()))
                    if event in range(50,60): #heavy losses
                      print("You overcome the assault, but lose %d unit(s) in the conflict." % round_up(assigned_units/2))
                      print("")
                      assigned_units -= int(round_up(assigned_units / 2))
                    
                    if event in range(60,70): #flawless victory
                      print("Your team crushes the ambush with ease and spend the rest of the day basking in the glory of their victory. +10 points.")
                      print("")
                      points += 10
                      
                    if event in range(70,80): #annihilated
                      print("Your team is annihilated by the ruthless assault, fated never to return.")
                      print("")
                      #scav_turns += ((scav_duration - scav_turns) + 1)
                      assigned_units = 0
                    scav_turns += 1
                    
                  elif event in range(80,90): #petrov corpse
                    print("Day %s: Your %s team finds the weathered remains of a long-since ruined Tyranny Petrov unit." % (scav_turns, dispatch_type.lower()))
                    print("Despite just being another heap of broken hardware, it's somehow a rather mournful scene.")
                    print("")
                    points -= 1
                    scav_turns += 1

                  elif event in range(90,100): #claimed unguarded cache
                    print("Day %s: Your %s team has located and secured an unguarded cache of resources. Points +25." % (scav_turns, dispatch_type.lower()))
                    print("")
                    points += 25
                    scav_turns += 1
                  
                  elif event == 100: #the master
                    print("The unearthly strains of a phantom violin echo all around your Promethid team. The Master is with them; for their foes, all hope is lost.")
                    print("")
                    #heavy_units += (assigned_units * 2)
                    assigned_units *= 2
                    master = True
                
                else:
                  print("No units remaining. Dispatch aborted.")
                  scav_turns = 8
              
              else:
                print("Dispatch complete.")
                print("")
                heavy_units = int(heavy_units + assigned_units)
                if heavy_units < 0:
                  heavy_units = 0
              
            else: #dispatch > 7
              print("Teams cannot be dispatched for longer than 7 days.") #10
         
          else:
            print("Insufficient units in reserve.")
            print("")
            
        else:
          print("Unit type not found.")
        
      elif faction == "TYRANNY":
        if dispatch_type.lower() in tyr_unit_names:
          assigned_units = int(input("Choose a number of units to dispatch.\n >"))
          print("")
          if dispatch_type.lower() == "petrov" and assigned_units <= light_units: #dispatched petrov
            scav_duration = int(input("Choose a dispatch order duration. (max. 7 days) \n >"))
            print("")
            if scav_duration <= 7:
              scav_turns = 1
              light_units -= assigned_units
              while scav_turns <= scav_duration:
                if assigned_units > 0:
                  if petrov_s == False:
                    event = randint(1, 101)
                  else:
                    event = randint(1, 100)
                  
                  print("Units remaining: %d" % assigned_units)
                  
                  if event == 1: #heavy losses
                    print("Day %s: Your %s team has run afoul of a natural disaster and suffered heavy losses. %d units lost." % (scav_turns, dispatch_type.lower(), round_up(assigned_units/4)))
                    print("")
                    assigned_units -= int(round_up(assigned_units / 4))
                    scav_turns += 1
                    
                  elif event in range(2,11): #intercept cache escort
                    print("Day %s: Your %s team has intercepted a small cache of resources being transported by a small enemy squad." % (scav_turns, dispatch_type.lower()))
                    outcome = randint(1, 5)
                    if outcome == 1: #repelled, one loss
                      print("Your unit did not fare well in the conflict. You were driven off, failing to claim the resources and losing 1 %s in the process." % dispatch_type.lower())
                      print("")
                      assigned_units -= 1
                    elif outcome in range(2, 5): #victory, damaged cache
                      print("Your unit successfully neutralised the enemy squad, but the resource cache was damaged in the conflict.")
                      print("+5 points.")
                      print("")
                      points += 5
                    elif outcome == 5: #victory, intact cache
                      print("Your unit took the enemy by surprise, achieving a flawless victory and securing the resource cache.")
                      print("+10 points.")
                      print("")
                      points += 10
                    scav_turns += 1

                  elif event in range(11,31): #empty-handed
                    print("Day %s: Your unit has nothing to show for the day but covered ground." % scav_turns)
                    print("")
                    scav_turns += 1

                  elif event in range(31,50): #necro troop remains
                    print("Day %s: Your %s team find the scattered remains of a Necropolitan patrol." % (scav_turns, dispatch_type.lower()))
                    if event in range(31, 35): #survivor camp
                      print("The trail leads to a small encampment of the patrol's survivors.") 
                      if event in range(31, 33): #survivors flee
                        print("The survivors don't like their odds, and flee before your team can engage.")
                        print("")
                      if event == 33: #survivors resist
                        print("The survivors were too well-prepared and fend you off, killing 1 %s in the process." % dispatch_type.lower())
                        print("")
                        assigned_units -= 1
                      if event == 34: #survivors finished
                        print("The survivors are too devastated by their previous loss, and crumble under your assault. You recover a small cache of supplies. +5 points.")
                        print("")
                        points += 5
                    if event in range(35, 40): #deathdreg field
                      print("The trail leads to an area choked with antilife; at its centre is an idling Deathdreg Revenant, evidently having attacked its own.")
                      if event in range(35, 38): #revenant weakened
                        print("The Revenant is weakened from its previous battle and proves little challenge. Your victory is inspiring.")
                        print("+10 points.")
                        print("")
                        points += 10
                      if event in range(38, 40): #revenant stronk
                        print("The Revenant is too strong. In putting it to rest, you lose 1 %s." % dispatch_type.lower())
                        print("")
                        assigned_units -= 1
                    if event in range(40, 45): #cold trail
                      print("The trail runs cold. Whoever put down these corpses, they're long gone. Good on them.")
                      print("")
                    if event in range(45, 50): #deathseeker
                      print("You find a recently returned Deathseeker, evidently killed sometime during their scuffle with the troops -- albeit not before giving as good as they got. They decline to join your squad, but gladly hand over a cut of their spoils. +5 points.")
                      print("")
                      points += 5
                    scav_turns += 1

                  elif event in range(50,80): #enemy ambush
                    print("Day %s: Your %s team is ambushed by a squad of Vengeful Dead." % (scav_turns, dispatch_type.lower()))
                    if event in range(50,60): #heavy losses
                      print("You overcome the assault, but lose %d unit(s) in the conflict." % round_up(assigned_units/2))
                      print("")
                      assigned_units -= int(round_up(assigned_units / 2))
                    
                    if event in range(60,70): #flawless victory
                      print("Your team crushes the ambush with ease and spend the rest of the day basking in the glory of their victory. +10 points.")
                      print("")
                      points += 10
                      
                    if event in range(70,80): #annihilated
                      print("Your team is annihilated by the ruthless assault, fated never to return.")
                      print("")
                      #scav_turns += ((scav_duration - scav_turns) + 1)
                      assigned_units = 0
                    scav_turns += 1
                    
                  elif event in range(80,90): #petrov corpse
                    print("Day %s: Your %s team finds the weathered remains of a long-since ruined Tyranny Petrov unit." % (scav_turns, dispatch_type.lower()))
                    print("Despite just being another heap of broken hardware, it's somehow a rather mournful scene.")
                    print("")
                    points -= 1
                    scav_turns += 1

                  elif event in range(90,100): #claimed unguarded cache
                    print("Day %s: Your %s team has located and secured an unguarded cache of resources. Points +25." % (scav_turns, dispatch_type.lower()))
                    print("")
                    points += 25
                    scav_turns += 1
                  
                  elif event == 100: #REND
                    print("Petrov special event placeholder")
                    print("")
                    #light_units += (assigned_units * 2)
                    assigned_units *= 2
                    petrov_s = True
                
                else:
                  print("No units remaining. Dispatch aborted.")
                  scav_turns = 8
              
              else:
                print("Dispatch complete.")
                print("")
                light_units = int(light_units + assigned_units)
                if light_units < 0:
                  light_units = 0
              
            else: #dispatch > 7
              print("Teams cannot be dispatched for longer than 7 days.") #10
          
          elif dispatch_type.lower() == "commando" and assigned_units <= mid_units: #dispatched commando
            scav_duration = int(input("Choose a dispatch order duration. (max. 7 days) \n >"))
            print("")
            if scav_duration <= 7:
              scav_turns = 1
              mid_units -= assigned_units
              while scav_turns <= scav_duration:
                if assigned_units > 0:
                  if comm_s == False:
                    event = randint(1, 101)
                  else:
                    event = randint(1, 100)
                  
                  print("Units remaining: %d" % assigned_units)
                  
                  if event == 1: #heavy losses
                    print("Day %s: Your %s team has run afoul of a natural disaster and suffered heavy losses. %d units lost." % (scav_turns, dispatch_type.lower(), round_up(assigned_units/4)))
                    print("")
                    assigned_units -= int(round_up(assigned_units / 4))
                    scav_turns += 1
                    
                  elif event in range(2,11): #intercept cache escort
                    print("Day %s: Your %s team has intercepted a small cache of resources being transported by a small enemy squad." % (scav_turns, dispatch_type.lower()))
                    outcome = randint(1, 5)
                    if outcome == 1: #repelled, one loss
                      print("Your unit did not fare well in the conflict. You were driven off, failing to claim the resources and losing 1 %s in the process." % dispatch_type.lower())
                      print("")
                      assigned_units -= 1
                    elif outcome in range(2, 5): #victory, damaged cache
                      print("Your unit successfully neutralised the enemy squad, but the resource cache was damaged in the conflict.")
                      print("+5 points.")
                      print("")
                      points += 5
                    elif outcome == 5: #victory, intact cache
                      print("Your unit took the enemy by surprise, achieving a flawless victory and securing the resource cache.")
                      print("+10 points.")
                      print("")
                      points += 10
                    scav_turns += 1

                  elif event in range(11,31): #empty-handed
                    print("Day %s: Your unit has nothing to show for the day but covered ground." % scav_turns)
                    print("")
                    scav_turns += 1

                  elif event in range(31,50): #tyranny troop remains
                    print("Day %s: Your %s team find the scattered remains of a Tyranny patrol." % (scav_turns, dispatch_type.lower()))
                    if event in range(31, 35): #survivor camp
                      print("The trail leads to a small encampment of the patrol's survivors.") 
                      if event in range(31, 33): #survivors flee
                        print("The survivors don't like their odds, and flee before your team can engage.")
                        print("")
                      if event == 33: #survivors resist
                        print("The survivors were too well-prepared and fend you off, killing 1 %s in the process." % dispatch_type.lower())
                        print("")
                        assigned_units -= 1
                      if event == 34: #survivors finished
                        print("The survivors are too devastated by their previous loss, and crumble under your assault. You recover a small cache of supplies. +5 points.")
                        print("")
                        points += 5
                    if event in range(35, 40): #deathdreg field
                      print("The trail leads to an area choked with antilife; at its centre is an idling Deathdreg Revenant, evidently having attacked its own.")
                      if event in range(35, 38): #revenant follows
                        print("The Revenant is weakened from its previous battle and proves little challenge. Your victory is inspiring.")
                        print("+10 points.")
                        print("")
                        points += 10
                      if event in range(38, 40): #revenant attacks
                        print("The Revenant is too strong. In putting it to rest, you lose 1 %s." % dispatch_type.lower())
                        print("")
                        assigned_units -= 1
                    if event in range(40, 45): #cold trail
                      print("The trail runs cold. Whoever killed those troops, they're long gone. Good on them.")
                      print("")
                    if event in range(45, 50): #deathseeker
                      print("You find a recently returned Deathseeker, evidently killed sometime during their scuffle with the troops -- albeit not before giving as good as they got. They decline to join your squad, but gladly hand over a cut of their spoils. +5 points.")
                      print("")
                      points += 5
                    scav_turns += 1

                  elif event in range(50,80): #enemy ambush
                    print("Day %s: Your %s team is ambushed by a squad of Tyranny Commandos." % (scav_turns, dispatch_type.lower()))
                    if event in range(50,60): #heavy losses
                      print("You overcome the assault, but lose %d unit(s) in the conflict." % round_up(assigned_units/2))
                      print("")
                      assigned_units -= int(round_up(assigned_units / 2))
                    
                    if event in range(60,70): #flawless victory
                      print("Your team crushes the ambush with ease and spend the rest of the day basking in the glory of their victory. +10 points.")
                      print("")
                      points += 10
                      
                    if event in range(70,80): #annihilated
                      print("Your team is annihilated by the ruthless assault, fated never to return.")
                      print("")
                      #scav_turns += ((scav_duration - scav_turns) + 1)
                      assigned_units = 0
                    scav_turns += 1
                    
                  elif event in range(80,90): #petrov corpse
                    print("Day %s: Your %s team finds the weathered remains of a long-since ruined Tyranny Petrov unit." % (scav_turns, dispatch_type.lower()))
                    print("Despite just being another heap of broken hardware, it's somehow a rather mournful scene.")
                    print("")
                    points -= 1
                    scav_turns += 1

                  elif event in range(90,100): #claimed unguarded cache
                    print("Day %s: Your %s team has located and secured an unguarded cache of resources. Points +25." % (scav_turns, dispatch_type.lower()))
                    print("")
                    points += 25
                    scav_turns += 1
                  
                  elif event == 100: #spearman
                    print("Commando special event placeholder")
                    print("")
                    #mid_units += (assigned_units * 2)
                    assigned_units *= 2
                    comm_s = True
                
                else:
                  print("No units remaining. Dispatch aborted.")
                  scav_turns = 8
              
              else:
                print("Dispatch complete.")
                print("")
                mid_units = int(mid_units + assigned_units)
                if mid_units < 0:
                  mid_units = 0
              
            else: #dispatch > 7
              print("Teams cannot be dispatched for longer than 7 days.") #10
          
          elif dispatch_type.lower() == "siegebreaker" and assigned_units <= heavy_units: #dispatched siegebreaker
            scav_duration = int(input("Choose a dispatch order duration. (max. 7 days) \n >"))
            print("")
            if scav_duration <= 7:
              scav_turns = 1
              heavy_units -= assigned_units
              while scav_turns <= scav_duration:
                if assigned_units > 0:
                  if siege_s == False:
                    event = randint(1, 101)
                  else:
                    event = randint(1, 100)
                  
                  print("Units remaining: %d" % assigned_units)
                  
                  if event == 1: #heavy losses
                    print("Day %s: Your %s team has run afoul of a natural disaster and suffered heavy losses. %d units lost." % (scav_turns, dispatch_type.lower(), round_up(assigned_units/4)))
                    print("")
                    assigned_units -= int(round_up(assigned_units / 4))
                    scav_turns += 1
                    
                  elif event in range(2,11): #intercept cache escort
                    print("Day %s: Your %s team has intercepted a small cache of resources being transported by a small enemy squad." % (scav_turns, dispatch_type.lower()))
                    outcome = randint(1, 5)
                    if outcome == 1: #repelled, one loss
                      print("Your unit did not fare well in the conflict. You were driven off, failing to claim the resources and losing 1 %s in the process." % dispatch_type.lower())
                      print("")
                      assigned_units -= 1
                    elif outcome in range(2, 5): #victory, damaged cache
                      print("Your unit successfully neutralised the enemy squad, but the resource cache was damaged in the conflict.")
                      print("+5 points.")
                      print("")
                      points += 5
                    elif outcome == 5: #victory, intact cache
                      print("Your unit took the enemy by surprise, achieving a flawless victory and securing the resource cache.")
                      print("+10 points.")
                      print("")
                      points += 10
                    scav_turns += 1

                  elif event in range(11,31): #empty-handed
                    print("Day %s: Your unit has nothing to show for the day but covered ground." % scav_turns)
                    print("")
                    scav_turns += 1

                  elif event in range(31,50): #tyranny troop remains
                    print("Day %s: Your %s team find the scattered remains of a Tyranny patrol." % (scav_turns, dispatch_type.lower()))
                    if event in range(31, 35): #survivor camp
                      print("The trail leads to a small encampment of the patrol's survivors.") 
                      if event in range(31, 33): #survivors flee
                        print("The survivors don't like their odds, and flee before your team can engage.")
                        print("")
                      if event == 33: #survivors resist
                        print("The survivors were too well-prepared and fend you off, killing 1 %s in the process." % dispatch_type.lower())
                        print("")
                        assigned_units -= 1
                      if event == 34: #survivors finished
                        print("The survivors are too devastated by their previous loss, and crumble under your assault. You recover a small cache of supplies. +5 points.")
                        print("")
                        points += 5
                    if event in range(35, 40): #deathdreg field
                      print("The trail leads to an area choked with antilife; at its centre is an idling Deathdreg Revenant, evidently having attacked its own.")
                      if event in range(35, 38): #revenant follows
                        print("The Revenant is weakened from its previous battle and proves little challenge. Your victory is inspiring.")
                        print("+10 points.")
                        print("")
                        points += 10
                      if event in range(38, 40): #revenant attacks
                        print("The Revenant is too strong. In putting it to rest, you lose 1 %s." % dispatch_type.lower())
                        print("")
                        assigned_units -= 1
                    if event in range(40, 45): #cold trail
                      print("The trail runs cold. Whoever killed those troops, they're long gone. Good on them.")
                      print("")
                    if event in range(45, 50): #deathseeker
                      print("You find a recently returned Deathseeker, evidently killed sometime during their scuffle with the troops -- albeit not before giving as good as they got. They decline to join your squad, but gladly hand over a cut of their spoils. +5 points.")
                      print("")
                      points += 5
                    scav_turns += 1

                  elif event in range(50,80): #enemy ambush
                    print("Day %s: Your %s team is ambushed by a squad of Tyranny Commandos." % (scav_turns, dispatch_type.lower()))
                    if event in range(50,60): #heavy losses
                      print("You overcome the assault, but lose %d unit(s) in the conflict." % round_up(assigned_units/2))
                      print("")
                      assigned_units -= int(round_up(assigned_units / 2))
                    
                    if event in range(60,70): #flawless victory
                      print("Your team crushes the ambush with ease and spend the rest of the day basking in the glory of their victory. +10 points.")
                      print("")
                      points += 10
                      
                    if event in range(70,80): #annihilated
                      print("Your team is annihilated by the ruthless assault, fated never to return.")
                      print("")
                      #scav_turns += ((scav_duration - scav_turns) + 1)
                      assigned_units = 0
                    scav_turns += 1
                    
                  elif event in range(80,90): #petrov corpse
                    print("Day %s: Your %s team finds the weathered remains of a long-since ruined Tyranny Petrov unit." % (scav_turns, dispatch_type.lower()))
                    print("Despite just being another heap of broken hardware, it's somehow a rather mournful scene.")
                    print("")
                    points -= 1
                    scav_turns += 1

                  elif event in range(90,100): #claimed unguarded cache
                    print("Day %s: Your %s team has located and secured an unguarded cache of resources. Points +25." % (scav_turns, dispatch_type.lower()))
                    print("")
                    points += 25
                    scav_turns += 1
                  
                  elif event == 100: #the master
                    print("Siegebreaker special event placeholder")
                    print("")
                    #heavy_units += (assigned_units * 2)
                    assigned_units *= 2
                    siege_s = True
                
                else:
                  print("No units remaining. Dispatch aborted.")
                  scav_turns = 8
              
              else:
                print("Dispatch complete.")
                print("")
                heavy_units = int(heavy_units + assigned_units)
                if heavy_units < 0:
                  heavy_units = 0
              
            else: #dispatch > 7
              print("Teams cannot be dispatched for longer than 7 days.") #10
         
          else:
            print("Insufficient units in reserve.")
            print("") 
          
        else:
          print("Unit type not found.")
    except:
      print("###Requires a numeric value. Command aborted.###\n ")
  else:
    print("Insufficent troops. Purchase at least 1 unit to dispatch.")

def battle():    #Allows the user to specify a single instance of a unit in reserve and pit it against a randomly selected unit from the opposing faction in order to earn loot.
  global light_units
  global mid_units
  global heavy_units
  global inventory
  #--------------------------------Troop Stats--------------------------------# 
  #Example: Troop(0,1,1,6,5,3,7) - Caustic Tyranny Commando - is a (0)Tyranny (1)medium-class (1)Commando with an attack stat of (6), a defense stat of (5) and an agility stat of (3) with the prefix (7)Caustic.  
  legionnaire = Troop(1,0,3,3,2,5,randint(0,9)) #attack rating 3*5=15 / evade rating 5*2 = 10
  petrov = Troop(0,0,0,3,2,5,randint(0,9)) #ar 3*5=15 / er 5*2 = 10
  vengeful = Troop(1,1,4,6,5,3,randint(0,9)) #ar 6*3=18 / er 3*5 =15 
  commando = Troop(0,1,1,6,5,3,randint(0,9)) #ar 6*3=18 / er 3*5 =15 
  promethid = Troop(1,2,5,10,7,1,randint(0,9)) #ar 10*1=10 / er 7*1=7
  siegebreaker = Troop(0,2,2,10,7,1,randint(0,9))
  deathdreg = Troop(1,3,6,(randint(1,10)),randint(1,10),randint(1,5),randint(0,9))
  
  lootinst = None   #Defines the loot dropped by defeated enemies, then added to inventory.

  necrodict = {"legionnaire":legionnaire, "vengeful":vengeful, "promethid":promethid, "deathdreg":deathdreg}

  tyrdict = {"petrov":petrov, "commando":commando, "siegebreaker":siegebreaker}

  unitdict = {"legionnaire":legionnaire, "vengeful":vengeful, "promethid":promethid, "petrov":petrov, "commando":commando, "siegebreaker":siegebreaker}
  
  
  valid = True
  p1 = None
  p2 = None
  player_select = input("Choose a unit to put forward for battle:\n >")
  if player_select.lower() in necrodict and faction == "NECROPOLIS":
  
    p1 = necrodict[player_select]
    p2 = choice(list(tyrdict.values()))
    if (p1.cls == 0 and light_units > 0) or (p1.cls == 1 and mid_units > 0) or (p1.cls == 2 and heavy_units > 0) or (p1.cls == 3 and dd_units > 0):
      print("Challenger 1: {}Necropolitan {} with attack rating {}, defence rating {} and agility rating {}.".format(p1.special(), p1.name(), p1.atk, p1.dfn, p1.agl))
      print("Challenger 2: {}Tyranny {} with attack rating {}, defence rating {} and agility rating {}.".format(p2.special(), p2.name(), p2.atk, p2.dfn, p2.agl))
      print(" ")
      unitonehp = p1.hp()
      unittwohp = p2.hp()
      while unitonehp > 0 and unittwohp > 0:
        p1atkroll = randint(1, p1.acc())
        p2evdroll = randint(1, p2.evade())
        p2atkroll = randint(1, p2.acc())
        p1evdroll = randint(1, p1.evade())
        print("{}{} attacks.".format(p1.special(),p1.name()))
        
        if p1atkroll < p2evdroll:       #Miss if player 1's attack roll is lower than player 2's evade roll
          print("p1:{} p2:{}".format(p1atkroll,p2evdroll))
          print("Attack missed.")
          if p1atkroll == 1:            #Stumble if player 1 attack roll equals 1
            print("{}{} stumbled!".format(p1.special(),p1.name()))
            if p2.spcl == 8:            #Chance for counterattack if player 2 has the "Opportunistic" prefix:
              print("{}{} launches a counter-attack!".format(p2.special(),p2.name()))
              p2atkroll = randint(1, p2.acc())
              p1evdroll = randint(1, p1.evade())
              if p2atkroll > p1evdroll:
                unitonehp -= p2.dmg()
                print("{}{} takes {} damage. {} HP remaining.".format(p1.special(), p1.name(), p2.dmg(), unitonehp))
              else:
                print("{}{} misses.".format(p2.special(),p2.name()))
          print("")
          
        elif p1atkroll > p2evdroll and p1atkroll < p1.acc():	  #if atkroll higher than evdroll but not p1.acc()
          print("p1:{} p2:{}".format(p1atkroll,p2evdroll))
          print("Attack hit!")
          unittwohp -= p1.dmg()
          print("{}{} takes {} damage. {} HP remaining.".format(p2.special(), p2.name(), p1.dmg(), unittwohp))
          print("")
          
        elif p1atkroll == p1.acc():    #if atkroll = p1.acc()
          print("p1:{} p2:{}".format(p1atkroll,p2evdroll))
          print("Critical hit!")
          unittwohp -= int((p1.dmg() *1.2))
          print("{}{} takes {:.0f} damage. {} HP remaining.".format(p2.special(), p2.name(), (p1.dmg()*1.2), unittwohp))
          print("")
          
        elif p1atkroll == p2.evade():  #if atkroll = p2.evade()
          print("p1:{} p2:{}".format(p1atkroll,p2evdroll))
          print("Attack parried!")
          if p2.spcl == 8:
            print("{}{} launches a counter-attack!".format(p2.special(),p2.name()))
            p2atkroll = randint(1, p2.acc())
            p1evdroll = randint(1, p1.evade())
            if p2atkroll > p1evdroll:
              unitonehp -= p2.dmg()
              print("{}{} takes {} damage. {} HP remaining.".format(p1.special(), p1.name(), p2.dmg(), unitonehp))
            else:
              print("{}{} misses.".format(p2.special(),p2.name()))
          #window of Opportunity
          print("")
        if unittwohp > 0:
          print("{}{} attacks.".format(p2.special(),p2.name()))
          if p2atkroll < p1evdroll:     #1
            print("p2:{} p1:{}".format(p2atkroll,p1evdroll))
            print("Attack missed.")
            if p2atkroll == 1:      #2
              print("{}{} stumbled!".format(p2.special(),p2.name()))
              if p1.spcl == 8:
                print("{}{} launches a counter-attack!".format(p1.special(),p1.name()))
                p1atkroll = randint(1, p2.acc())
                p2evdroll = randint(1, p1.evade())
                if p1atkroll > p2evdroll:
                  unittwohp -= p1.dmg()
                  print("{}{} takes {} damage. {} HP remaining.".format(p2.special(), p2.name(), p1.dmg(), unittwohp))
                else:
                  print("{}{} misses.".format(p1.special(),p1.name()))
              #window of Opportunity
            print("")
          elif p2atkroll > p1evdroll and p2atkroll < p2.acc():	  #if atkroll higher than evdroll but not p1.acc()
            print("p2:{} p1:{}".format(p2atkroll,p1evdroll))
            print("Attack hit!")
            unitonehp -= p2.dmg()
            print("{}{} takes {} damage. {} HP remaining.".format(p1.special(), p1.name(), p2.dmg(), unitonehp))
            print("")
          elif p2atkroll == p2.acc():    #if atkroll = p1.acc()
            print("p2:{} p1:{}".format(p2atkroll,p1evdroll))
            unitonehp -= int((p2.dmg() *1.2))
            print("Critical hit!")
            print("{}{} takes {:.0f} damage. {} HP remaining.".format(p1.special(), p1.name(), (p2.dmg()*1.2), unitonehp))
            print("")
          elif p2atkroll == p1.evade():  #if atkroll = p2.evade()
            print("p2:{} p1:{}".format(p2atkroll,p1evdroll))
            print("Attack parried!")
            if p1.spcl == 8:
              print("{}{} launches a counter-attack!".format(p1.special(),p1.name()))
              p1atkroll = randint(1, p2.acc())
              p2evdroll = randint(1, p1.evade())
              if p1atkroll > p2evdroll:
                unittwohp -= p1.dmg()
                print("{}{} takes {} damage. {} HP remaining.".format(p2.special(), p2.name(), p1.dmg(), unittwohp))
              else:
                print("{}{} misses.".format(p1.special(),p1.name()))
            #window of Opportunity
            print("")
            
      else:
        if unitonehp <= 0:
          if p1.cls == 0:
            light_units -= 1
          elif p1.cls == 1:
            mid_units -= 1
          elif p1.cls == 2:
            heavy_units -= 1
          print("Enemy victory.")
        elif unittwohp <= 0:
          print("Player victory.")
          lootinst = p2.loots()
          print("You found a %s!" % lootinst)
          inventory.append(lootinst)
    else:
      print("Insufficient units.")


  elif player_select.lower() in tyrdict and faction == "TYRANNY":
    p1 = tyrdict[player_select]
    p2 = choice(list(necrodict.values()))
    if (p1.cls == 0 and light_units > 0) or (p1.cls == 1 and mid_units > 0) or (p1.cls == 2 and heavy_units >0):
      print("Challenger 1: {}Tyranny {} with attack rating {}, defence rating {} and agility rating {}.".format(p1.special(), p1.name(), p1.atk, p1.dfn, p1.agl))
      print("Challenger 2: {}Necropolitan {} with attack rating {}, defence rating {} and agility rating {}.".format(p2.special(), p2.name(), p2.atk, p2.dfn, p2.agl))
      print(" ")
      unitonehp = p1.hp()
      unittwohp = p2.hp()
      while unitonehp > 0 and unittwohp > 0:    #While both units' HP is greater than 0,
        if unitonehp > 0:   #If unit 1's HP > 0,
          print("%s %s attacks." % (p1.special(), p1.name()))   #Unit 1 attacks.
          print(" ")
          #if p1.acc()= 
          unittwohp -= p1.dmg()   #unit 2 takes damage.
          print("%s %s takes %d damage. %d HP remaining." % (p2.special(), p2.name(), p1.dmg(), unittwohp))
          print("")
          if unittwohp > 0:
            print("%s %s attacks." % (p2.special(), p2.name()))
            print(" ")
            unitonehp -= p2.dmg()
            print("%s %s takes %d damage. %d HP remaining." % (p1.special(), p1.name(), p2.dmg(), unitonehp))
            print("")
      else:
        if unitonehp <= 0:
          if p1.cls == 0:
            light_units -= 1
          elif p1.cls == 1:
            mid_units -= 1
          elif p1.cls == 2:
            heavy_units -= 1
          print("Enemy victory.")
        elif unittwohp <= 0:
          print("Player victory.")
          lootinst = p2.loots()
          print("You found a %s!" % lootinst)
          inventory.append(lootinst)          

    else:
      print("Insufficient units.")
  else:
    print("Invalid unit.")

def inv():    #Displays the user's inventory of loot earned from [scav()] and [battle()].
  undupe = []
  print("Your inventory contains:")
  for item in inventory:
    if item not in undupe:
      count = inventory.count(item)
      print("{} x{}".format(item, count))
      undupe.append(item)
  print("")

def inspect():    #Allows the user to see a list of non-duplicate loot and read descriptions.
#########################################################################################################################################<MAX TOPLINE
  abonesdesc = """The ancient, yellowed bones of a Necropolitan Legionnaire. To hold them in their inert state, it is unfathomable how 
a foe made of such brittle old matter could prove such a profound threat."""
#######################################################################################################################<MAX SUBLINE
  rsworddesc = """A sword flaked with rust, previously wielded by a Necropolitan Legionnaire. Despite how useless it looks in your hands,
it nevertheless proves to be a deadly weapon in those of its undead bearers."""

  rrifledesc = """An old rifle, battered and weathered to apparent uselessness, formerly carried by a Necropolitan Legionnaire. 
Regardless of appearances, it certainly seemed functional in its previous owner's hands, and the many Tyranny soldiers 
cut down by such firearms prove it."""

  sclothdesc = """A swatch of translucent fabric, taken from the clothing of the Vengeful Dead. It feels like silk and cold air, and 
twists and drifts of its own accord like a ribbon in the wind."""

  whairdesc = """A lock of jet-black, water-soaked hair, sometimes carried by the Vengeful Dead as tokens of favour from their leader 
The Drowned Lover. No matter how much you attempt to dry it out, it remains saturated."""

  btalisdesc = """A small charm made from carved bone and strips of leather, taken from the remains of one of the Vengeful Dead. Its 
purpose is a complete mystery, but they appear to be of some value to those who carry them."""

  bmemdesc = """A small relic of the pre-Tyranny world, evidently carrying great sentimental value to the Vengeful Dead from which it 
was taken. Now that you hold it, you're surprised to feel a small sense of attachment to the thing, even though you 
have no idea what it is."""

  slabdesc = """A sizeable piece of strangely coloured, unpleasant-smelling flesh, harvested from the corpse of a Necropolitan 
Promethid. It continues to twitch disconcertingly, despite being entirely separated from the rest of its body."""

  promblooddesc = """A measure of viscous black fluid which appears to be climbing the walls of the vial containing it, extracted from the 
body of a Necropolitan Promethid. It smells like burning tar. Everything about it seems to discourage contact."""

  fbonesdesc = """The large, misshapen and unusually fused-together bones of a Necropolitan Promethid. Their density and hardness is 
remarkable but unsurprising, considering the absolute devastation their former owners are capable of."""

  wsutdesc = """A length of suture taken from a seam in the flesh of a Necropolitan Promethid. It twists and squirms like a living 
thing, occasionally attempting to probe the surface of your skin before withdrawing. It seems you don't meet whatever 
criteria it may be looking for -- presumably, the vulgar matter which comprised its former host's body."""

  pskulldesc = """The grossly misshapen skull of a Necropolitan Promethid. You cannot help but avoid gazing at its visage for too long --
there is a pervasive aura of malice and madness about the thing, and you feel deep discomfort just trying to fathom why
the existence of such a grotesque thing was necessary."""

  nexdesct = """A compact and deceptively heavy sphere of dark, glassy material left behind by a dispelled Deathdreg Ruiner. It is
safely contained within a heavily lined case -- the debilitating effects of exposure to the residual antilife known as
Deathdregs are all too well-documented."""

  cbladedesct = """A vicious weapon carried by a Deathdreg Ruiner. Attempting to hold it yourself would saturate you with the lingering
antilife which pervades it -- it may not really be "cursed" as such, but its debilitating effects upon the living make
the distinction negligible."""

  reyedesct = """The gem-like eye of a Deathdreg Ruiner. Unlike most other reclaimable parts of a Ruiner's remains, it is safe to handle
  -- which is not to say one would want to. Despite the superficial allure of its glinting facets and swirling, smoky
purple hues, you swear you can feel the unbridled malice of the Ruiner's wild, hateful gaze upon you."""

  nexdescn = """The compacted residual antilife of a Deathdreg Ruiner. While debilitating or outright lethal to the living, it has the 
potential to bestow immense power to the Undead -- the cost, however, is sure to be high."""

  cbladedescn = """The Deathdreg Ruiner's antilife-drenched weapon of choice. With it in your undead hands, you feel your body surge with 
might -- your mind, however, begins to cloud with intense, directionless rage, and you find yourself relinquishing your
grip for fear of losing all control. What good can such wild and unrelenting fury possibly do?"""

  reyedescn = """The crystalline physical manifestation of a Deathdreg Ruiner's amalgamated spirit, formed from the remnants of 
countless enraged, bodiless souls. You can feel its presence staring at you from within its dark, glinting surface; 
somewhere behind the wild, aimless fury, you can feel its desire to take form once again."""

  tagdesc = """A dogtag taken from a destroyed Tyranny Petrov unit, stamped with its former owner's name, rank and serial number -- to
look at it, you would be forgiven for thinking it belonged to a real person and not a synthetic parody of one."""

  gcapdesc = """An angular, brimless piece of headwear, part of the uniform for the Tyranny's low-ranked Petrov units. It's stained 
with dirt, blood and whichever other synthetic fluids fill the bodies of the Tyrant's man-machines, but despite its 
condition and its nature as the enemy's livery, there's no denying that it has a certain stylish flair about it."""

  pmachdesc = """A short, broad-bladed weapon carried by Tyranny Petrov units. It appears ideally designed for cutting through flesh and
bone. Judging by its performance in the hands of the Petrov units, it's quite good at it -- alas, the same can't be 
said for this particular weapon's previous owner."""  

  smgdesc = """An advanced sub machine gun issued to Tyranny Petrov units. As the Undead are highly resilient to all but the most 
catastrophic damage, the explosive rounds loaded into these weapons are capable of enough to keep them down -- at least
temporarily."""
  
  ardesc = """The standard issue weapon for Tyranny commandos and assault infantry. While outfitted with several high tech functions 
like adaptive ammunition, rangefinding, recoil dampening and bullet drop compensation, all of which would be invaluable
in combating the Tyranny... If only the weapon wasn't locked to some kind of electronic signature unique to their 
construction."""
  
  circdesc = """A piece of highly advanced circuitry taken from the destroyed chassis of a Tyranny Commando. While itself useless for 
any non-Tyranny application, it is still composed of valuable materials which could potentially be recycled into 
something capable of creating even more broken hardware."""
  
  weavedesc = """A piece of bullet-resistant fabric salvaged from the uniform of a fallen Tyranny Commando. The undead may not have any 
vital organs to protect, but often incorporate these scraps into their own outfits regardless. Undeath on Erebus is a 
matter of willpower; enough damage will still put one down, at least temporarily, so the reassurance of extra 
protection from firearms goes a long way."""
  
  ocapdesc = """The flat-topped peaked cap of a Tyranny officer. It's a striking piece of uniform, unmistakeably a mark of authority 
and respect -- and an equally prestigious trophy for the one who claimed it from its owner."""
  
  factdesc = """A large, complicated piece of machinery salvaged from the hulking armour of a Tyranny Siegebreaker, designed to assist 
its occupant in exerting inhuman force upon its targets. Doubtlessly it could be stripped down and used for the 
production of high quality tools and equipment, but considering the effort required to overcome a Siegebreaker in the 
first place, one would not be blamed for wanting to simply keep it as a mark of pride."""
  
  caldesc = """A large piece of ceramic alloy plating used on the external armor of Tyranny Siegebreaker units. Given the tremendous 
damage Siegebreakers are known to endure before they are bested, undamaged plates large enough to be useful are hard to
come by -- a piece like this is sure to be of great worth."""
  
  vcsdesc = """A container of slightly viscous liquid, formerly cocooned in the chassis of a Tyranny Siegebreaker. These substances 
are responsible for their inhuman might and tenacity -- and most likely for their wild, untethered brutality. Due to 
the lack of a bloodstream, they are of no use to the undead whatsoever, and are wholly unfit for use by Necropolitan 
humans. Perhaps there is some way they might be otherwise weaponized, but given their effect on Siegebreakers 
themselves, there is understandably great trepidation in testing the theory on a viable target."""
  
  sgauntdesc = """The enormous severed forearm and hand pieces from the armor of a Tyranny Siegebreaker. It stands at almost the same 
height as a person, and weighs as much as one might expect. Packed with valuable components and constructed from alloys
which the Necropolis lacks the advanced means to refine, it is sure to be of tremendous value in combating the Tyranny."""
  
  hpcabdesc = """A length of highly efficient cabling, salvaged from the internal workings of a Tyranny Siegebreaker. The high grade 
materials used to make the wiring are superior to anything the Necropolis is technologically capable of producing -- 
even the relatively small amount of cable salvageable from a single downed Siegebreaker is a veritable bounty for how 
desirable it is."""

  undupe = []
  print("Select an item to inspect:\n")
  for item in inventory:
    if item not in undupe:
      undupe.append(item)
  for item in undupe:
    print(item)
  print("")
  undupelower = [x.lower() for x in undupe]
  
  rchoice = input(" >")
  
  if rchoice.lower() in undupelower:
    #legionnaire / pile of ancient bones, rusted sword, ruined rifle
    if rchoice.lower() == "pile of ancient bones":
      print(abonesdesc)
      print(" ")
    elif rchoice.lower() == "rusted sword":
      print(rsworddesc)
      print(" ")
    elif rchoice.lower() == "ruined rifle":
      print(rrifledesc)
      print(" ")
    
    #vengeful / scrap of spectral cloth, lock of wet hair, bone talisman, beloved memento
    elif rchoice.lower() == "scrap of spectral cloth":
      print(sclothdesc)
      print(" ")
    elif rchoice.lower() == "lock of wet hair":
      print(whairdesc)
      print(" ")
    elif rchoice.lower() == "bone talisman":
      print(btalisdesc)
      print(" ")
    elif rchoice.lower() == "beloved memento":
      print(bmemdesc)
      print(" ")
    
    #promethid / slab of twitching flesh, vial of promethid blood, pile of fused bones, writhing suture, promethid skull
    elif rchoice.lower() == "slab of twitching flesh":
      print(slabdesc)
      print(" ")
    elif rchoice.lower() == "vial of promethid blood":
      print(promblooddesc)
      print(" ")
    elif rchoice.lower() == "pile of fused bones":
      print(fbonesdesc)
      print(" ")
    elif rchoice.lower() == "writhing suture":
      print(wsutdesc)
      print(" ")
    elif rchoice.lower() == "promethid skull":
      print(pskulldesc)
      print(" ")
    
    #petrov / dogtag, petrov machete, garrison cap, tyranny smg
    elif rchoice.lower() == "dogtag":
      print(tagdesc)
      print("")
    elif rchoice.lower() == "petrov machete":
      print(pmachdesc)
      print("")
    elif rchoice.lower() == "garrison cap":
      print(gcapdesc)
      print("")
    elif rchoice.lower() == "tyranny smg":
      print(smgdesc)
      print("")
    
    #commando / tyranny assault rifle, scrap circuitry, scrap of damaged ballistic weave, officer's cap
    elif rchoice.lower() == "tyranny assault rifle":
      print(ardesc)
      print("")
    elif rchoice.lower() == "scrap circuitry":
      print(circdesc)
      print("")
    elif rchoice.lower() == "scrap of damaged ballistic weave":
      print(weavedesc)
      print("")
    elif rchoice.lower() == "officer's cap":
      print(ocapdesc)
      print("")
    
    #siegebreaker / force actuator, ceramic alloy plate, vial of combat stimulants, siegebreaker gauntlet, bunch of high performance cable
    elif rchoice.lower() == "force actuator":
      print(factdesc)
      print("")
    elif rchoice.lower() == "ceramic alloy plate":
      print(caldesc)
      print("")
    elif rchoice.lower() == "vial of combat stimulants":
      print(vcsdesc)
      print("")
    elif rchoice.lower() == "siegebreaker gauntlet":
      print(sgauntdesc)
      print("")
    elif rchoice.lower() == "bunch of high-performance cable":
      print(hpcabdesc)
      print("")
    
    #deathdreg / deathdreg nexus, cursed blade, ruiner's eye
    elif rchoice.lower() == "deathdreg nexus":
      if faction == "TYRANNY":
        print(nexdesct)
        print(" ")
      elif faction == "NECROPOLIS":
        print(nexdescn)
        print(" ")
    elif rchoice.lower() == "cursed blade":
      if faction == "TYRANNY":
        print(cbladedesct)
        print(" ")
      elif faction == "NECROPOLIS":
        print(cbladedescn)
        print(" ")
    elif rchoice.lower() == "ruiner's eye":
      if faction == "TYRANNY":
        print(reyedesct)
        print(" ")
      elif faction == "NECROPOLIS":
        print(reyedescn)
        print(" ")
    
  else:
    print("Item not present in inventory.")
    print(" ")

def save(): #Allows the user to save their current faction, points, troops and inventory.
  savewarn = input("Are you sure? Any existing save file will be overwritten. [Y/N]\n >")
  if savewarn.lower() == "y":
    try:
      numsave = open("numstats.txt", "w+")
      numsave.write(str(points))
      numsave.write("\n")
      numsave.write(str(light_units))
      numsave.write("\n")
      numsave.write(str(mid_units))
      numsave.write("\n")
      numsave.write(str(heavy_units))
      numsave.write("\n")
      numsave.write(str(dd_units))
      numsave.close()
      invsave = open("inventory.txt", "w+")
      invsave.write(str(inventory))
      invsave.close()
      factionsave = open("faction.txt", "w+")
      factionsave.write(faction)
      factionsave.close()
      
      #saveinv = open("inventory.txt", "w+")
      #saveinv.write(str(inventory))
      #saveinv.close
      print("Save complete.")
      print("")
    except:
      print("Save failed.")

def load(): #Allows the user to load previously saved data.
  global faction
  global points
  global light_units
  global mid_units
  global heavy_units
  global dd_units
  global inventory
  loadwarn = input("Are you sure? Current faction, points and units will be lost. [Y/N]\n >")
  if loadwarn.lower() == "y":
    numload = open("numstats.txt", "r")
    readnum = numload.readlines()
    #print(loadlines[0])
    #print(loadlines[1])
    #print(loadlines[2])
    #print(loadlines[3])
    #print(loadlines[4])
    points = int(readnum[0])
    light_units = int(readnum[1])
    mid_units = int(readnum[2])
    heavy_units = int(readnum[3])
    dd_units = int(readnum[4])
    numload.close()
    invload = open("inventory.txt", "r")
    readinv = invload.readline()
    inventory = literal_eval(readinv)    
    invload.close()
    factionload = open("faction.txt", "r")
    readfact = factionload.readline()
    faction = readfact
    factionload.close()
    
    #loadinv = open("inventory.txt", "r")
    #loadlines = loadinv.readlines()
    #inventory = loadlines[0]
    print("Load complete.")
    print("")
    
def deploy():
  pass
    
while run == True: #The main game loop, initialised with [run] and looping until otherwise broken.

  if faction_chosen == False:
    faction_choice()

  if faction_chosen == True:
    if initial == True:
      print("For a list of commands, type 'HELP'.")
      print("")
      initial = False
      
    if set_chosen == False:
      starting_set()
      print(start_set + " selected.")
      print("")

    action_choice = input(" >")
    print("")
    if action_choice.lower() == "total":
      print(light_units + mid_units + heavy_units)
    elif action_choice.lower() == "faction":
      faction_select()
    elif action_choice.lower() == "help":
      help()
    #elif action_choice.lower() == "earn":
      #earn()
    elif action_choice.lower() == "points":
      showpoints()
    elif action_choice.lower() == "buy":
      buytroops()
    elif action_choice.lower() == "units":
      showunits()
    elif action_choice.lower() == "dispatch":
      scav()
    elif action_choice.lower() == "inventory":
      inv()
    elif action_choice.lower() == "inspect":
      inspect()
    elif action_choice.lower() == "save":
      save()
    elif action_choice.lower() == "load":
      load()
    elif action_choice.lower() == "quit":
      quit()
    elif action_choice.lower() == "battle":
      battle()
    elif action_choice.lower() == "inv2":
      print(inventory)
    elif action_choice.lower() == "deploy":
      print("Troop carriers are not functional at present.")
      #deploy()
    else:
      print("Invalid command.")
