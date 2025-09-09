from tkinter import *
import keyboard
import requests
import json
from time import sleep

root = Tk()
root.attributes("-fullscreen", True)     # plein écran
root.configure(bg="black")               # fond noir
root.attributes("-topmost", True)        # toujours au-dessus

pi_file = 'pi.txt'
config_file = 'config.json'

global win
win = False

class Config:
    def __init__(self):
        try :
            with open(config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)

                cles = self.config.keys()     
                    
                for cle in cles :
                    setattr(self, cle, self.config.get(cle))
        except FileNotFoundError :
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump({'score':0}, f, ensure_ascii=False, indent=4)
                setattr(self, "score", 0)
    
    def updtadeConfig(self, key, value) :
        self.key = value
        self.config[key] = value
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
            
                
config = Config()

def update_pi(limit = 1, start=1) :
   i = start
   open(pi_file, 'w').write('')
   print("0000")
   c = 0

   while True :
        reponse = requests.get(f"https://www.piday.org/wp-json/millionpi/v1/million?action=example_ajax_request&page={i}")
        if reponse.status_code != 200 or c == limit :
            break
        else :
            print(f"{i:04}")
            open(pi_file, 'a').write(reponse.text.replace('"', '').removeprefix('3.'))
        i += 1
        c += 1

def get_pi(n_terms: int) -> tuple:
    # Lire les X premières décimals de pi
    with open(pi_file, "r", encoding="utf-8") as f:
        return f.read(n_terms)

def get_next_term(pos: int) -> tuple:
    # Lire la Xe décimal de pi
    with open(pi_file, "r", encoding="utf-8") as f:
        f.seek(pos-1)
        return f.read(1)

def check_unlock():
    # Si Ctrl + Shift + L est pressé → quitter
    if keyboard.is_pressed("ctrl+shift+l"):
        root.destroy()
    else:
        root.after(100, check_unlock)  # revérifie dans 100ms

def show(text="", color="red") :
    Result.config(text=text, fg=color)

def valider(*events) :
    global win

    if win :
        root.destroy()
        quit()

    value = input.get()

    if len(value) < config.score :
        show("Tu a déja fait mieux, tu dois le refaire.")
        return
    
    if value == get_pi(len(value))  :
        config.updtadeConfig('score', len(value))
        show(f"Tu a gagné, décimal suivante : {get_next_term(len(value) + 1)}", "green")
        win = True
    else : 
        show("Tu t'es trompé")

# Bloquer Alt+F4
root.protocol("WM_DELETE_WINDOW", lambda: None)

# Vérifie régulièrement la combinaison secrète
check_unlock()

EntryFrame = Frame(root, bd=0)
EntryFrame.place(relx=0.5, rely=0.5, anchor="center")

Label(EntryFrame, text='3.', fg="white", bg="black", font=("Consolas", 40)).pack(side=LEFT)

input = Entry(EntryFrame, fg="white", bg="black", font=("Consolas", 40), bd=0, insertbackground="white", highlightthickness=2, highlightbackground="black", highlightcolor="black")
input.pack(side=RIGHT, ipady=0)
input.focus_set()
input.bind("<Return>", valider)

Result = Label(root, text='', fg="red", bg="black", font=("Consolas", 20))
Result.place(relx=0.5, rely=0.55, anchor="center")

root.mainloop()
