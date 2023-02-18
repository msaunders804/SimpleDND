# Application to simplify play with high level characters
import tkinter as tk
from tkinter import *
import sqlite3
import dill
from tkinter import ttk
from Classes import *

Menu = Tk()

char_dict = {}

class Character:
    def __init__(self, name='name', race='Human', char_class='Barbarian', subclass="Path of The Zealot", background='Solider', level=1, str_=15,
                 dex_=15, con_=15, wis_=15, intell_=15, cha_=15):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.subclass = subclass
        self.background = background
        self.level = level
        self.str_ = str_
        self.dex_ = dex_
        self.con_ = con_
        self.intell_ = intell_
        self.wis_ = wis_
        self.cha_ = cha_
        self.str_mod = self.dex_mod = self.con_mod = self.intell_mod = self.wis_mod = self.cha_mod = 1
        self.initiative = 0
        self.HP = 0
        self.proficiency = 0
        self.AC = 0
        self.speed = 30
        self.current_HP = 0

# Functions and design related to the character creation page (Includes: Update_Score_Options, Subclass, Create_Character_Object, Set_Modifiers, Submit)
def NewChar():
    # Accept input and push to DB
    NewCharPage = Toplevel(Menu)
    NewCharPage.geometry("1500x1500")
    NewCharPage.configure(bg="black")
    Label(NewCharPage, text="Enter Character information below:", bg="black", fg="red", font=("roman", 25)).grid(row=0,
                                                                                                                 column=1)

    Level_options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    levelVar = IntVar(NewCharPage)
    levelVar.set(Level_options[0])

    char_class_options = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue",
                          "Sorcerer", "Warlock", "Wizard", "Artificer", "Blood Hunter"]
    classVar = StringVar(NewCharPage)
    classVar.set(char_class_options[0])
    char_subclass_options = ["Not High Enough Level"]
    subclassVar = StringVar(NewCharPage)
    subclassVar.set(char_subclass_options[0])

    race_options = ["Dragonborne", "Dwarf", "Elf", "Gnome", "Half-elf", "Halfling", "Half-Orc", "Human", "Tiefling",
                    "Leonin",
                    "Satyr", "Owlin", "Aarakorcra", "Aasimar", "Air Genasi", "Bugbear", "Centuar", "Changeling",
                    "Duergar", "Earth Genasi", "Elasrin", "Fairy", "Firbolg", "Fire Genasi", "Githyanki", "Githzerai",
                    "Goblin",
                    "Goliath", "Harengon", "Tabaxi", "Triton", "Water Genasi", "Warforged", "Plasmoid"]
    raceVar = StringVar(NewCharPage)
    raceVar.set(race_options[0])

    statTypeVar = StringVar(NewCharPage)
    stat_type_options = ["Standard Array", "Roll", "Point Buy"]
    statTypeVar.set(stat_type_options[1])
    stdarr_stats_options = [15, 14, 13, 12, 10, 8]
    stat_options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    strstatVar = IntVar(NewCharPage)
    constatVar = IntVar(NewCharPage)
    dexstatVar = IntVar(NewCharPage)
    intstatVar = IntVar(NewCharPage)
    wisstatVar = IntVar(NewCharPage)
    chastatVar = IntVar(NewCharPage)
    strstatVar.set(stdarr_stats_options[0])
    constatVar.set(stdarr_stats_options[0])
    dexstatVar.set(stdarr_stats_options[0])
    intstatVar.set(stdarr_stats_options[0])
    wisstatVar.set(stdarr_stats_options[0])
    chastatVar.set(stdarr_stats_options[0])

    # Updated Stat score options based on Std array, roll or point buy
    def Update_Score_Options(selection):
        if statTypeVar.get() == "Standard Array":
            strstatVar.set('')
            constatVar.set('')
            dexstatVar.set('')
            intstatVar.set('')
            wisstatVar.set('')
            chastatVar.set('')

            str['menu'].delete(0, 'end')
            con['menu'].delete(0, 'end')
            dex['menu'].delete(0, 'end')
            intell['menu'].delete(0, 'end')
            wis['menu'].delete(0, 'end')
            cha['menu'].delete(0, 'end')

            stat_options = stdarr_stats_options

            for x in stat_options:
                str['menu'].add_command(label=x, command=tk._setit(strstatVar, x))
                con['menu'].add_command(label=x, command=tk._setit(constatVar, x))
                dex['menu'].add_command(label=x, command=tk._setit(dexstatVar, x))
                wis['menu'].add_command(label=x, command=tk._setit(wisstatVar, x))
                intell['menu'].add_command(label=x, command=tk._setit(intstatVar, x))
                cha['menu'].add_command(label=x, command=tk._setit(chastatVar, x))

            strstatVar.set(stat_options[0])
            constatVar.set(stat_options[0])
            dexstatVar.set(stat_options[0])
            intstatVar.set(stat_options[0])
            wisstatVar.set(stat_options[0])
            chastatVar.set(stat_options[0])
        else:
            strstatVar.set('')
            constatVar.set('')
            dexstatVar.set('')
            intstatVar.set('')
            wisstatVar.set('')
            chastatVar.set('')

            str['menu'].delete(0, 'end')
            con['menu'].delete(0, 'end')
            dex['menu'].delete(0, 'end')
            intell['menu'].delete(0, 'end')
            wis['menu'].delete(0, 'end')
            cha['menu'].delete(0, 'end')

            stat_options = Level_options

            for x in stat_options:
                str['menu'].add_command(label=x, command=tk._setit(strstatVar, x))
                con['menu'].add_command(label=x, command=tk._setit(constatVar, x))
                dex['menu'].add_command(label=x, command=tk._setit(dexstatVar, x))
                wis['menu'].add_command(label=x, command=tk._setit(wisstatVar, x))
                intell['menu'].add_command(label=x, command=tk._setit(intstatVar, x))
                cha['menu'].add_command(label=x, command=tk._setit(chastatVar, x))

            strstatVar.set(stat_options[0])
            constatVar.set(stat_options[0])
            dexstatVar.set(stat_options[0])
            intstatVar.set(stat_options[0])
            wisstatVar.set(stat_options[0])
            chastatVar.set(stat_options[0])

    # Creates dropdowns for subclass options based on class choice
    def subclass(selection):
        # Update subclass options based on class selection
        if levelVar.get() >= 3:
            if classVar.get() == "Barbarian":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Path of The Berserker", "Path of The Zealot", "Path of the Battlerager"
                    , "Path of The Beast", "Path of The Storm Herald", "Path of The Ancestral Guardian",
                                         "Path of Wild Magic"
                    , "Path of The Totem Warrior"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Bard":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["College of Swords", "College of Spirits", "College of Eloquence",
                                         "College of Creation",
                                         "College of The Epic Saga", "College of Whispers", "College of Glamour",
                                         "College of Valor", "College of Lore"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Cleric":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Nature Domain", "Knowledge Domain", "Grave Domain", "Death Domain",
                                         "Twilight Domain",
                                         "Trickery Domain", "Forge Domain", "Life Domain", "Tempest Domain",
                                         "Light Domain",
                                         "Peace Domain", "Arcana Domain", "Order Domain", "War Domain"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Druid":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Circle of Spores", "Circle of Dreams", "Circle of Moon", "Circle of Land",
                                         "Circle of Stars", "Circle of Wildfire", "Circle of Shephard"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Fighter":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Psi Warrior", "Purple Knight Dragon", "Echo Knight",
                                         "Rune Knight", "Cavalier", "Arcane Archer", "Samurai", "Gunslinger",
                                         "Eldritch Knight",
                                         "Battle Master", "Champion"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Monk":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Way of The Astral Self", "Way of Mercy", "Way of The Ascendant Dragon",
                                         "Way of The Sun Soul", "Way of The Kensei", "Way of The Four Elements",
                                         "Way of The Shadow", "Way of The Open Hand", "Way of The Long Death",
                                         "Way of The Drunken Master"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Paladin":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Oath of The Crown","Oath of Devotion","Oath of Glory","Oath of Conquest",
                                         "Oath of The Open Sea","Oath of The Watchers","Oath of The Ancients",
                                         "Oathbreaker","Oath of Redemption","Oath of Vengeance"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Ranger":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Hunter Conclave","Beast Master Conclave","Fey Wanderer Conclave",
                                         "Drakewarden Conclave","Monster Slayer Conclave", "Gloom Stalker Conclave",
                                         "Swarm Keeper Conclave", "Horizon Walker Conclave"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Rogue":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Mastermind","Inquisitive","Swashbuckler","Scout","Phantom","Arcane Trickster",
                                         "Assassin","Soul Knife","Thief"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Sorcerer":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Wild Magic","Storm","Lunar","Divine Soul","Clockwork Soul",
                                         "Draconic Bloodline","Aberrant Mind","Shadow Magic"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Wizard":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["School of Transmutation","School of Enchantment","School of Abjuration",
                                         "School of War Magic","School of Divination","School of Conjuration",
                                         "School of Necromancy","School of Illusion","School of Bladesinging",
                                         "Order of the Scribes","School of Evocation"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Warlock":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["The Undying","The Fathomless","The Hexblade","The Undead","The Great Old One",
                                         "The Celestial","The Archfey","The Genie","The Fiend"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Artificer":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Alchemist","Armorer","Artillerist","Battle Smith"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
            elif classVar.get() == "Blood Hunter":
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Order of The Ghostslayer","Order of The Lycan","Order of The Mutant",
                                         "Order of The Profane Soul"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
        else:
            subclassVar.set('')
            subclass['menu'].delete(0, 'end')

            char_subclass_options = ["Not High Enough Level"]

            for x in char_subclass_options:
                subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

            subclassVar.set(char_subclass_options[0])

    # diplay entries
    name = Entry(NewCharPage, width=40)
    name.grid(row=1, column=1, padx=20)
    level = OptionMenu(NewCharPage, levelVar, *Level_options, command=subclass)
    level.grid(row=1, column=3)
    char_class = OptionMenu(NewCharPage, classVar, *char_class_options, command=subclass)
    char_class.grid(row=2, column=1)
    subclass = OptionMenu(NewCharPage, subclassVar, *char_subclass_options)
    subclass.grid(row=2, column=3)
    race = OptionMenu(NewCharPage, raceVar, *race_options)
    race.grid(row=3, column=1)
    background = Entry(NewCharPage, width=40)
    background.grid(row=3, column=3)
    stat_type = OptionMenu(NewCharPage, statTypeVar, *stat_type_options, command=Update_Score_Options)
    stat_type.grid(row=3, column=4)

    str = OptionMenu(NewCharPage, strstatVar, *stat_options)
    str.grid(row=4, column=1)
    dex = OptionMenu(NewCharPage, dexstatVar, *stat_options)
    dex.grid(row=4, column=3)
    con = OptionMenu(NewCharPage, constatVar, *stat_options)
    con.grid(row=5, column=1)
    intell = OptionMenu(NewCharPage, intstatVar, *stat_options)
    intell.grid(row=5, column=3)
    wis = OptionMenu(NewCharPage, wisstatVar, *stat_options)
    wis.grid(row=6, column=1)
    cha = OptionMenu(NewCharPage, chastatVar, *stat_options)
    cha.grid(row=6, column=3)

    Label(NewCharPage, text="Name: ", font=("Arial", 15)).grid(row=1, column=0)
    Label(NewCharPage, text="Level: ", font=("Arial", 15)).grid(row=1, column=2)
    Label(NewCharPage, text="Class: ", font=("Arial", 15)).grid(row=2, column=0)
    Label(NewCharPage, text="Subclass: ", font=("Arial", 15)).grid(row=2, column=2)
    Label(NewCharPage, text="Race: ", font=("Arial", 15)).grid(row=3, column=0)
    Label(NewCharPage, text="Background: ", font=("Arial", 15)).grid(row=3, column=2)
    Label(NewCharPage, text="Str: ", font=("Arial", 15)).grid(row=4, column=0)
    Label(NewCharPage, text="Dex: ", font=("Arial", 15)).grid(row=4, column=2)
    Label(NewCharPage, text="Con: ", font=("Arial", 15)).grid(row=5, column=0)
    Label(NewCharPage, text="Int: ", font=("Arial", 15)).grid(row=5, column=2)
    Label(NewCharPage, text="Wis: ", font=("Arial", 15)).grid(row=6, column=0)
    Label(NewCharPage, text="Cha: ", font=("Arial", 15)).grid(row=6, column=2)

    # Function that creates the actual Character object
    def create_Character_Object(char_dict):
        # Function to create other stats based on character information
        # speed set to 30 unless (Check Race things)
        if char_dict[name.get()].race == "Air Genasi" or char_dict[name.get()].race == "Dhampir" or char_dict[
            name.get()].race == "Leonin" or char_dict[name.get()].race == 'Satyr' or char_dict[
            name.get()].race == 'Wood Elf':
            char_dict[name.get()].speed == 35
        elif char_dict[name.get()].race == "Leonin":
            char_dict[name.get()].speed == 40
        else:
            char_dict[name.get()].speed == 30
        # Initi == Dex modifier also check race/class
        char_dict[name.get()].initiative = char_dict[name.get()].dex_mod
        # HP check class then do levelDClass Defaults to Max and set Current HP
        if 'Wiz' in char_dict[name.get()].char_class or 'Sor' in char_dict[name.get()].char_class:
            char_dict[name.get()].HP = char_dict[name.get()].level * 6
        elif 'Fight' in char_dict[name.get()].char_class or 'Pal' in char_dict[name.get()].char_class or 'Rang' in \
                char_dict[name.get()].char_class:
            char_dict[name.get()].HP = char_dict[name.get()].level * 10
        elif 'Barba' in char_dict[name.get()].char_class:
            char_dict[name.get()].HP = char_dict[name.get()].level * 12
        else:
            char_dict[name.get()].HP = char_dict[name.get()].level * 8
        char_dict[name.get()].current_HP = char_dict[name.get()].HP
        # Proficiency bonus
        if char_dict[name.get()].level <= 4:
            char_dict[name.get()].proficiency = 2
        elif 4 < char_dict[name.get()].level <= 8:
            char_dict[name.get()].proficiency = 3
        elif 8 < char_dict[name.get()].level <= 12:
            char_dict[name.get()].proficiency = 4
        elif 12 < char_dict[name.get()].level <= 16:
            char_dict[name.get()].proficiency = 5
        else:
            char_dict[name.get()].proficiency = 6
        #AC Calculation Starts with no armor assumption
        char_dict[name.get()].AC = 10 + char_dict[name.get()].dex_mod


    # Determines modifers
    def Set_Modifiers(char_dict):
        modifiers = []
        # Strength
        if char_dict[name.get()].str_ <= 6:
            modifiers.append(-2)
        elif char_dict[name.get()].str_ == 8 or char_dict[name.get()].str_ == 9:
            modifiers.append(-1)
        elif char_dict[name.get()].str_ == 10 or char_dict[name.get()].str_ == 11:
            modifiers.append(0)
        elif char_dict[name.get()].str_ == 12 or char_dict[name.get()].str_ == 13:
            modifiers.append(1)
        elif char_dict[name.get()].str_ == 14 or char_dict[name.get()].str_ == 15:
            modifiers.append(2)
        elif char_dict[name.get()].str_ == 16 or char_dict[name.get()].str_ == 17:
            modifiers.append(3)
        elif char_dict[name.get()].str_ == 18 or char_dict[name.get()].str_ == 19:
            modifiers.append(4)
        elif char_dict[name.get()].str_ == 20 or char_dict[name.get()].str_ == 21:
            modifiers.append(5)
        elif char_dict[name.get()].str_ == 22 or char_dict[name.get()].str_ == 23:
            modifiers.append(6)
        elif char_dict[name.get()].str_ == 24 or char_dict[name.get()].str_ == 25:
            modifiers.append(7)
        elif char_dict[name.get()].str_ == 26 or char_dict[name.get()].str_ == 27:
            modifiers.append(8)
        elif char_dict[name.get()].str_ == 28 or char_dict[name.get()].str_ == 29:
            modifiers.append(9)
        else:
            modifiers.append(10)

        # Dexterity
        if char_dict[name.get()].dex_ <= 6:
            modifiers.append(-2)
        elif char_dict[name.get()].dex_ == 8 or char_dict[name.get()].dex_ == 9:
            modifiers.append(-1)
        elif char_dict[name.get()].dex_ == 10 or char_dict[name.get()].dex_ == 11:
            modifiers.append(0)
        elif char_dict[name.get()].dex_ == 12 or char_dict[name.get()].dex_ == 13:
            modifiers.append(1)
        elif char_dict[name.get()].dex_ == 14 or char_dict[name.get()].dex_ == 15:
            modifiers.append(2)
        elif char_dict[name.get()].dex_ == 16 or char_dict[name.get()].dex_ == 17:
            modifiers.append(3)
        elif char_dict[name.get()].dex_ == 18 or char_dict[name.get()].dex_ == 19:
            modifiers.append(4)
        elif char_dict[name.get()].dex_ == 20 or char_dict[name.get()].dex_ == 21:
            modifiers.append(5)
        elif char_dict[name.get()].dex_ == 22 or char_dict[name.get()].dex_ == 23:
            modifiers.append(6)
        elif char_dict[name.get()].dex_ == 24 or char_dict[name.get()].dex_ == 25:
            modifiers.append(7)
        elif char_dict[name.get()].dex_ == 26 or char_dict[name.get()].dex_ == 27:
            modifiers.append(8)
        elif char_dict[name.get()].dex_ == 28 or char_dict[name.get()].dex_ == 29:
            modifiers.append(9)
        else:
            modifiers.append(10)

        # Constitution
        if char_dict[name.get()].con_ <= 6:
            modifiers.append(-2)
        elif char_dict[name.get()].con_ == 8 or char_dict[name.get()].con_ == 9:
            modifiers.append(-1)
        elif char_dict[name.get()].con_ == 10 or char_dict[name.get()].con_ == 11:
            modifiers.append(0)
        elif char_dict[name.get()].con_ == 12 or char_dict[name.get()].con_ == 13:
            modifiers.append(1)
        elif char_dict[name.get()].con_ == 14 or char_dict[name.get()].con_ == 15:
            modifiers.append(2)
        elif char_dict[name.get()].con_ == 16 or char_dict[name.get()].con_ == 17:
            modifiers.append(3)
        elif char_dict[name.get()].con_ == 18 or char_dict[name.get()].con_ == 19:
            modifiers.append(4)
        elif char_dict[name.get()].con_ == 20 or char_dict[name.get()].con_ == 21:
            modifiers.append(5)
        elif char_dict[name.get()].con_ == 22 or char_dict[name.get()].con_ == 23:
            modifiers.append(6)
        elif char_dict[name.get()].con_ == 24 or char_dict[name.get()].con_ == 25:
            modifiers.append(7)
        elif char_dict[name.get()].con_ == 26 or char_dict[name.get()].con_ == 27:
            modifiers.append(8)
        elif char_dict[name.get()].con_ == 28 or char_dict[name.get()].con_ == 29:
            modifiers.append(9)
        else:
            modifiers.append(10)

        # Intellegence
        if char_dict[name.get()].intell_ <= 6:
            modifiers.append(-2)
        elif char_dict[name.get()].intell_ == 8 or char_dict[name.get()].intell_ == 9:
            modifiers.append(-1)
        elif char_dict[name.get()].intell_ == 10 or char_dict[name.get()].intell_ == 11:
            modifiers.append(0)
        elif char_dict[name.get()].intell_ == 12 or char_dict[name.get()].intell_ == 13:
            modifiers.append(1)
        elif char_dict[name.get()].intell_ == 14 or char_dict[name.get()].intell_ == 15:
            modifiers.append(2)
        elif char_dict[name.get()].intell_ == 16 or char_dict[name.get()].intell_ == 17:
            modifiers.append(3)
        elif char_dict[name.get()].intell_ == 18 or char_dict[name.get()].intell_ == 19:
            modifiers.append(4)
        elif char_dict[name.get()].intell_ == 20 or char_dict[name.get()].intell_ == 21:
            modifiers.append(5)
        elif char_dict[name.get()].intell_ == 22 or char_dict[name.get()].intell_ == 23:
            modifiers.append(6)
        elif char_dict[name.get()].intell_ == 24 or char_dict[name.get()].intell_ == 25:
            modifiers.append(7)
        elif char_dict[name.get()].intell_ == 26 or char_dict[name.get()].intell_ == 27:
            modifiers.append(8)
        elif char_dict[name.get()].intell_ == 28 or char_dict[name.get()].intell_ == 29:
            modifiers.append(9)
        else:
            modifiers.append(10)

        # Wisdom
        if char_dict[name.get()].wis_ <= 6:
            modifiers.append(-2)
        elif char_dict[name.get()].wis_ == 8 or char_dict[name.get()].wis_ == 9:
            modifiers.append(-1)
        elif char_dict[name.get()].wis_ == 10 or char_dict[name.get()].wis_ == 11:
            modifiers.append(0)
        elif char_dict[name.get()].wis_ == 12 or char_dict[name.get()].wis_ == 13:
            modifiers.append(1)
        elif char_dict[name.get()].wis_ == 14 or char_dict[name.get()].wis_ == 15:
            modifiers.append(2)
        elif char_dict[name.get()].wis_ == 16 or char_dict[name.get()].wis_ == 17:
            modifiers.append(3)
        elif char_dict[name.get()].wis_ == 18 or char_dict[name.get()].wis_ == 19:
            modifiers.append(4)
        elif char_dict[name.get()].wis_ == 20 or char_dict[name.get()].wis_ == 21:
            modifiers.append(5)
        elif char_dict[name.get()].wis_ == 22 or char_dict[name.get()].wis_ == 23:
            modifiers.append(6)
        elif char_dict[name.get()].wis_ == 24 or char_dict[name.get()].wis_ == 25:
            modifiers.append(7)
        elif char_dict[name.get()].wis_ == 26 or char_dict[name.get()].wis_ == 27:
            modifiers.append(8)
        elif char_dict[name.get()].wis_ == 28 or char_dict[name.get()].wis_ == 29:
            modifiers.append(9)
        else:
            modifiers.append(10)

        # Charisma
        if char_dict[name.get()].cha_ <= 6:
            modifiers.append(-2)
        elif char_dict[name.get()].cha_ == 8 or char_dict[name.get()].cha_ == 9:
            modifiers.append(-1)
        elif char_dict[name.get()].cha_ == 10 or char_dict[name.get()].cha_ == 11:
            modifiers.append(0)
        elif char_dict[name.get()].cha_ == 12 or char_dict[name.get()].cha_ == 13:
            modifiers.append(1)
        elif char_dict[name.get()].cha_ == 14 or char_dict[name.get()].cha_ == 15:
            modifiers.append(2)
        elif char_dict[name.get()].cha_ == 16 or char_dict[name.get()].cha_ == 17:
            modifiers.append(3)
        elif char_dict[name.get()].cha_ == 18 or char_dict[name.get()].cha_ == 19:
            modifiers.append(4)
        elif char_dict[name.get()].cha_ == 20 or char_dict[name.get()].cha_ == 21:
            modifiers.append(5)
        elif char_dict[name.get()].cha_ == 22 or char_dict[name.get()].cha_ == 23:
            modifiers.append(6)
        elif char_dict[name.get()].cha_ == 24 or char_dict[name.get()].cha_ == 25:
            modifiers.append(7)
        elif char_dict[name.get()].cha_ == 26 or char_dict[name.get()].cha_ == 27:
            modifiers.append(8)
        elif char_dict[name.get()].cha_ == 28 or char_dict[name.get()].cha_ == 29:
            modifiers.append(9)
        else:
            modifiers.append(10)
            # store modifiers to be stored
        char_dict[name.get()].str_mod = modifiers[0]
        char_dict[name.get()].dex_mod = modifiers[1]
        char_dict[name.get()].con_mod = modifiers[2]
        char_dict[name.get()].intell_mod = modifiers[3]
        char_dict[name.get()].wis_mod = modifiers[4]
        char_dict[name.get()].cha_mod = modifiers[5]

    #Submits character and clears entry form
    def submit():
        # connect to db to add information

        char_dict[name.get()] = Character(name.get(), raceVar.get(), classVar.get(), subclassVar.get(),background.get(), levelVar.get(),
                                          int(strstatVar.get()), int(dexstatVar.get()), int(constatVar.get()),
                                          int(wisstatVar.get()), int(intstatVar.get()), int(chastatVar.get()))
        Set_Modifiers(char_dict)
        create_Character_Object(char_dict)

        name.delete(0, END)
        levelVar.set(Level_options[0])
        classVar.set(char_class_options[0])
        subclassVar.set(char_subclass_options[0])
        raceVar.set(race_options[0])
        background.delete(0, END)
        strstatVar.set(stdarr_stats_options[0])
        constatVar.set(stdarr_stats_options[0])
        dexstatVar.set(stdarr_stats_options[0])
        intstatVar.set(stdarr_stats_options[0])
        wisstatVar.set(stdarr_stats_options[0])
        chastatVar.set(stdarr_stats_options[0])

        Label(NewCharPage, text="Character Successfully Added. You may now enter another character or exit the page ",
              font=('arial', 15), bg='yellow').place(relx=0.1, rely=0.7)

    Button(NewCharPage, text="Create Character", command=submit).grid(row=7, column=2, columnspan=2)


