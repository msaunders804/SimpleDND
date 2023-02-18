from tkinter import *
import tkinter as tk

def Play_Class_Select(char):
    if char.char_class == "Barbarian":
        Barbarian(char)
    '''elif char.char_class == "Bard":
        Bard(char)
    elif char.char_class == "Paladin":
        Paladin(char)
    elif char.char_class == "Ranger":
        Ranger(char)
    elif char.char_class == "Rogue":
        Rogue(char)
    elif char.char_class == "Wizard":
        Wizard(char)
    elif char.char_class == "Warlock":
        Warlock(char)
    elif char.char_class == "Sorcerer":
        Sorcerer(char)
    elif char.char_class == "Artificer":
        Artificer(char)
    elif char.char_class == "Blood Hunter":
        Blood(char)
    else:
        #Write a function that basically kills them if they somehow break this shit
        Dragon_Attack()'''
def Barbarian(character):
    BarbarianPage = Tk()
    BarbarianPage.title("Barbarian")
    BarbarianPage.geometry("800x800")
    BarbarianPage.configure(bg="black")
    BarbarianPage.attributes('-topmost', True)

    BarbarianPage.mainloop()

'''def Bard():
    
def Paladin():
    
def Ranger():
    
def Rogue():
    
def Wizard():
    
def Warlock():
    
def Sorcerer():
    
def Artificer():
    
def Blood():





Label(ViewCharPage, text="AC:" + str(char_dict[set_name.get()].AC), background='black', foreground='red').place(
    relx=0.0, rely=0.1)
Label(ViewCharPage, text="HP:", background='black', foreground='red').place(relx=0.2, rely=0.1)
curr_HP = tk.IntVar()
curr_HP.set(char_dict[set_name.get()].current_HP - .1)
# Works but very hard to see as it is Grey on Grey
s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", background='red')
print(curr_HP.get())
ttk.Progressbar(ViewCharPage, style="red.Horizontal.TProgressbar", maximum=char_dict[set_name.get()].HP,
                variable=curr_HP, orient=tk.HORIZONTAL).place(relx=0.24, rely=0.1)
# Stats
Label(ViewCharPage, text="STR\n" + str(char_dict[set_name.get()].str_mod), background='black', foreground='red',
      borderwidth=1, relief="solid").place(relx=0.0, rely=0.2)
Label(ViewCharPage, text="CON\n" + str(char_dict[set_name.get()].con_mod), background='black', borderwidth=1,
      relief="solid",
      foreground='red').place(relx=0.0, rely=0.3)
Label(ViewCharPage, text="DEX\n" + str(char_dict[set_name.get()].dex_mod), background='black', borderwidth=1,
      relief="solid",
      foreground='red').place(relx=0.0, rely=0.4)
Label(ViewCharPage, text="WIS\n" + str(char_dict[set_name.get()].wis_mod), background='black', borderwidth=1,
      relief="solid",
      foreground='red').place(relx=0.0, rely=0.5)
Label(ViewCharPage, text="INT\n" + str(char_dict[set_name.get()].intell_mod), background='black', borderwidth=1,
      relief="solid",
      foreground='red').place(relx=0.0, rely=0.6)
Label(ViewCharPage, text="CHA\n" + str(char_dict[set_name.get()].cha_mod), background='black', borderwidth=1,
      relief="solid",
      foreground='red').place(relx=0.0, rely=0.7)
'''