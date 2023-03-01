# Application to simplify play with high level characters
import random
import dill
from tkinter import *
import PIL.Image, PIL.ImageTk
from images import *
import spells
from Classes import *
from tkinter import ttk

Menu = Tk()

char_dict = {}

class Character:
    def __init__(self, name='name', race='Human', subrace = "Variant", char_class='Barbarian', subclass="Path of The Zealot", background='Solider', level=1, str_=15,
                 dex_=15, con_=15, wis_=15, int_=15, cha_=15):
        self.name = name
        self.race = race
        self.subrace = subrace
        self.char_class = char_class
        self.subclass = subclass
        self.background = background
        self.level = level
        self.str_ = str_
        self.dex_ = dex_
        self.con_ = con_
        self.int_ = int_
        self.wis_ = wis_
        self.cha_ = cha_
        self.str_mod = self.dex_mod = self.con_mod = self.intell_mod = self.wis_mod = self.cha_mod = 1
        self.initiative = 0
        self.HP = 0
        self.proficiency = 0
        self.AC = 0
        self.speed = 30
        self.current_HP = 0
        self.darkvision = 0
        self.save_prof = []
        self.skill_prof = []
        self.weapon_prof = []
        self.armor_prof = []
        self.tool_prof = []
        self.skill_scores=[]
        self.spells= []
        self.resistance = []
        self.languages = ["Common"]
        self.adv =[]
        self.feats = []
        self.weapon = []



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

    back_options = ["Acolyte","Criminal/Spy","Folk Hero","Noble","Sage","Solider"]
    backVar = StringVar(NewCharPage)
    backVar.set(back_options[0])

    skill_options = ['']
    skillVar = tk.Variable(value=skill_options)

    music_options = ['Bagpipes', 'Drum', 'Dulcimer', 'Flute', 'Lute', 'Lyre', 'Horn', 'Pan Flute', 'Shawm', 'Viol']
    musicVar = tk.Variable(value=music_options)

    tool_options = ['Alchemists','Brewers','Calligraphers','Carpenters','Cartographers','Cobblers','Cooks','Glassblowers'
        ,'Jewelers','Leatherworkers','Masons','Painters','Potters','Smiths','Tinkers','Weavers','Woodcarvers']

    monk_options = ['Instrument','Artisan Tools']
    monkVar = StringVar(NewCharPage)

    race_options = ["Dragonborne", "Dwarf", "Elf", "Gnome", "Half-Elf", "Halfling", "Half-Orc", "Human","Tiefling",
                    "Leonin","Satyr", "Aarakorcra", "Aasimar", "Changeling", "Fairy","Genasi", "Goblin","Goliath",
                    "Harengon", "Tabaxi", "Triton", "Warforged", "Plasmoid"]
    raceVar = StringVar(NewCharPage)
    raceVar.set(race_options[-1])

    langs = ["Dwarvish","Giant","Elvish","Gnomish","Goblin","Halfling","Orcish","Abyssal","Celestial","Draconic","Deep"
        ,"Infernal","Primordial","Sylvan","Undercommon"]

    raceSpecVar = StringVar(NewCharPage)
    race_spec_options = ['None']

    raceSkillVar = StringVar(NewCharPage)
    raceFeatVar = StringVar(NewCharPage)
    feats_options = ["Lucky"]

    dwarfToolVar = StringVar(NewCharPage)
    dwarf_tools_options = ["Smiths", "Brewers", "Masons"]

    highSpellVar = StringVar(NewCharPage)
    high_spell_options = spells.wizard_cantrip

    raceLangVar = StringVar(NewCharPage)
    race_lang_options = ["Dwarvish","Giant","Gnomish","Goblin","Halfling","Orcish","Abyssal","Celestial","Draconic","Deep"
        ,"Infernal","Primordial","Sylvan","Undercommon"]
    halfElfSkillVar = StringVar(NewCharPage)
    halfelf_skill_options = ["Acrobatics","Animal Handling", "Arcana","Athletics","Deception","History","Insight",
                             "Intimidation", "Investigation", "Medicine","Nature", "Perception", "Performance",
                             "Persuasion","Religion", "Sleight of Hand","Stealth","Survival"]

    score_options = []

    statTypeVar = StringVar(NewCharPage)
    stat_type_options = ["Standard Array", "Roll", "Point Buy"]
    statTypeVar.set(stat_type_options[0])
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


    def roll_stats():
        final_stats = []
        temp_stat = []
        x = 0
        while x < 6:
            y = 0
            temp_stat.clear()
            while y < 4:
                temp_stat.append(random.randrange(1,6))
                y += 1
            temp_stat.remove(min(temp_stat))
            total = 0
            for num in temp_stat:
                total += num
            final_stats.append(total)
            x += 1
        return final_stats

    # Updated Stat score options based on Std array, roll or point buy
    def Update_Score_Options(selection):
        if statTypeVar.get() == "Standard Array":
            strstatVar.set('')
            constatVar.set('')
            dexstatVar.set('')
            intstatVar.set('')
            wisstatVar.set('')
            chastatVar.set('')

            str_opt['menu'].delete(0, 'end')
            con['menu'].delete(0, 'end')
            dex['menu'].delete(0, 'end')
            intell['menu'].delete(0, 'end')
            wis['menu'].delete(0, 'end')
            cha['menu'].delete(0, 'end')

            stat_options = stdarr_stats_options

            for x in stat_options:
                str_opt['menu'].add_command(label=x, command=tk._setit(strstatVar, x))
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
        elif statTypeVar.get() == "Roll":
            strstatVar.set('')
            constatVar.set('')
            dexstatVar.set('')
            intstatVar.set('')
            wisstatVar.set('')
            chastatVar.set('')

            str_opt['menu'].delete(0, 'end')
            con['menu'].delete(0, 'end')
            dex['menu'].delete(0, 'end')
            intell['menu'].delete(0, 'end')
            wis['menu'].delete(0, 'end')
            cha['menu'].delete(0, 'end')

            stat_options = roll_stats()

            for x in stat_options:
                str_opt['menu'].add_command(label=x, command=tk._setit(strstatVar, x))
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

            str_opt['menu'].delete(0, 'end')
            con['menu'].delete(0, 'end')
            dex['menu'].delete(0, 'end')
            intell['menu'].delete(0, 'end')
            wis['menu'].delete(0, 'end')
            cha['menu'].delete(0, 'end')

            stat_options = Level_options

            for x in stat_options:
                str_opt['menu'].add_command(label=x, command=tk._setit(strstatVar, x))
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

            return

    # Creates dropdowns for subclass options based on class choice
    def Class_Specific_Attributes(selection):
        # Update subclass options based on class selection
        Tool_label.forget()
        monk_choice1.grid_forget()
        monk_choice2.grid_forget()
        musicbox.grid_forget()
        toolbox.grid_forget()
        if classVar.get() == "Barbarian":
            barbarian_ref = PIL.ImageTk.PhotoImage(barbarian)
            Class_Image.config(image=barbarian_ref)
            Class_Image.image = barbarian_ref
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = ["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])



            if levelVar.get() >=3:
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
            bard_ref = PIL.ImageTk.PhotoImage(bard)
            Class_Image.config(image=bard_ref)
            Class_Image.image = bard_ref
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = ["Acrobatics","Animal Handling", "Arcana","Athletics","Deception","History","Insight",
                             "Intimidation", "Investigation", "Medicine","Nature", "Perception", "Performance",
                             "Persuasion","Religion", "Sleight of Hand","Stealth","Survival"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            #dealing with Musical tool choices
            Tool_label.grid(row=8, column=3)
            musicbox.grid(row=8, column=4)

            if levelVar.get() >= 3:
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
            cleric_ref = PIL.ImageTk.PhotoImage(cleric)
            Class_Image.config(image=cleric_ref)
            Class_Image.image = cleric_ref
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = [ "History", "Insight", "Medicine",
                             "Persuasion", "Religion",]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            if levelVar.get() >= 3:
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
            druid_ref = PIL.ImageTk.PhotoImage(druid)
            Class_Image.config(image=druid_ref)
            Class_Image.image = druid_ref
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = ["Animal Handling", "Arcana", "Insight",
                             "Medicine", "Nature", "Perception", "Religion",  "Survival"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            if levelVar.get() >= 3:
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Circle of Spores", "Circle of Dreams", "Circle of Moon", "Circle of Land",
                                         "Circle of Stars", "Circle of Wildfire", "Circle of Shephard"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
        elif classVar.get() == "Fighter":
            fighter_ref = PIL.ImageTk.PhotoImage(fighter)
            Class_Image.config(image=fighter_ref)
            Class_Image.image = fighter_ref
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = ["Acrobatics", "Animal Handling", "Athletics", "History", "Insight",
                             "Intimidation", "Perception", "Survival"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            if levelVar.get() >= 3:
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
            monk_ref = PIL.ImageTk.PhotoImage(monk)
            Class_Image.config(image=monk_ref)
            Class_Image.image = monk_ref
            skillVar.set('')
            listbox.delete(0, 'end')
            monk_choice1.grid(row=8,column=3)
            monk_choice2.grid(row=8,column=4)

            skill_options = ["Acrobatics", "Athletics", "History", "Insight",
                             "Religion", "Stealth"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            if levelVar.get() >= 3:
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
            paladin_ref = PIL.ImageTk.PhotoImage(paladin)
            Class_Image.config(image=paladin_ref)
            Class_Image.image = paladin_ref
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = [ "Athletics", "Insight",
                             "Intimidation", "Medicine",
                             "Persuasion", "Religion"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            if levelVar.get() >= 3:
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Oath of The Crown","Oath of Devotion","Oath of Glory","Oath of Conquest",
                                         "Oath of The Open Sea","Oath of The Watchers","Oath of The Ancients",
                                         "Oathbreaker","Oath of Redemption","Oath of Vengeance"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
        elif classVar.get() == "Ranger":
            ranger_ref = PIL.ImageTk.PhotoImage(ranger)
            Class_Image.config(image=ranger_ref)
            Class_Image.image = ranger_ref
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = ["Animal Handling", "Athletics","Insight",
                             "Investigation", "Nature", "Perception", "Stealth", "Survival"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            if levelVar.get() >= 3:
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Hunter Conclave","Beast Master Conclave","Fey Wanderer Conclave",
                                         "Drakewarden Conclave","Monster Slayer Conclave", "Gloom Stalker Conclave",
                                         "Swarm Keeper Conclave", "Horizon Walker Conclave"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
        elif classVar.get() == "Rogue":
            rogue_ref = PIL.ImageTk.PhotoImage(rogue)
            Class_Image.config(image=rogue_ref)
            Class_Image.image = rogue_ref
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = ["Acrobatics", "Athletics", "Deception","Insight",
                             "Intimidation", "Investigation",  "Perception", "Performance",
                             "Persuasion", "Sleight of Hand", "Stealth"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            if levelVar.get() >= 3:
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Mastermind","Inquisitive","Swashbuckler","Scout","Phantom","Arcane Trickster",
                                         "Assassin","Soul Knife","Thief"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
        elif classVar.get() == "Sorcerer":
            sorcerer_ref = PIL.ImageTk.PhotoImage(sorcerer)
            Class_Image.config(image=sorcerer_ref)
            Class_Image.image = sorcerer_ref
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = ["Arcana", "Deception","Insight",
                             "Intimidation",
                             "Persuasion", "Religion"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            if levelVar.get() >= 3:
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Wild Magic","Storm","Lunar","Divine Soul","Clockwork Soul",
                                         "Draconic Bloodline","Aberrant Mind","Shadow Magic"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
        elif classVar.get() == "Wizard":
            wizard_ref = PIL.ImageTk.PhotoImage(wizard)
            Class_Image.config(image=wizard_ref)
            Class_Image.image = wizard_ref
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = ["Arcana","History", "Insight",
                             "Investigation", "Medicine","Religion"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            if levelVar.get() >= 3:
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
            warlock_ref = PIL.ImageTk.PhotoImage(warlock)
            Class_Image.config(image=warlock_ref)
            Class_Image.image = warlock_ref
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = [ "Arcana","Deception", "History",
                             "Intimidation", "Investigation", "Nature", "Religion"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            if levelVar.get() >= 3:
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["The Undying","The Fathomless","The Hexblade","The Undead","The Great Old One",
                                         "The Celestial","The Archfey","The Genie","The Fiend"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
        elif classVar.get() == "Artificer":
            artificer_ref = PIL.ImageTk.PhotoImage(artificer)
            Class_Image.config(image=artificer_ref)
            Class_Image.image = artificer_ref
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = ["Arcana", "History",
                              "Investigation", "Medicine", "Nature", "Perception", "Sleight of Hand"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            Tool_label.grid(row=8, column=3)
            toolbox.grid(row=8, column=4)

            if levelVar.get() >= 3:
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Alchemist","Armorer","Artillerist","Battle Smith"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
        elif classVar.get() == "Blood Hunter":
            skillVar.set('')
            listbox.delete(0, 'end')

            skill_options = ["Acrobatics","Arcana", "Athletics","History", "Insight",
                             "Investigation", "Religion", "Survival"]

            for x in skill_options:
                listbox.insert(END, x)

            skillVar.set(skill_options[0])

            if levelVar.get() >= 3:
                subclassVar.set('')
                subclass['menu'].delete(0, 'end')

                char_subclass_options = ["Order of The Ghostslayer","Order of The Lycan","Order of The Mutant",
                                         "Order of The Profane Soul"]

                for x in char_subclass_options:
                    subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

                subclassVar.set(char_subclass_options[0])
        if levelVar.get() < 3:
            subclassVar.set('')
            subclass['menu'].delete(0, 'end')

            char_subclass_options = ["Not High Enough Level"]

            for x in char_subclass_options:
                subclass['menu'].add_command(label=x, command=tk._setit(subclassVar, x))

            subclassVar.set(char_subclass_options[0])

    #Creates dropdown for subraces
    def Race_Options(selection):
        leonin_skill_choice.grid_forget()
        vhuman_skill_choice.grid_forget()
        vhuman_feat_choice.grid_forget()
        human_lang_choice.grid_forget()
        vhumanScoreBox.grid_forget()
        halfelfbox.grid_forget()
        halfelfbox2.grid_forget()
        high_lang_choice.grid_forget()
        high_spell_choice.grid_forget()
        dwarf_tool_choice.grid_forget()
        satyr_music_choice.grid_forget()
        if raceVar.get() == "Dwarf":
            dwarf_ref = PIL.ImageTk.PhotoImage(dwarf)
            Race_Image.config(image=dwarf_ref)
            Race_Image.image = dwarf_ref
            dwarf_tool_choice.grid(row=4, column=3)
            raceSpecVar.set('')
            race_specifics['menu'].delete(0, 'end')

            race_spec_options = ["Hill","Mountain"]

            for x in race_spec_options:
                race_specifics['menu'].add_command(label=x, command=tk._setit(raceSpecVar, x))

            raceSpecVar.set(race_spec_options[0])
        elif raceVar.get() == "Elf":
            elf_ref = PIL.ImageTk.PhotoImage(elf)
            Race_Image.config(image=elf_ref)
            Race_Image.image = elf_ref
            if raceSpecVar.get() == "High":
                high_lang_choice.grid(row=4, column=3)
                high_spell_choice.grid(row=4, column= 4)
            raceSpecVar.set('')
            race_specifics['menu'].delete(0, 'end')

            race_spec_options = ["High","Wood","Drow"]

            for x in race_spec_options:
                race_specifics['menu'].add_command(label=x, command=tk._setit(raceSpecVar, x))

            raceSpecVar.set(race_spec_options[0])
        elif raceVar.get() == "Human":
            human_ref = PIL.ImageTk.PhotoImage(human)
            Race_Image.config(image=human_ref)
            Race_Image.image = human_ref
            human_lang_choice.grid(row=4,column=3)
            if raceSpecVar.get() == "Variant":
                score_options = ["Str", "Dex", "Con", "Wis", "Int"]
                for x in score_options:
                    vhumanScoreBox.insert(END, x)
                vhumanScoreBox.grid(row=4,column=4)
                vhuman_feat_choice.grid(row=4, column=5)
                vhuman_skill_choice.grid(row=4, column=6)

            raceSpecVar.set('')
            race_specifics['menu'].delete(0, 'end')

            race_spec_options = ["Human","Variant"]

            for x in race_spec_options:
                race_specifics['menu'].add_command(label=x, command=tk._setit(raceSpecVar, x))

            raceSpecVar.set(race_spec_options[0])
        elif raceVar.get() == "Dragonborn":
            dragon_ref = PIL.ImageTk.PhotoImage(dragonborn)
            Race_Image.config(image=dragon_ref)
            Race_Image.image = dragon_ref
            raceSpecVar.set('')
            race_specifics['menu'].delete(0, 'end')

            race_spec_options = ["Black","Blue","Brass","Bronze","Copper","Gold","Green","Red","Silver","White"]

            for x in race_spec_options:
                race_specifics['menu'].add_command(label=x, command=tk._setit(raceSpecVar, x))

            raceSpecVar.set(race_spec_options[0])
        elif raceVar.get() == "Gnome":
            gnome_ref = PIL.ImageTk.PhotoImage(gnome)
            Race_Image.config(image=gnome_ref)
            Race_Image.image = gnome_ref
            raceSpecVar.set('')
            race_specifics['menu'].delete(0, 'end')

            race_spec_options = ["Forest","Rock"]

            for x in race_spec_options:
                race_specifics['menu'].add_command(label=x, command=tk._setit(raceSpecVar, x))

            raceSpecVar.set(race_spec_options[0])
        elif raceVar.get() == "Genasi":
            if raceSpecVar.get() == "Air":
                airg_ref = PIL.ImageTk.PhotoImage(airgenasi)
                Race_Image.config(image=airg_ref)
                Race_Image.image = airg_ref
            elif raceSpecVar.get() == "Earth":
                earthg_ref = PIL.ImageTk.PhotoImage(earthgenasi)
                Race_Image.config(image=earthg_ref)
                Race_Image.image = earthg_ref
            elif raceSpecVar.get() == "Fire":
                fireg_ref = PIL.ImageTk.PhotoImage(firegenasi)
                Race_Image.config(image=fireg_ref)
                Race_Image.image = fireg_ref
            else:
                waterg_ref = PIL.ImageTk.PhotoImage(watergenasi)
                Race_Image.config(image=waterg_ref)
                Race_Image.image = waterg_ref

            raceSpecVar.set('')
            race_specifics['menu'].delete(0, 'end')

            race_spec_options = ["Air","Earth","Fire","Earth"]

            for x in race_spec_options:
                race_specifics['menu'].add_command(label=x, command=tk._setit(raceSpecVar, x))

            raceSpecVar.set(race_spec_options[0])
        elif raceVar.get() == "Aasimar":
            aasimar_ref = PIL.ImageTk.PhotoImage(aasimar)
            Race_Image.config(image=aasimar_ref)
            Race_Image.image = aasimar_ref
            raceSpecVar.set('')
            race_specifics['menu'].delete(0, 'end')

            race_spec_options = ["Protector","Scourge","Fallen"]

            for x in race_spec_options:
                race_specifics['menu'].add_command(label=x, command=tk._setit(raceSpecVar, x))

            raceSpecVar.set(race_spec_options[0])
        elif raceVar.get() == "Halfling":
            halfling_ref = PIL.ImageTk.PhotoImage(halfling)
            Race_Image.config(image=halfling_ref)
            Race_Image.image = halfling_ref
            raceSpecVar.set('')
            race_specifics['menu'].delete(0, 'end')

            race_spec_options = ["Stout","Lightfoot"]

            for x in race_spec_options:
                race_specifics['menu'].add_command(label=x, command=tk._setit(raceSpecVar, x))

            raceSpecVar.set(race_spec_options[0])
        elif raceVar.get() == "Half-Elf":
            halfelf_ref = PIL.ImageTk.PhotoImage(halfelf)
            Race_Image.config(image=halfelf_ref)
            Race_Image.image = halfelf_ref
            skill_options = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight",
                             "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance",
                             "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"]
            for x in skill_options:
                halfelfbox.insert(END, x)
            halfelfbox.grid(row=4, column=4)
            high_lang_choice.grid(row=4, column=3)
            score_options = ["Str","Dex","Con","Wis","Int"]
            for x in score_options:
                halfelfbox2.insert(END,x)
            halfelfbox2.grid(row=4,column=6)
        elif raceVar.get() == "Leonin":
            leonin_ref = PIL.ImageTk.PhotoImage(leonin)
            Race_Image.config(image=leonin_ref)
            Race_Image.image = leonin_ref
            leonin_skill_choice.grid(row=4, column=4)
        elif raceVar.get() == "Satyr":
            satyr_ref = PIL.ImageTk.PhotoImage(satry)
            Race_Image.config(image=satyr_ref)
            Race_Image.image = satyr_ref
            satyr_music_choice.grid(row=4,column=4)
        else:
            raceSpecVar.set('')
            race_specifics['menu'].delete(0, 'end')

            race_spec_options = ["None"]

            for x in race_spec_options:
                race_specifics['menu'].add_command(label=x, command=tk._setit(raceSpecVar, x))

            raceSpecVar.set(race_spec_options[0])

    def Count_Proficiencies_Selected(selection):
        #Use a counter to prevent additional selections if too many
        if classVar.get() == "Bard" or classVar.get() == "Ranger" or classVar.get() == "Blood Hunter":
            if len(listbox.curselection()) > 3:
                listbox.selection_clear('active')
                Label(NewCharPage, text="You can only select 3 additional skills").grid(row=8,column=2)
        elif classVar.get() == "Rogue":
            if len(listbox.curselection()) > 4:
                listbox.selection_clear('active')
                Label(NewCharPage, text="You can only select 4 additional skills").grid(row=8,column=2)
        else:
            if len(listbox.curselection()) > 2:
                listbox.selection_clear('active')
                Label(NewCharPage, text="You can only select 2 additional skills").grid(row=8,column=2)
        if classVar.get() == "Bard":
            if len(musicbox.curselection()) > 3:
                musicbox.selection_clear('active')
                Label(NewCharPage, text="You can only select 3 Instruments").grid(row=8,column=5)
        if classVar.get() == "Artificer":
            if len(toolbox.curselection()) > 1:
                toolbox.selection_clear('active')
                Label(NewCharPage, text="You can only select 1 Tool").grid(row=8, column=5)
        if classVar.get() == "Monk":
            if len(toolbox.curselection()) > 1 or len(musicbox.curselection()) > 1:
                toolbox.selection_clear('active')
                musicbox.selection_clear('active')
                Label(NewCharPage, text="You can only select 1 Tool").grid(row=8, column=5)

        if raceVar.get() == "Half-Elf":
            if len(halfelfbox.curselection()) > 2:
                halfelfbox.selection_clear('active')
                Label(NewCharPage, text="You can only select 2").grid(row=4, column=5)
            if len(halfelfbox2.curselection()) > 2:
                halfelfbox2.selection_clear('active')
                Label(NewCharPage, text="You can only select 2").grid(row=4, column=5)
        if raceSpecVar.get() == "Variant":
            if len(vhumanScoreBox.curselection()) > 2:
                vhumanScoreBox.selection_clear('active')
                Label(NewCharPage, text="You can only select 2").grid(row=4, column=5)
    # VISUAL ISSUE __ OVERLAY RATHER THAN REPLACE
    def Display_Back_Skills(selection):
        if backVar.get() == "Acolyte":
            Back_Label.config(text="Skills: Insight, Religion")
        elif backVar.get() == "Criminal/Spy":
            Back_Label.config(text= "Skills: Deception, Stealth")
        elif backVar.get() == "Folk Hero":
            Back_Label.config(text= "Skills: Animal Handling, Survival")
        elif backVar.get() == "Noble":
            Back_Label.config(text= "Skills: History, Persuasion")
        elif backVar.get() == "Solider":
            Back_Label.config(text= "Skills: Athletics, Intimidation")
        elif backVar.get() == "Sage":
            Back_Label.config(text= "Skills: Arcana, History")


    def Monk_choice_setup(selection):
        if monkVar.get() == "Instrument":
            musicbox.grid_forget()
            toolbox.grid_forget()
            musicbox.grid(row=9, column=4)
        elif monkVar.get() == "Artisan Tools":
            musicbox.grid_forget()
            toolbox.grid_forget()
            toolbox.grid(row=9, column=4)

    # diplay entries
    name = Entry(NewCharPage, width=40)
    name.grid(row=1, column=1, padx=20)
    level = OptionMenu(NewCharPage, levelVar, *Level_options, command=Class_Specific_Attributes)
    level.grid(row=1, column=3)
    char_class = OptionMenu(NewCharPage, classVar, *char_class_options, command=Class_Specific_Attributes)
    char_class.grid(row=2, column=1)
    subclass = OptionMenu(NewCharPage, subclassVar, *char_subclass_options)
    subclass.grid(row=2, column=3)
    race = OptionMenu(NewCharPage, raceVar, *race_options, command=Race_Options)
    race.grid(row=3, column=1)
    race_specifics = OptionMenu(NewCharPage, raceSpecVar, *race_spec_options, command=Race_Options)
    race_specifics.grid(row=4, column=1)
    background = OptionMenu(NewCharPage, backVar, *back_options, command=Display_Back_Skills)
    background.grid(row=3, column=3)
    stat_type = OptionMenu(NewCharPage, statTypeVar, *stat_type_options, command=Update_Score_Options)
    stat_type.grid(row=1, column=5)

    str_opt = OptionMenu(NewCharPage, strstatVar, *stat_options)
    str_opt.grid(row=5, column=1)
    dex = OptionMenu(NewCharPage, dexstatVar, *stat_options)
    dex.grid(row=5, column=3)
    con = OptionMenu(NewCharPage, constatVar, *stat_options)
    con.grid(row=6, column=1)
    intell = OptionMenu(NewCharPage, intstatVar, *stat_options)
    intell.grid(row=6, column=3)
    wis = OptionMenu(NewCharPage, wisstatVar, *stat_options)
    wis.grid(row=7, column=1)
    cha = OptionMenu(NewCharPage, chastatVar, *stat_options)
    cha.grid(row=7, column=3)
    listbox = tk.Listbox(NewCharPage,listvariable=skill_options, height=6, selectmode=tk.MULTIPLE,exportselection=False)
    listbox.grid(row=9,column=1)
    listbox.bind("<<ListboxSelect>>", Count_Proficiencies_Selected)
    musicbox = tk.Listbox(NewCharPage,height=6, selectmode=tk.MULTIPLE,exportselection=False)
    for i in music_options:
        musicbox.insert(END, i)
    musicbox.bind("<<ListboxSelect>>", Count_Proficiencies_Selected)
    toolbox = tk.Listbox(NewCharPage, height=6, selectmode=tk.MULTIPLE, exportselection=False)
    for i in tool_options:
        toolbox.insert(END, i)
    toolbox.bind("<<ListboxSelect>>", Count_Proficiencies_Selected)
    monk_choice1 = Label(NewCharPage,text="Instrument or Artisian Tools?")
    monk_choice2 = OptionMenu(NewCharPage, monkVar, *monk_options, command=Monk_choice_setup)

    #Potential race options
    #Dwarf
    dwarf_tool_choice = OptionMenu(NewCharPage, dwarfToolVar, *dwarf_tools_options)
    #High Elf
    high_spell_choice = OptionMenu(NewCharPage, highSpellVar, *high_spell_options)
    high_lang_choice = OptionMenu(NewCharPage, raceLangVar, *race_lang_options)
    #Half-elf
    halfelfbox = tk.Listbox(NewCharPage,listvariable=skill_options, height=6, selectmode=tk.MULTIPLE,exportselection=False)
    halfelfbox.bind("<<ListboxSelect>>", Count_Proficiencies_Selected)
    halfelfbox2 = tk.Listbox(NewCharPage, listvariable=score_options, height=6, selectmode=tk.MULTIPLE,
                            exportselection=False)
    halfelfbox2.bind("<<ListboxSelect>>", Count_Proficiencies_Selected)
    #human
    human_lang_choice = OptionMenu(NewCharPage, raceLangVar, *race_lang_options)
    skill_options = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight",
                     "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance",
                     "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"]
    vhuman_skill_choice = OptionMenu(NewCharPage, raceSkillVar, *skill_options)
    vhuman_feat_choice = OptionMenu(NewCharPage, raceFeatVar, *feats_options)
    vhumanScoreBox = tk.Listbox(NewCharPage, listvariable=score_options, height=5, selectmode=tk.MULTIPLE,
                            exportselection=False)
    vhumanScoreBox.bind("<<ListboxSelect>>", Count_Proficiencies_Selected)

    skill_options = ["Athletics", "Intimidation","Perception", "Survival"]
    #leonin
    leonin_skill_choice = OptionMenu(NewCharPage, raceSkillVar, *skill_options)
    #satyr
    satyr_music_choice = OptionMenu(NewCharPage, raceSkillVar, *music_options)

    #Also choose a language but just reusing high elfs

    Label(NewCharPage, text="Name: ", font=("Arial", 15)).grid(row=1, column=0)
    Label(NewCharPage, text="Level: ", font=("Arial", 15)).grid(row=1, column=2)
    Label(NewCharPage, text="Gen Method: ", font=("Arial", 15)).grid(row=1, column=4)
    Label(NewCharPage, text="Class: ", font=("Arial", 15)).grid(row=2, column=0)
    Label(NewCharPage, text="Subclass: ", font=("Arial", 15)).grid(row=2, column=2)
    Label(NewCharPage, text="Race: ", font=("Arial", 15)).grid(row=3, column=0)
    Label(NewCharPage, text="Subrace:",font=("Arial", 15)).grid(row=4, column=0)
    Label(NewCharPage, text="Race Details:", font=("Arial", 15)).grid(row=4, column=2)
    Label(NewCharPage, text="Background: ", font=("Arial", 15)).grid(row=3, column=2)
    Label(NewCharPage, text="Str: ", font=("Arial", 15)).grid(row=5, column=0)
    Label(NewCharPage, text="Dex: ", font=("Arial", 15)).grid(row=5, column=2)
    Label(NewCharPage, text="Con: ", font=("Arial", 15)).grid(row=6, column=0)
    Label(NewCharPage, text="Int: ", font=("Arial", 15)).grid(row=6, column=2)
    Label(NewCharPage, text="Wis: ", font=("Arial", 15)).grid(row=7, column=0)
    Label(NewCharPage, text="Cha: ", font=("Arial", 15)).grid(row=7, column=2)
    Label(NewCharPage, text="Skill Proficiencies:",font=("Arial", 15)).grid(row=9, column=0)
    Tool_label = Label(NewCharPage, text="Tool Proficiencies:",font=("Arial", 15))
    Back_Label = Label(NewCharPage, text="Select Background",font=("Arial", 15))
    Back_Label.grid(row=3,column=4)

    # Function that finds background Attributes
    def Generate_Character_Attributes(char_dict):
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
        #Skill Proficiencies based on Background
        if char_dict[name.get()].background == "Acolyte":
            char_dict[name.get()].skill_prof.append("Insight")
            char_dict[name.get()].skill_prof.append("Religion")
        elif char_dict[name.get()].background == "Criminal/Spy":
            char_dict[name.get()].skill_prof.append("Deception")
            char_dict[name.get()].skill_prof.append("Stealth")
        elif char_dict[name.get()].background == "Folk Hero":
            char_dict[name.get()].skill_prof.append("Animal Handling")
            char_dict[name.get()].skill_prof.append("Survival")
        elif char_dict[name.get()].background == "Noble":
            char_dict[name.get()].skill_prof.append("History")
            char_dict[name.get()].skill_prof.append("Persuasion")
        elif char_dict[name.get()].background == "Solider":
            char_dict[name.get()].skill_prof.append("Athletics")
            char_dict[name.get()].skill_prof.append("Intimidation")
        elif char_dict[name.get()].background == "Sage":
            char_dict[name.get()].skill_prof.append("Arcana")
            char_dict[name.get()].skill_prof.append("History")
        #Set Skill scores
        str_skills = ["Athletics"]
        dex_skills = ["Acrobatics","Sleight of Hand","Stealth"]
        int_skills = ["Arcana","History","Investigation","Nature","Religion"]
        wis_skills=["Animal Handling","Insight","Medicine","Perception","Survival"]
        cha_skills =["Deception","Intimidation","Performance","Persuasion"]

        for prof in char_dict[name.get()].skill_prof:
            for skill in str_skills:
                if skill == prof:
                    char_dict[name.get()].skill_scores.append([prof,char_dict[name.get()].str_mod + char_dict[name.get()].proficiency])
                    str_skills.remove(skill)
        for prof in char_dict[name.get()].skill_prof:
            for skill in dex_skills:
                if skill in char_dict[name.get()].skill_prof:
                    char_dict[name.get()].skill_scores.append([prof,char_dict[name.get()].dex_mod + char_dict[name.get()].proficiency])
                    dex_skills.remove(skill)
        for prof in char_dict[name.get()].skill_prof:
            for skill in int_skills:
                if prof == skill:
                    char_dict[name.get()].skill_scores.append([prof, char_dict[name.get()].intell_mod + char_dict[name.get()].proficiency])
                    int_skills.remove(skill)
        for prof in char_dict[name.get()].skill_prof:
            for skill in wis_skills:
                if prof == skill:
                    char_dict[name.get()].skill_scores.append([prof,char_dict[name.get()].wis_mod + char_dict[name.get()].proficiency])
                    wis_skills.remove(skill)
        for prof in char_dict[name.get()].skill_prof:
            for skill in cha_skills:
                if prof == skill:
                    char_dict[name.get()].skill_scores.append([prof,char_dict[name.get()].cha_mod + char_dict[name.get()].proficiency])
                    cha_skills.remove(skill)

        for skill in str_skills:
            char_dict[name.get()].skill_scores.append( [skill, char_dict[name.get()].str_mod])
        for skill in dex_skills:
            char_dict[name.get()].skill_scores.append( [skill, char_dict[name.get()].dex_mod])
        for skill in int_skills:
            char_dict[name.get()].skill_scores.append( [skill, char_dict[name.get()].intell_mod])
        for skill in wis_skills:
            char_dict[name.get()].skill_scores.append([skill, char_dict[name.get()].wis_mod])
        for skill in cha_skills:
            char_dict[name.get()].skill_scores.append([skill, char_dict[name.get()].cha_mod])

        char_dict[name.get()].skill_scores.sort(key=lambda x: x[0])

    def Race_Bonus(char_dict):
        if char_dict[name.get()].race == "Dragonborn":
            char_dict[name.get()].cha_ += 1
            char_dict[name.get()].str_ += 2
            char_dict[name.get()].languages.append("Draconic")
            if char_dict[name.get()].subrace == " Black" or "Copper":
                char_dict[name.get()].spells.append("Acid Breath")
                char_dict[name.get()].resistance.append("Acid")
            elif char_dict[name.get()].subrace == " Blue" or "Bronze":
                char_dict[name.get()].spells.append("Lightning Breath")
                char_dict[name.get()].resistance.append("Lightning")
            elif char_dict[name.get()].subrace == "Brass" or "Gold" or "Red":
                char_dict[name.get()].spells.append("Fire Breath")
                char_dict[name.get()].resistance.append("Fire")
            elif char_dict[name.get()].subrace == "Green":
                char_dict[name.get()].spells.append("Poison Breath")
                char_dict[name.get()].resistance.append("Poison")
            else:
                char_dict[name.get()].spells.append("Cold Breath")
                char_dict[name.get()].resistance.append("Cold")
        if char_dict[name.get()].race == "Dwarf":
            char_dict[name.get()].resistance.append("Poison")
            char_dict[name.get()].darkvision = 60
            char_dict[name.get()].speed = 25
            char_dict[name.get()].langiages.append("Dwarvish")
            char_dict[name.get()].weapon_prof.append("Battleaxe","Handaxe","Light Hammer","Warhammer")
            char_dict[name.get()].tool_prof.append(dwarfToolVar)
            if char_dict[name.get()].subrace == "Mountian":
                char_dict[name.get()].armor_prof.append("Light","Medium")
            else:
                x = 1
                while x < char_dict[name.get()].level:
                    char_dict[name.get()].HP += 1
        if char_dict[name.get()].race == "Elf":
            char_dict[name.get()].adv.append("Charm")
            char_dict[name.get()].darkvision = 60
            char_dict[name.get()].skill_prof.append("Perception")
            char_dict[name.get()].languages.append("Elven")
            char_dict[name.get()].con_ += 2
            if char_dict[name.get()].subrace == "Wood":
                char_dict[name.get()].weapon_prof.extend(("Longsword","Shortsword","Longbow","Shortbow"))
                char_dict[name.get()].speed = 35
                char_dict[name.get()].wis_ += 1
            elif char_dict[name.get()].subrace == "High":
                char_dict[name.get()].weapon_prof.extend(("Longsword", "Shortsword", "Longbow", "Shortbow"))
                char_dict[name.get()].languages.append(raceLangVar)
                char_dict[name.get()].spells.append(highSpellVar)
                char_dict[name.get()].int_ += 1
            else:
                char_dict[name.get()].darkvision = 120
                char_dict[name.get()].weapon_prof.extend(("Rapier","SHhrtsword","Hand Crossbow"))
                char_dict[name.get()].spells.append("Dancing Lights")
                char_dict[name.get()].cha_ += 1
                if char_dict[name.get()].level > 2:
                    char_dict[name.get()].spells.append("Faire Fire")
                if char_dict[name.get()].level > 4:
                    char_dict[name.get()].spells.append("Darkness")
        if char_dict[name.get()].race == "Gnome":
            char_dict[name.get()].speed = 25
            char_dict[name.get()].darkvision = 60
            char_dict[name.get()].int_ += 2
            char_dict[name.get()].languages.append("Gnomish")
            char_dict[name.get()].adv.append("Int, Wis, Cha against magic")
            if char_dict[name.get()].subrace == "Rock":
                char_dict[name.get()].con_ += 1
                char_dict[name.get()].spells.append("Minor Illusion")
            else:
                char_dict[name.get()].tool_prof.append("Tinkers")
                # Also earn the Tinker ability (Not sure how to handle that yet)
        if char_dict[name.get()].race == "Half-Elf":
            for x in halfelfbox.curselection():
                char_dict[name.get()].skill_prof.append(halfelfbox.get(x))
            for x in halfelfbox2.curselection():
                if x == "Str":
                    char_dict[name.get()].str_ += 1
                elif x == "Dex":
                    char_dict[name.get()].dex_ += 1
                elif x == "Con":
                    char_dict[name.get()].con_ += 1
                elif x == "Wis":
                    char_dict[name.get()].wis_ += 1
                elif x == "Int":
                    char_dict[name.get()].int_ += 1
            char_dict[name.get()].cha_ += 2
            char_dict[name.get()].darkvision = 60
            char_dict[name.get()].languages.extend(("Elven",raceLangVar))
            char_dict[name.get()].adv.append("Magically Charmed")
        if char_dict[name.get()].race == "Halfling":
            char_dict[name.get()].dex_ += 2
            char_dict[name.get()].speed = 25
            char_dict[name.get()].adv.append("Frightened")
            char_dict[name.get()].languages.append("Halfling")
            char_dict[name.get()].feats.append("Lucky")
            if char_dict[name.get()].subrace == "Stout":
                char_dict[name.get()].adv.append("Poison")
                char_dict[name.get()].con_ += 1
            else:
                char_dict[name.get()].cha_ += 1
        if char_dict[name.get()].race == "Half-Orc":
            char_dict[name.get()].darkvision = 60
            char_dict[name.get()].languages.append("Orcish")
            char_dict[name.get()].skill_prof.append("Intimidation")
            char_dict[name.get()].feats.extend(("Relentless Endurance","Savage Attacks"))
            char_dict[name.get()].str_ += 2
            char_dict[name.get()].con_ += 1
        if char_dict[name.get()].race == "Human":
            char_dict[name.get()].languages.append(raceLangVar)
            if char_dict[name.get()].subrace == "Human":
                char_dict[name.get()].str_ += 1
                char_dict[name.get()].dex_ += 1
                char_dict[name.get()].con_ += 1
                char_dict[name.get()].wis_ += 1
                char_dict[name.get()].int_ += 1
                char_dict[name.get()].cha_ += 1
            else:
                for x in vhumanScoreBox.curselection():
                    if x == "Str":
                        char_dict[name.get()].str_ += 1
                    elif x == "Dex":
                        char_dict[name.get()].dex_ += 1
                    elif x == "Con":
                        char_dict[name.get()].con_ += 1
                    elif x == "Wis":
                        char_dict[name.get()].wis_ += 1
                    elif x == "Int":
                        char_dict[name.get()].int_ += 1
                    elif x == "Cha":
                        char_dict[name.get()].cha_ += 1
                char_dict[name.get()].feats.append(raceFeatVar)
                char_dict[name.get()].skills_prof.append(raceSkillVar)
        if char_dict[name.get()].race == "Tiefling":
            char_dict[name.get()].int_ += 1
            char_dict[name.get()].cha_ += 2
            char_dict[name.get()].darkvision = 60
            char_dict[name.get()].resistance.append("Fire")
            char_dict[name.get()].languages.append("Infernal")
        if char_dict[name.get()].race == "Leonin":
            char_dict[name.get()].speed = 35
            char_dict[name.get()].darkvision = 60
            char_dict[name.get()].languages.append("Leonin")
            char_dict[name.get()].weapons.extend("Claws","Roar")
            char_dict[name.get()].skill_prof.append(raceSkillVar)
        if char_dict[name.get()].race == "Satyr":
            char_dict[name.get()].dex_ += 1
            char_dict[name.get()].cha_ += 2
            char_dict[name.get()].speed = 35
            char_dict[name.get()].weapon.append("Ram")
            char_dict[name.get()].skill_prof.extend(("Performanace","Persuasion"))
            char_dict[name.get()].adv.append("Magic")
            char_dict[name.get()].feats.append("Mirthful Leaps")
            char_dict[name.get()].languages.append("Sylvan")
            char_dict[name.get()].tool_prof.append(raceSkillVar)

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
        if char_dict[name.get()].int_<= 6:
            modifiers.append(-2)
        elif char_dict[name.get()].int_== 8 or char_dict[name.get()].int_== 9:
            modifiers.append(-1)
        elif char_dict[name.get()].int_== 10 or char_dict[name.get()].int_== 11:
            modifiers.append(0)
        elif char_dict[name.get()].int_== 12 or char_dict[name.get()].int_== 13:
            modifiers.append(1)
        elif char_dict[name.get()].int_== 14 or char_dict[name.get()].int_== 15:
            modifiers.append(2)
        elif char_dict[name.get()].int_== 16 or char_dict[name.get()].int_== 17:
            modifiers.append(3)
        elif char_dict[name.get()].int_== 18 or char_dict[name.get()].int_== 19:
            modifiers.append(4)
        elif char_dict[name.get()].int_== 20 or char_dict[name.get()].int_== 21:
            modifiers.append(5)
        elif char_dict[name.get()].int_== 22 or char_dict[name.get()].int_== 23:
            modifiers.append(6)
        elif char_dict[name.get()].int_== 24 or char_dict[name.get()].int_== 25:
            modifiers.append(7)
        elif char_dict[name.get()].int_== 26 or char_dict[name.get()].int_== 27:
            modifiers.append(8)
        elif char_dict[name.get()].int_== 28 or char_dict[name.get()].int_== 29:
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

    # Sets armor,weapon, tool prof,Saving Throws
    def Set_Class_Info(char_dict):
        if char_dict[name.get()].char_class == 'Barbarian':
            char_dict[name.get()].armor_prof = ['Light Armor','Medium Armor','Shields']
            char_dict[name.get()].weapon_prof = ['Simple Weapons','Martial Weapons']
            char_dict[name.get()].tool_prof = ['']
            char_dict[name.get()].save_prof = ['Strength','Constitution']
        elif char_dict[name.get()].char_class == 'Bard':
            char_dict[name.get()].armor_prof = ['Light Armor']
            char_dict[name.get()].weapon_prof = ['Simple Weapons','Hand Crossbows','Longswords','rapiers','Shortswords']
            char_dict[name.get()].save_prof = ['Dexterity','Charisma']
        elif char_dict[name.get()].char_class == 'Cleric':
            char_dict[name.get()].armor_prof = ['Light Armor','Medium Armor','Shields']
            char_dict[name.get()].weapon_prof = ['Simple Weapons']
            char_dict[name.get()].tool_prof = ['']
            char_dict[name.get()].save_prof = ['Wisdom', 'Charisma']
        elif char_dict[name.get()].char_class == 'Druid':
            char_dict[name.get()].armor_prof = ['Light Armor','Medium Armor','Shields']
            char_dict[name.get()].weapon_prof = ['Clubs','Daggers','Darts','Javelins','Maces','Quaterstaffs','Scimitars'
                ,'Sickles','Slings','Spears']
            char_dict[name.get()].tool_prof = ['Herbalism Kit']
            char_dict[name.get()].save_prof = ['Wisdom', 'Intelligence']
        elif char_dict[name.get()].char_class == 'Fighter':
            char_dict[name.get()].armor_prof = ['Light Armor','Medium Armor','Heavy Armor','Shields']
            char_dict[name.get()].weapon_prof = ['Simple Weapons','Martial Weapons']
            char_dict[name.get()].tool_prof = ['']
            char_dict[name.get()].save_prof = ['Strength','Constitution']
        elif char_dict[name.get()].char_class == 'Monk':
            char_dict[name.get()].armor_prof = ['']
            char_dict[name.get()].weapon_prof = ['Simple Weapons','Short Swords']
            char_dict[name.get()].save_prof = ['Strength','Dexterity']
        elif char_dict[name.get()].char_class == 'Paladin':
            char_dict[name.get()].armor_prof = ['Light Armor','Medium Armor','Heavy Armor','Shields']
            char_dict[name.get()].weapon_prof = ['Simple Weapons','Martial Weapons']
            char_dict[name.get()].tool_prof = ['']
            char_dict[name.get()].save_prof = ['Wisdom', 'Charisma']
        elif char_dict[name.get()].char_class == 'Rogue':
            char_dict[name.get()].armor_prof = ['Light Armor']
            char_dict[name.get()].weapon_prof = ['Simple Weapons', 'Hand Crossbows','Longswords','Rapiers','Shortswords']
            char_dict[name.get()].tool_prof = ['Thieves']
            char_dict[name.get()].save_prof = ['Dexterity', 'Intelligence']
        elif char_dict[name.get()].char_class == 'Ranger':
            char_dict[name.get()].armor_prof = ['Light Armor','Medium Armor','Shields']
            char_dict[name.get()].weapon_prof = ['Simple Weapons','Martial Weapons']
            char_dict[name.get()].tool_prof = ['']
            char_dict[name.get()].save_prof = ['Strength','Dexterity']
        elif char_dict[name.get()].char_class == 'Wizard':
            char_dict[name.get()].armor_prof = ['']
            char_dict[name.get()].weapon_prof = ['Daggers','Darts','Slings','Quaterstaffs','Light Crossbows']
            char_dict[name.get()].tool_prof = ['']
            char_dict[name.get()].save_prof = ['Intelligence','Wisdom']
        elif char_dict[name.get()].char_class == 'Warlock':
            char_dict[name.get()].armor_prof = ['Light Armor']
            char_dict[name.get()].weapon_prof = ['Simple Weapons']
            char_dict[name.get()].tool_prof = ['']
            char_dict[name.get()].save_prof = ['Wisdom','Charisma']
        elif char_dict[name.get()].char_class == 'Sorcerer':
            char_dict[name.get()].armor_prof = ['']
            char_dict[name.get()].weapon_prof = ['Daggers','Darts','Slings','Quaterstaffs','Light Crossbows']
            char_dict[name.get()].tool_prof = ['']
            char_dict[name.get()].save_prof = ['Constitution','Charisma']
        elif char_dict[name.get()].char_class == 'Artificer':
            char_dict[name.get()].armor_prof = ['Light Armor','Medium Armor','Shields']
            char_dict[name.get()].weapon_prof = ['Simple Weapons']
            tools = ['Thieves','Tinkers']
            for x in tools:
                char_dict[name.get()].tool_prof.append(x)
            char_dict[name.get()].save_prof = ['Constitution','Intelligence']
        elif char_dict[name.get()].char_class == 'Blood Hunter':
            char_dict[name.get()].armor_prof = ['Light Armor','Medium Armor','Shields']
            char_dict[name.get()].weapon_prof = ['Simple Weapons', 'Martial Weapons']
            char_dict[name.get()].tool_prof = ['Alchemists']
            char_dict[name.get()].save_prof = ['Dexterity','Intelligence']

    #Submits character and clears entry form
    def submit():
        # connect to db to add information

        char_dict[name.get()] = Character(name.get(), raceVar.get(), raceSpecVar.get(), classVar.get(), subclassVar.get(),backVar.get(), levelVar.get(),
                                          int(strstatVar.get()), int(dexstatVar.get()), int(constatVar.get()),
                                          int(wisstatVar.get()), int(intstatVar.get()), int(chastatVar.get()))

        for i in listbox.curselection():
            char_dict[name.get()].skill_prof.append(listbox.get(i))
        for x in musicbox.curselection():
            char_dict[name.get()].tool_prof.append(musicbox.get(x))
        Race_Bonus(char_dict)
        Set_Modifiers(char_dict)
        Generate_Character_Attributes(char_dict)
        Set_Class_Info(char_dict)

        name.delete(0, END)
        levelVar.set(Level_options[0])
        classVar.set(char_class_options[0])
        subclassVar.set(char_subclass_options[0])
        raceVar.set(race_options[0])
        raceSpecVar.set(race_spec_options[0])
        backVar.set(back_options[0])
        strstatVar.set(stdarr_stats_options[0])
        constatVar.set(stdarr_stats_options[0])
        dexstatVar.set(stdarr_stats_options[0])
        intstatVar.set(stdarr_stats_options[0])
        wisstatVar.set(stdarr_stats_options[0])
        chastatVar.set(stdarr_stats_options[0])
        listbox.selection_clear(0, 'end')


        Label(NewCharPage, text="Character Successfully Added. You may now enter another character or exit the page ",
              font=('arial', 15), bg='yellow').place(relx=0.15, rely=0.7)

    Button(NewCharPage, text="Create Character", command=submit, height=3, width=25,background='red').place(relx=0.3, rely=0.5)
    Class_Image = Label(NewCharPage, image='',borderwidth=0, highlightthickness=0)
    Class_Image.place(relx=0.0, rely=0.6)
    Race_Image = Label(NewCharPage, image='', borderwidth=0, highlightthickness=0)
    Race_Image.place(relx=0.5,rely=0.6)


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
        subraceLabel.pack_forget()
        raceLabel.pack_forget()
        classLabel.pack_forget()
        levelLabel.pack_forget()
        Label(ViewCharPage, text="AC:" + str(char_dict[set_name.get()].AC), background='black', foreground='red').place(relx=0.0, rely=0.1)
        Label(ViewCharPage, text="HP:", background='black', foreground='red').place(relx=0.2, rely=0.1)
        curr_HP = tk.IntVar()
        curr_HP.set(char_dict[set_name.get()].current_HP-.1)
        if char_dict[set_name.get()].subrace != 'None':
            subraceLabel.config(text=char_dict[set_name.get()].subrace)
            subraceLabel.place(relx=0.4, rely=0.1)
        raceLabel.config(text=char_dict[set_name.get()].race)
        raceLabel.place(relx=0.5, rely=0.1)
        classLabel.config(text=char_dict[set_name.get()].char_class)
        classLabel.place(relx=0.6, rely=0.1)
        levelLabel.config(text="Level: " + str(char_dict[set_name.get()].level))
        levelLabel.place(relx=0.7, rely=0.1)
        #Works but very hard to see as it is Grey on Grey no bueno
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
        Label(ViewCharPage, text="Skills:\n", background='black',foreground='red').place(relx=0.2,rely=0.17)
        x=0.2
        for i in char_dict[set_name.get()].skill_scores:
            Label(ViewCharPage,text= i,background='black',foreground='red').place(relx=0.2,rely=x)
            x += 0.03

    Label(ViewCharPage, text="Your Character", fg='red', bg='black', font=('arial', 15)).place(relx=0.0, rely=0.0)
    char_select = OptionMenu(ViewCharPage, set_name, *name_list, command=selected)
    char_select.place(relx=0.2, rely=0.0)
    Button(ViewCharPage, text="Play as this character", command=lambda : Play_Class_Select(char_dict[set_name.get()])).place(relx=0.35, rely=0.0)
    subraceLabel = Label(ViewCharPage, text='', background='black', foreground='red')
    raceLabel = Label(ViewCharPage, text='', background='black', foreground='red')
    classLabel = Label(ViewCharPage, text='', background='black', foreground='red')
    levelLabel = Label(ViewCharPage, text='', background='black', foreground='red')


try:
    infile = "characters.pkl"
    with open(infile, 'rb') as in_strm:
        char_dict = dill.load(in_strm)

except:
    pass

Label(Menu, text="Welcome Legends!", bg="Black", fg="red", font=('arial', 20)).place(relx=0.35, rely=0.0)
#main_dnd = PIL.Image.open('d20.png')
resize_main_dnd = main_dnd.resize((600, 500))
main_dnd_ref = PIL.ImageTk.PhotoImage(resize_main_dnd)
Label(Menu, image=main_dnd_ref, borderwidth=0, highlightthickness=0).place(relx=0.1, rely=0.1)
# Buttons to import a character or view a character
Menu.title("Main Menu")
Menu.geometry("800x800")
Menu.configure(bg="black")

Button(Menu, text="Add a new Character", command=NewChar).place(relx=0.1, rely=0.8)
Button(Menu, text="View a Character", command=View).place(relx=0.7, rely=0.8)
Button(Menu, text="Exit", command=close).place(relx=0.9, rely=0.0)
Menu.mainloop()