def close():
    file = open("characters.pkl", 'a+')
    with open("characters.pkl", 'wb') as out_strm:
        dill.dump(char_dict, out_strm)
    Menu.destroy()


def View():
    ViewCharPage = Toplevel(Menu)
    ViewCharPage.geometry("800x800")
    ViewCharPage.configure(bg="black")
    # Pull from database and display
    name_list = list(char_dict.keys())
    set_name = tk.StringVar(ViewCharPage)
    set_name.set("")

    def selected(event):
        Label(ViewCharPage, text="AC:" + str(char_dict[set_name.get()].AC), background='black', foreground='red').place(relx=0.0, rely=0.1)
        Label(ViewCharPage, text="HP:", background='black', foreground='red').place(relx=0.2, rely=0.1)
        curr_HP = tk.IntVar()
        curr_HP.set(char_dict[set_name.get()].current_HP-.1)
        #Works but very hard to see as it is Grey on Grey
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", background='red')
        ttk.Progressbar(ViewCharPage,style= "red.Horizontal.TProgressbar",maximum=char_dict[set_name.get()].HP, variable=curr_HP ,orient=tk.HORIZONTAL).place(relx=0.24, rely=0.1)
        #Stats
        Label(ViewCharPage, text="STR\n" + str(char_dict[set_name.get()].str_mod), background='black', foreground='red', borderwidth=1, relief="solid").place(relx=0.0, rely=0.2)
        Label(ViewCharPage, text="CON\n" + str(char_dict[set_name.get()].con_mod), background='black', borderwidth=1, relief="solid",
              foreground='red').place(relx=0.0, rely=0.3)
        Label(ViewCharPage, text="DEX\n" + str(char_dict[set_name.get()].dex_mod), background='black', borderwidth=1, relief="solid",
              foreground='red').place(relx=0.0, rely=0.4)
        Label(ViewCharPage, text="WIS\n" + str(char_dict[set_name.get()].wis_mod), background='black', borderwidth=1, relief="solid",
              foreground='red').place(relx=0.0, rely=0.5)
        Label(ViewCharPage, text="INT\n" + str(char_dict[set_name.get()].intell_mod), background='black', borderwidth=1, relief="solid",
              foreground='red').place(relx=0.0, rely=0.6)
        Label(ViewCharPage, text="CHA\n" + str(char_dict[set_name.get()].cha_mod), background='black', borderwidth=1, relief="solid",
              foreground='red').place(relx=0.0, rely=0.7)


    Label(ViewCharPage, text="Your Character", fg='red', bg='black', font=('arial', 15)).place(relx=0.0, rely=0.0)
    char_select = OptionMenu(ViewCharPage, set_name, *name_list, command=selected)
    char_select.place(relx=0.2, rely=0.0)
    Button(ViewCharPage, text="Play as this character", command=lambda : Play_Class_Select(char_dict[set_name.get()])).place(relx=0.35, rely=0.0)


try:
    infile = "characters.pkl"
    with open(infile, 'rb') as in_strm:
        char_dict = dill.load(in_strm)

except:
    pass

Label(Menu, text="Welcome Legends!", bg="Black", fg="red", font=('arial', 20)).place(relx=0.35, rely=0.0)
# Buttons to import a character or view a character
Menu.title("Main Menu")
Menu.geometry("800x800")
Menu.configure(bg="black")

Button(Menu, text="Add a new Character", command=NewChar).place(relx=0.1, rely=0.7)
Button(Menu, text="View a Character", command=View).place(relx=0.7, rely=0.7)
Button(Menu, text="Exit", command=close).place(relx=0.9, rely=0.0)
Menu.mainloop()
