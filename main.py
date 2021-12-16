from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

#Create black magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 12, 140, "black")

#Create white magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

#Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 500 HP", 500)
superpotion = Item("Super-Potion", "potion", "Heals 150 HP", 150)
elixer = Item("Elixer", "elixer", "Fully recover HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores HP/MP of one party member", 9999)

grenade = Item("Grenade", "attack", "deals 500 damage", 500)


player_spells = [fire, thunder, meteor, cure, cura]
enemy_spells = [fire, thunder, cure]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2},
                {"item": grenade, "quantity": 2}]
#Instantiate players

player1 = Person("Vals:", 460, 100, 60, 34, player_spells, player_items)
player2 = Person("Chax:", 460, 100, 60, 34, player_spells, player_items)
player3 = Person("Povy:", 460, 100, 60, 34, player_spells, player_items)

enemy1 = Person("Magus:", 1200, 65, 65, 25, enemy_spells, [])
enemy2 = Person("Zatz: ", 1000, 20, 100, 10, enemy_spells, [])
enemy3 = Person("Omeg: ", 1000, 20, 50, 10, enemy_spells, [])

defeated_players = 0
defeated_enemies = 0

players = [player1, player2, player3 ]
enemies = [enemy1, enemy2, enemy3 ]

running = True

print(bcolors.FAIL + bcolors.BOLD + "ATTACKS 4 IL'H'AM!" + bcolors.ENDC)
print( "••••••••••" )
print( "-----~~ Game starts ~~------" )
#print( "Enemy HP:", bcolors.FAIL + str( enemy.get_hp() ) + "/" + str( enemy.get_max_hp() ) +"\n" + bcolors.ENDC )
#print( "Your HP:", bcolors.OKGREEN + str( player.get_hp() ) + "/" + str( player.get_max_hp() ) + bcolors.ENDC )

while running:
    print("NAME               HP                                       MP")
    for player in players :
        player.get_stats()
    print("\n\n")
    for enemy in enemies:
        enemy.get_enemy_stats()
    for player in players :
        print("\n")
        player.choose_action()
        choice = input("Choose action:")
        index = int(choice) -1

        if index == 0 :
            dmg = player.generate_damage()
            enemy_index = player.choose_target(enemies)
            enemies[enemy_index].take_damage(dmg)
            print("attacked " + enemies[enemy_index].name + "for: ",dmg, "points of damage. Enemy HP:", enemy.get_hp())
            if enemies[enemy_index].get_hp() <= 0:
                print(enemies[enemy_index].name + " has died!")
                del enemies[enemy_index]
        elif index == 1 :
            player.choose_magic()
            magic_choice = int(input("Choose magic:")) - 1

            if magic_choice == -1 :
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()
            cost = spell.cost
            if spell.cost > current_mp:
                print(bcolors.FAIL +"\nNOT enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(cost)

            if spell.type == 'white' :
                player.heal(magic_dmg)
                print(bcolors.OKCYAN + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == 'black' :
                enemy_index = player.choose_target(enemies)
                enemies[enemy_index].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " on "+ enemies[enemy_index].name + " deals", str(magic_dmg), " Points of damage" + bcolors.ENDC)
                if enemies[enemy_index].get_hp() == 0:
                    print(enemies[enemy_index].name + " has died!")
                    del enemies[enemy_index]
        elif index == 2 :
            player.choose_item()
            item_choice = int(input("Choose Item: ")) - 1

            if item_choice == -1 :
                continue

            item = player.items[item_choice]["item"]
            if (player.items[item_choice]["quantity"]) == 0:
                print(bcolors.FAIL +"\n" + "None lef..."+ bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion" :
                player.heal(item.prop)
                print(bcolors.OKBLUE + "\n" + item.name + " heals", str( item.prop ), "HP" + bcolors.ENDC)
            elif item.type == "elixer" :
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKBLUE + "\n" + item.name + " fully restores HP/MP " + bcolors.ENDC)
            elif item.name == "MegaElixer" :
                for plr in players :
                    plr.hp = plr.maxhp
                    plr.mp = plr.maxmp
                    print(bcolors.OKBLUE + "\n" + item.name + " fully restores HP/MP " + bcolors.ENDC)
            elif item.type == "attack":
                enemy_index = player.choose_target(enemies)
                enemies[enemy_index].take_damage(item.prop)
                print( bcolors.FAIL + "\n" + item.name +" on " + enemies[enemy_index].name +" deals", str(item.prop), "points of damage" + bcolors.ENDC )
                if enemies[enemy_index].get_hp() == 0:
                    print(enemies[enemy_index].name + " has died!")
                    del enemies[enemy_index]
            if player.get_hp() == 0:
                defeated_players += 1

    if defeated_players == len(players) :
        print(bcolors.FAIL +"Enemies win" + bcolors.ENDC)
        running = False
    print("\n\n")


    import random
    player = players[random.randint(0,2)]

    print( "------------------" )

    for enemy in enemies :
        enemy_choice = random.randint(0,1)
        print("enemy_choice ",enemy_choice )

        if enemy_choice == 0 :
            enemy_dmg = enemy.generate_damage()
            player.take_damage(enemy_dmg)
            print( enemy.name.replace(":","") + " attacked ", player.name.replace(":",""), " for ", enemy_dmg)
        elif enemy_choice == 1 :
            try :
                spell, magic_dmg = enemy.choose_enemy_spell()
                enemy.reduce_mp(spell.cost)

                if spell.type == 'white':
                    enemy.heal(magic_dmg)
                    print(bcolors.OKCYAN + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
                elif spell.type == 'black' :
                    m = random.randint(0,2)
                    player = players[m]
                    player.take_damage(magic_dmg)
                    print(bcolors.OKBLUE + enemy.name.replace(":","") + " applied " + spell.name + " on "+ player.name.replace(":","") + " deals", str(magic_dmg), " Points of damage" + bcolors.ENDC)
            except :
                TypeError

                if player.get_hp() == 0:
                    print(player.name + " has died!")
                    del player
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == len(enemies) :
        print(bcolors.OKGREEN +"You win" + bcolors.ENDC)
        running = False