from random import randint
import math

"""Hash out this unitlist nonsense. You gotta get the hang of classes somehow."""

run = True

initial = True

points = 0

light_units = 0

mid_units = 0

heavy_units = 0

dd_units = 0

unitlist = []

class Troop:
  #Represents a single troop unit.
  def __init__(self, fct, typ, atk, dfn, loot):
    self.fct = fct
    self.typ = typ
    self.atk = atk
    self.dfn = dfn
    self.loot = loot
    
  faction_keys = ["Tyranny", "Necropolitan"]
  troop_type = ["Infantry", "Commando", "Siegebreaker", "Legionnaire", "Vengeful", "Promethid"]
  loot_tables = [["Gun","Scrap Circuitry","Cracked Metal Plate"],["Force Actuator","Scrap Circuitry","Cracked Metal Plate","Thick Alloy Plate"],["Ancient Bones","Rusted Sword"]]
  
  
  def stats(self):
    if self.typ in range(0,6):
      return "%s %s with attack rating %s and defence rating %s." % (Troop.faction_keys[self.fct],Troop.troop_type[self.typ],self.atk,self.dfn)
    elif self.typ == 6:
      return "Necropolitan Deathdreg Ruiner with attack rating %s and defence rating %s." % (self.atk, self.dfn)
  
  def loots(self):
    return "Loot table consists of %s." % (Troop.loot_tables[self.loot])

infantry = Troop(0,0,3,2,0)
legionnaire = Troop(1,3,3,2,2)
commando = Troop(0,1,6,5,0)
vengeful = Troop(1,4,6,5,2)
siegebreaker = Troop(0,2,10,7,1)
promethid = Troop(1,5,10,7,2)
deathdreg = Troop(1,6,(randint(1,11)),randint(1,11),2)

necro_unit_names = ["legionnaire", "vengeful", "promethid"]

tyr_unit_names = ["infantry", "commando", "siegebreaker"]


"""points references: light unit = 2pts, medium unit = 5pts, heavy unit = 10pts"""

def points_gen():
  gen = randint(1, 10)
  global points
  points += gen
  return points

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

faction = ""

faction_chosen = False

def faction_choice():
  global faction
  global faction_chosen

  faction_choice = input("Choose your faction (TYRANNY or NECROPOLIS): ")
  if faction_choice.lower() == "tyranny":
    faction = "TYRANNY"
    print("You have chosen The Tyranny.")
    faction_chosen = True

  elif faction_choice.lower() == "necropolis":
    faction = "NECROPOLIS"
    print("You have chosen The Necropolis.\n ")
    faction_chosen = True

  else:
    print("Invalid faction.")

  return(faction_chosen)
  return(faction)

def action_list():
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
  
  if initial == True:
    print("For a list of commands, type 'HELP'.")
    initial = False

  action_choice = input(" >")
  
  if action_choice.lower() == "class":
    print(unitlist)

  #Earn
  if action_choice.lower() == "earn":
    gen = randint(1,10)
    bonus = randint(1, 10)
    points += gen
    if bonus == gen:
      points += bonus
      print("Resource trove uncovered!")
      print("%d points earned, plus %d bonus points." % (gen, bonus))
    else:
      print("%d points earned." % gen)
      return points

  #Show
  elif action_choice.lower() == "show":
    print("You have %d available points." % points)

  #Help
  elif action_choice.lower() == "help":
    print("Available actions: \n#[EARN] points \n#[BUY] units \n#[SHOW] points \n#show [UNITS] in reserve \n#change [FACTION] \n#[DISPATCH] units to procure resources \n#[QUIT] game")

  #Buy
  elif action_choice.lower() == "buy":

    if faction.lower() == "tyranny": #faction == tyranny
      type_choice = input("Choose a unit type to produce: [INFANTRY]: 2pts, [COMMANDO]: 5pts, [SIEGEBREAKER]: 10pts\n >")

      if type_choice.lower() == "infantry":
        mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 2, 0)))
        cost = (mult * 2)

        if cost > points:
          print("Insufficient points.")

        else:
          points -= cost
          light_units += mult
          print("Produced %d INFANTRY units." % mult)

      elif type_choice.lower() == "commando":
        mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 5, 0)))
        cost = (mult * 5)

        if cost > points:
          print("Insufficient points.")

        else:
          points -= cost
          mid_units += mult
          print("Produced %d COMMANDO units." % mult)

      elif type_choice.lower() == "siegebreaker":
        mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 10, 0)))
        cost = (mult * 10)

        if cost > points:
          print("Insufficient points.")

        else:
          points -= cost
          heavy_units += mult
          print("Produced %d SIEGEBREAKER units." % mult)

      else:
	      print("Unit type not found.")

    else: # faction == necropolis
      type_choice = input("Choose an undead type to raise: [LEGIONNAIRE]: 2pts, [VENGEFUL]: 5pts, [PROMETHID]: 10pts\n >")

      if type_choice.lower() == "legionnaire":
        mult = int(input("Enter a number of undead to raise (max available = %d): \n >" % round_down(points / 2, 0)))
        cost = (mult * 2)

        if cost > points:
          print("Insufficient points.")

        else:
          points -= cost
          light_units += mult
          print("Produced %d LEGIONNAIRE undead." % mult)
          unitlist.append(legionnaire)
          

      elif type_choice.lower() == "vengeful":
        mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 5, 0)))
        cost = (mult * 5)

        if cost > points:
          print("Insufficient points.")

        else:
          points -= cost
          mid_units += mult
          print("Produced %d VENGEFUL undead." % mult)

      elif type_choice.lower() == "promethid":
        mult = int(input("Enter a number of units to produce (max available = %d): \n >" % round_down(points / 10, 0)))
        cost = (mult * 10)

        if cost > points:
          print("Insufficient points.")

        else:
          points -= cost
          heavy_units += mult
          print("Produced %d PROMETHID undead." % mult)

      else:
	      print("Undead class not found.")

  elif action_choice.lower() == "faction":
    faction_switch = input("Are you sure? All currently held points and units will be lost. [YES/NO] ")

    if faction_switch.lower() == "yes":
      faction_chosen = False
      initial = True
      light_units = 0
      mid_units = 0
      heavy_units = 0
      points = 0

  elif action_choice.lower() == "units":
    print("Light units: %d" % light_units) #print("s%: %d" % (faction_light,light_units))
    print("Medium units: %d" % mid_units)
    print("Heavy units: %d" % heavy_units)
    if dd_units >= 1:
      print("Deathdreg Revenant units: %d" % dd_units)

  elif action_choice.lower() == "quit":
    quit()
	
  elif action_choice.lower() == "dispatch":
    scav_duration = int(input("Choose a dispatch order duration. (max. 7 days) \n >"))
    if scav_duration <= 7:
      scav_turns = 1
      if scav_turns <= scav_duration:
        if faction == "NECROPOLIS": #faction: Necropolis
          dispatch_type = input("Choose a unit type to dispatch.\n >")
          if dispatch_type.lower() in necro_unit_names:
            assigned_units = int(input("Choose a number of units to dispatch.\n >"))
            if dispatch_type.lower() == "legionnaire" and assigned_units <= light_units: #dispatched legionnaires
              while scav_turns <= scav_duration:
                event = randint(1, 100) #event roll
                #event = 75
                print(event)
                if event == 1: #heavy losses
                  print("Day %s: Your %s team has run afoul of a natural disaster and suffered heavy losses. %d units lost." % (scav_turns, dispatch_type.lower(), (assigned_units/2)))
                  light_units / 2
                  scav_turns += 1
                  
                elif event in range(2,11): #intercept cache escort
                  print("Day %s: Your %s team has intercepted a small cache of resources being transported by a small enemy squad." % (scav_turns, dispatch_type.lower()))
                  outcome = randint(1, 5)
                  if outcome == 1: #repelled, one loss
                    print("Your unit did not fare well in the conflict. You were driven off, failing to claim the resources and losing 1 %s in the process." % dispatch_type.lower())
                    light_units -= 1
                  elif outcome in range(2, 5): #victory, damaged cache
                    print("Your unit successfully neutralised the enemy squad, but the resource cache was damaged in the conflict.")
                    print("+5 points.")
                    points += 5
                  elif outcome == 5: #victory, intact cache
                    print("Your unit took the enemy by surprise, achieving a flawless victory and securing the resource cache.")
                    print("+10 points.")
                    points += 10
                  scav_turns += 1

                elif event in range(11,31): #empty-handed
                  print("Day %s: Your unit has nothing to show for the day but covered ground." % scav_turns)
                  scav_turns += 1

                elif event in range(31,50): #tyranny troop remains
                  print("Day %s: Your %s team find the scattered remains of a Tyranny patrol." % (scav_turns, dispatch_type.lower()))
                  if event in range(31, 35): #survivor camp
                    print("The trail leads to a small encampment of the patrol's survivors.") 
                    if event in range(31, 33): #survivors flee
                      print("The survivors don't like their odds, and flee before your team can engage.")
                    if event == 33: #survivors resist
                      print("The survivors were too well-prepared and fend you off, killing 1 %s in the process." % dispatch_type.lower())
                      light_units -= 1
                    if event == 34: #survivors finished
                      print("The survivors are too devastated by their previous loss, and crumble under your assault. You recover a small cache of supplies. +5 points.")
                      points += 5
                  if event in range(35, 40): #deathdreg field
                    print("The trail leads to an area choked with antilife; at its centre, an idling Deathdreg Revenant.")
                    if event in range(35, 38): #revenant follows
                      print("The Revenant appears to recognize your team's state of undeath and decides to follow them.")
                      dd_units += 1
                    if event in range(38, 40): #revenant attacks
                      print("The Revenant is beyond sanity, and attacks. In putting it to rest, you lose 1 %s." % dispatch_type.lower())
                      light_units -= 1
                  if event in range(40, 45): #cold trail
                    print("The trail runs cold. Whoever killed those troops, they're long gone. Good on them.")
                  if event in range(45, 50): #deathseeker
                    print("You find a recently returned Deathseeker, evidently killed sometime during their scuffle with the troops -- albeit not before giving as good as they got. They decline to join your squad, but gladly hand over a cut of their spoils. +5 points.")
                    points += 5
                  scav_turns += 1

                elif event in range(50,80): #enemy ambush
                  print("Day %s: Your %s team is ambushed by a squad of Tyranny Commandos." % (scav_turns, dispatch_type.lower()))
                  if event in range(50,60): #heavy losses
                    print("You manage to fight them off, but not without heavy losses. %d units lost." % (assigned_units/2))
                    light_units / 2
                  
                  if event in range(60,70): #flawless victory
                    print("Your team crushes the ambush with ease and spend the rest of the day basking in the glory of their victory. +10 points.")
                    points += 10
                    
                  if event in range(70,80): #annihilated
                    print("Your team is annihilated by the ruthless assault, fated never to return.")
                    scav_turns += ((scav_duration - scav_turns) + 1)
                    light_units -= assigned_units
                  scav_turns += 1
                  
                elif event in range(80,90): #petrov corpse
                  print("Day %s: Your %s team finds the weathered remains of a long-since ruined Tyranny Petrov unit." % (scav_turns, dispatch_type.lower()))
                  print("Despite just being another heap of broken hardware, somehow it's a rather mournful scene.")
                  points -= 1
                  scav_turns += 1

                elif event in range(90,100): #claimed unguarded cache
                  print("Day %s: Your %s team has located and secured an unguarded cache of resources. Points +25." % (scav_turns, dispatch_type.lower()))
                  points += 25
                  scav_turns += 1
                
                elif event == 100: #the warrior
                  print("The Warrior graces your squad of Legionnaires with his presence. Under his leadership, they will be nigh unstoppable.")
                
              else:
                print("Dispatch complete.")

            elif dispatch_type.lower() == "vengeful" and assigned_units <= mid_units: #dispatched vengeful
              while scav_turns <= scav_duration:
                event = randint(1, 100) #event roll
                #event = 75
                print(event)
                if event == 1: #heavy losses
                  print("Day %s: Your %s team has run afoul of a natural disaster and suffered heavy losses. %d units lost." % (scav_turns, dispatch_type.lower(), (assigned_units/2)))
                  mid_units / 2
                  scav_turns += 1
                  
                elif event in range(2,11): #intercept cache escort
                  print("Day %s: Your %s team has intercepted a small cache of resources being transported by a small enemy squad." % (scav_turns, dispatch_type.lower()))
                  outcome = randint(1, 5)
                  if outcome == 1: #repelled, one loss
                    print("Your unit did not fare well in the conflict. You were driven off, failing to claim the resources and losing 1 %s in the process." % dispatch_type.lower())
                    mid_units -= 1
                  elif outcome in range(2, 5): #victory, damaged cache
                    print("Your unit successfully neutralised the enemy squad, but the resource cache was damaged in the conflict.")
                    print("+5 points.")
                    points += 5
                  elif outcome == 5: #victory, intact cache
                    print("Your unit took the enemy by surprise, achieving a flawless victory and securing the resource cache.")
                    print("+10 points.")
                    points += 10
                  scav_turns += 1

                elif event in range(11,31): #empty-handed
                  print("Day %s: Your unit has nothing to show for the day but covered ground." % scav_turns)
                  scav_turns += 1

                elif event in range(31,50): #tyranny troop remains
                  print("Day %s: Your %s team find the scattered remains of a Tyranny patrol." % (scav_turns, dispatch_type.lower()))
                  if event in range(31, 35): #survivor camp
                    print("The trail leads to a small encampment of the patrol's survivors.") 
                    if event in range(31, 33): #survivors flee
                      print("The survivors don't like their odds, and flee before your team can engage.")
                    if event == 33: #survivors resist
                      print("The survivors were too well-prepared and fend you off, killing 1 %s in the process." % dispatch_type.lower())
                      mid_units -= 1
                    if event == 34: #survivors finished
                      print("The survivors are too devastated by their previous loss, and crumble under your assault. You recover a small cache of supplies. +5 points.")
                      points += 5
                  if event in range(35, 40): #deathdreg field
                    print("The trail leads to an area choked with antilife; at its centre, an idling Deathdreg Revenant.")
                    if event in range(35, 38): #revenant follows
                      print("The Revenant appears to recognize your team's state of undeath and decides to follow them.")
                      dd_units += 1
                    if event in range(38, 40): #revenant attacks
                      print("The Revenant is beyond sanity, and attacks. In putting it to rest, you lose 1 %s." % dispatch_type.lower)
                      mid_units -= 1
                  if event in range(40, 45): #cold trail
                    print("The trail runs cold. Whoever killed those troops, they're long gone. Good on them.")
                  if event in range(45, 50): #deathseeker
                    print("You find a recently returned Deathseeker, evidently killed sometime during their scuffle with the troops -- albeit not before giving as good as they got. They decline to join your squad, but gladly hand over a cut of their spoils. +5 points.")
                    points += 5
                  scav_turns += 1

                elif event in range(50,80): #enemy ambush
                  print("Day %s: Your %s team is ambushed by a squad of Tyranny Commandos." % (scav_turns, dispatch_type.lower()))
                  if event in range(50,60): #heavy losses
                    print("You manage to fight them off, but not without heavy losses. %d units lost." % (assigned_units/2))
                    mid_units / 2
                  
                  if event in range(60,70): #flawless victory
                    print("Your team crushes the ambush with ease and spend the rest of the day basking in the glory of their victory. +10 points.")
                    points += 10
                    
                  if event in range(70,80): #annihilated
                    print("Your team is annihilated by the ruthless assault, fated never to return.")
                    scav_turns += ((scav_duration - scav_turns) + 1)
                    mid_units -= assigned_units
                  scav_turns += 1
                  
                elif event in range(80,90): #petrov corpse
                  print("Day %s: Your %s team finds the weathered remains of a long-since ruined Tyranny Petrov unit." % (scav_turns, dispatch_type.lower()))
                  print("Despite just being another heap of broken hardware, somehow it's a rather mournful scene.")
                  points -= 1
                  scav_turns += 1

                elif event in range(90,100): #claimed unguarded cache
                  print("Day %s: Your %s team has located and secured an unguarded cache of resources. Points +25." % (scav_turns, dispatch_type.lower()))
                  points += 25
                  scav_turns += 1
                
                elif event == 100: #the warrior
                  print("The Warrior graces your squad of Legionnaires with his presence. Under his leadership, they will be nigh unstoppable.")
                
              else:
                print("Dispatch complete.")
        
            elif dispatch_type.lower() == "promethid" and assigned_units <= heavy_units: #dispatched promethids
              while scav_turns <= scav_duration:
                event = randint(1, 100) #event roll
                #event = 75
                print(event)
                if event == 1: #heavy losses
                  print("Day %s: Your %s team has run afoul of a natural disaster and suffered heavy losses. %d units lost." % (scav_turns, dispatch_type.lower(), (assigned_units/2)))
                  heavy_units / 2
                  scav_turns += 1
                  
                elif event in range(2,11): #intercept cache escort
                  print("Day %s: Your %s team has intercepted a small cache of resources being transported by a small enemy squad." % (scav_turns, dispatch_type.lower()))
                  outcome = randint(1, 5)
                  if outcome == 1: #repelled, one loss
                    print("Your unit did not fare well in the conflict. You were driven off, failing to claim the resources and losing 1 %s in the process." % dispatch_type.lower())
                    heavy_units -= 1
                  elif outcome in range(2, 5): #victory, damaged cache
                    print("Your unit successfully neutralised the enemy squad, but the resource cache was damaged in the conflict.")
                    print("+5 points.")
                    points += 5
                  elif outcome == 5: #victory, intact cache
                    print("Your unit took the enemy by surprise, achieving a flawless victory and securing the resource cache.")
                    print("+10 points.")
                    points += 10
                  scav_turns += 1

                elif event in range(11,31): #empty-handed
                  print("Day %s: Your unit has nothing to show for the day but covered ground." % scav_turns)
                  scav_turns += 1

                elif event in range(31,50): #tyranny troop remains
                  print("Day %s: Your %s team find the scattered remains of a Tyranny patrol." % (scav_turns, dispatch_type.lower()))
                  if event in range(31, 35): #survivor camp
                    print("The trail leads to a small encampment of the patrol's survivors.") 
                    if event in range(31, 33): #survivors flee
                      print("The survivors don't like their odds, and flee before your team can engage.")
                    if event == 33: #survivors resist
                      print("The survivors were too well-prepared and fend you off, killing 1 %s in the process." % dispatch_type.lower())
                      heavy_units -= 1
                    if event == 34: #survivors finished
                      print("The survivors are too devastated by their previous loss, and crumble under your assault. You recover a small cache of supplies. +5 points.")
                      points += 5
                  if event in range(35, 40): #deathdreg field
                    print("The trail leads to an area choked with antilife; at its centre, an idling Deathdreg Revenant.")
                    if event in range(35, 38): #revenant follows
                      print("The Revenant appears to recognize your team's state of undeath and decides to follow them.")
                      dd_units += 1
                    if event in range(38, 40): #revenant attacks
                      print("The Revenant is beyond sanity, and attacks. In putting it to rest, you lose 1 %s." % dispatch_type.lower)
                      heavy_units -= 1
                  if event in range(40, 45): #cold trail
                    print("The trail runs cold. Whoever killed those troops, they're long gone. Good on them.")
                  if event in range(45, 50): #deathseeker
                    print("You find a recently returned Deathseeker, evidently killed sometime during their scuffle with the troops -- albeit not before giving as good as they got. They decline to join your squad, but gladly hand over a cut of their spoils. +5 points.")
                    points += 5
                  scav_turns += 1

                elif event in range(50,80): #enemy ambush
                  print("Day %s: Your %s team is ambushed by a squad of Tyranny Commandos." % (scav_turns, dispatch_type.lower()))
                  if event in range(50,60): #heavy losses
                    print("You manage to fight them off, but not without heavy losses. %d units lost." % (assigned_units/2))
                    heavy_units / 2
                  
                  if event in range(60,70): #flawless victory
                    print("Your team crushes the ambush with ease and spend the rest of the day basking in the glory of their victory. +10 points.")
                    points += 10
                    
                  if event in range(70,80): #annihilated
                    print("Your team is annihilated by the ruthless assault, fated never to return.")
                    scav_turns += ((scav_duration - scav_turns) + 1)
                    heavy_units -= assigned_units
                  scav_turns += 1
                  
                elif event in range(80,90): #petrov corpse
                  print("Day %s: Your %s team finds the weathered remains of a long-since ruined Tyranny Petrov unit." % (scav_turns, dispatch_type.lower()))
                  print("Despite just being another heap of broken hardware, somehow it's a rather mournful scene.")
                  points -= 1
                  scav_turns += 1

                elif event in range(90,100): #claimed unguarded cache
                  print("Day %s: Your %s team has located and secured an unguarded cache of resources. Points +25." % (scav_turns, dispatch_type.lower()))
                  points += 25
                  scav_turns += 1
                
                elif event == 100: #the warrior
                  print("The Warrior graces your squad of Legionnaires with his presence. Under his leadership, they will be nigh unstoppable.")
                
              else:
                print("Dispatch complete.")


            else:
              print("Insufficient units in reserve.")

          else:
            print("Unit type not found.")

        else: #faction: Tyranny
          dispatch_type = input("Choose a unit type to dispatch.\n >")
          if dispatch_type.upper() in tyr_unit_names:
            assigned_units = int(input("Choose a number of units to dispatch.\n >"))
            if dispatch_type.lower() == "infantry" and assigned_units <= light_units: #dispatched infantry
              event = randint(1, 100) #event roll
              if event == 1: #heavy losses
                print("Your %s team has run afoul of a natural disaster and suffered heavy losses. %d units lost." % (dispatch_type.lower(), (assigned_units/2)))
      
              elif event in range(2,11): #intercept cache escort
                print("Your %s team has intercepted a small cache of resources being transported by a small enemy squad." % dispatch_type.lower())
                outcome = randint(1, 5)
                if outcome == 1: #repelled, one loss
                  print("Your unit did not fare well in the conflict. You were driven off, failing to claim the resources and losing 1 %s in the process." % dispatch_type.lower())
                  light_units -= 1
                elif outcome in range(2, 5): #victory, damaged cache
                  print("Your unit successfully neutralised the enemy squad, but the resource cache was damaged in the conflict.")
                  print("+5 points.")
                  points += 5
                elif outcome == 5: #victory, intact cache
                  print("Your unit took the enemy by surprise, achieving a flawless victory and securing the resource cache.")
                  print("+10 points.")
                  points += 10

              elif event in range(11,31): #empty-handed
                print("Your unit returned empty-handed.")

              elif event in range(31,50): #test1
                print("test1")

              elif event in range(50,90): #test2
                print("test2")

              elif event in range(90,100): #claimed unguarded cache
                print("Your %s team has located and secured an unguarded cache of resources. Points +25." % dispatch_type.lower())
                points += 25

            elif dispatch_type.lower() == "commando" and assigned_units <= mid_units: #dispatched commandos
              event = randint(1, 100)
              if event == 1:
                print("Your %s team has run afoul of a natural disaster and suffered heavy losses. %d units lost." % (dispatch_type.lower(), (assigned_units/2)))
      
              elif event in range(2,11):
                print("Your %s team has intercepted a small cache of resources being transported by a small enemy squad." % dispatch_type.lower())
                outcome = randint(1, 5)
                if outcome == 1:
                  print("Your unit did not fare well in the conflict. You were driven off, failing to claim the resources and losing 1 %s in the process." % dispatch_type.lower())
                  mid_units -= 1
                elif outcome in range(2, 5):
                  print("Your unit successfully neutralised the enemy squad, but the resource cache was damaged in the conflict.")
                  print("+5 points.")
                  points += 5
                elif outcome == 5:
                  print("Your unit took the enemy by surprise, achieving a flawless victory and securing the resource cache.")
                  print("+10 points.")
                  points += 10

              elif event in range(11,31):
                print("Your unit returned empty-handed.")

              elif event in range(31,50):
                print("test1")

              elif event in range(50,90):
                print("test2")

              elif event in range(90,100):
                print("Your %s team has located and secured an unguarded cache of resources. Points +25." % dispatch_type.lower())
                points += 25
        
            elif dispatch_type.lower() == "siegebreaker" and assigned_units <= heavy_units: #dispatched siegebreakers
              event = randint(1, 100)
              if event == 1:
                print("Your %s team has run afoul of a natural disaster and suffered heavy losses. %d units lost." % (dispatch_type.lower(), (assigned_units/2)))
      
              elif event in range(2,11):
                print("Your %s team has intercepted a small cache of resources being transported by a small enemy squad." % dispatch_type.lower())
                outcome = randint(1, 5)
                if outcome == 1:
                  print("Your unit did not fare well in the conflict. You were driven off, failing to claim the resources and losing 1 %s in the process." % dispatch_type.lower())
                  heavy_units -= 1
                elif outcome in range(2, 5):
                  print("Your unit successfully neutralised the enemy squad, but the resource cache was damaged in the conflict.")
                  print("+5 points.")
                  points += 5
                elif outcome == 5:
                  print("Your unit took the enemy by surprise, achieving a flawless victory and securing the resource cache.")
                  print("+10 points.")
                  points += 10

              elif event in range(11,31):
                print("Your unit returned empty-handed.")

              elif event in range(31,50):
                print("test1")

              elif event in range(50,90):
                print("test2")

              elif event in range(90,100):
                print("Your %s team has located and secured an unguarded cache of resources. Points +25." % dispatch_type.lower())
                points += 25

              else: #insufficient units
                print("Insufficient units in reserve.")

            else: #invalid unit
              print("Unit type not found.")    

    else: #dispatch > 7
      print("Teams cannot be dispatched for longer than 7 days.")
  else: #invalid cmd
    print("Unrecognised command.")
    
def scav_loop():
  counter = 0
  

while run == True:

  if faction_chosen == False:
    faction_choice()

  else:
    action_list()
