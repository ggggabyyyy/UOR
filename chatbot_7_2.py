#!/usr/bin/env python3

# coding: utf8

# Nom ...... : chatbot_7_2
# Rôle ..... : Chatbot qui répond à quelques questions simples
# Version .. : V1 du 15/08/21
# Exercice . : 7.2
# Usage .... : Pour lancer le chatbot : python3 ./chatbot_7_2.py

from nltk.chat.util import Chat
from datetime import date
import locale
import tkinter
from tkinter import *


# définitit le langage pour l'heure locale
locale.setlocale(locale.LC_ALL, '')

# nom de l'exercice
NOM_CHATBOT = "Exercice 7.2 Mini-Projet"
    
# date de création du chatbot
NAISSANCE_CHATBOT = date(2021, 8, 15)


# retourne l'age du chatbot en jours
def get_age():
    age = date.today() - NAISSANCE_CHATBOT    
    return str(age.days)

# retourne la date du jour
def get_date():
    return date.today().strftime('%A %d %B %Y')


# Pour génerer les réponses du chatbot j'ai décidé d'utiliser la class Chat de nltk
# https://www.nltk.org/api/nltk.chat.html#nltk.chat.util.Chat
# J'ai définit les variables reflections et pairs qui servent à instancier un objet
# de la class Chat puis j'ai utilisé la méthode respond pour obtenir les réponse en fonction
# des messages de l'utilisateur


# les réflections sont utiles quand le chatbot répéte une phrase
# de l'utilisateur, il remplacera les expressions trouvées dans
# le dictionnaire reflections.
# ex: je n'ai pas envie de te parler => tu n'as pas envie de me parler

# les réflections sont utiles quand le chatbot répéte une phrase
# de l'utilisateur, il remplacera les expressions trouvées dans
# le dictionnaire reflections.
# ex: je n'ai pas envie de te parler => tu n'as pas envie de me parler

reflections = {
    "je n'ai": "tu n'as",
    "j'ai": "tu as",
    "ai": "as",
    "vais": "vas",
    "suis": "es",
    "j'": "tu",
    "je": "tu",
    "m'": "t'",
    "je voudrais": "tu voudrais",
    "serais": "seras",
    "mon": "ton",
    "me": "te",
    "mes": "tes",
    "nos": "vos",
    "notre": "votre",
    "ma": "ta",
    "mon": "ton",
    "moi": "toi",
    "le mien": "le tien",
    "les miens": "les tiens",
}

# On ajoute également les reflections inversent (ici de la 2ème personne vers la première)
# qui ne sont pas détectées automatiquement
reflections_inv = {}
for k, v in reflections.items():
    reflections_inv[v] = k
reflections_inv["t'es"] = "je suis"
reflections.update(reflections_inv)


# Le premier élèment de chaque pair est une expression régulière.
# Quand elle correspond à l'expression entrée par l'utilisateur la réponse 
# sera l'un des éléments du tuple de la pair choisi de manière aléatoire.
# Si plusieurs paires correspondent c'est la première trouvée qui sera utilisée.
# %n correspond au terme inclus entre la n-ième ouverture de parenthèse et sa fermeture corrspondante 

pairs=( 
    # dans le cas ou un nom ressemble à un pseudo, c'est à dire si il contient
    # des caractères spéciaux ou des chiffres.
    (
        r"(.*)([Mm]on (pré)?nom (c')?est|[Jj]e m'appelle) (([a-zA-Z]*[0-9&@~#$€£*<>()[\]\\-]+[a-zA-Z]*)+)(.*)",
        (
            "Enchanté %5 ! %5 c'est ton pseudo ou tu es une machine comme moi ?",
            "Ahah ! %5, ça n'est pas ton vrai prénom ça ?",
        )
    ),
    # si le nom semble normal
    (
        r"(.*)([Mm]on (pré)?nom (c')?est|[Jj]e m'appelle) ([a-zA-Z]+)(.*)",
        (
            "Ok ! Ravi de faire ta connaissance :)",
            "Enchanté $5 !",
        )
    ),
    (
        r"(.*)([çc]a va| je vais (très)? bien) et toi(.*)",
        (
            "Oui ça va :) merci!",
            "Ca peut aller. Que vas tu faire de ta journée ?",            
        )
    ),   
    (
        r"(.*)([Bb]on(jour|soir)|[Ss]alut|[Cc]oucou|Hh]ello|[Hh]ey)?(.*)([çcC]a va|[cC]omment (vas[\s-]tu|tu vas))[^.!]*\?",
        (
            "Salut, ça va et toi ?",
            "Hey, je vais très bien ! et toi ?",
        )
    ),
    (
        r"(.*)(je vais (très )?bien|[Ccç]a va)(.*)",
        (
            "Super, je suis content de l'apprendre !",
            "Cool",
            "Tant mieux",
        )
    ),
    (
        r"(.*)([Bb]onjour|[Cc]oucou|Hh]ello)(.*)",
        (
            "Bonjour !",
            "Salut !",
            "Hey !",
        )
    ),
    (
        r"(.*)([Aa]u revoir|[Aaà] (bient[ôo]t|plus|\+|la prochaine)|[Cc]iao)(.*)",
        (
            "Salut. Ce fut un plaisir !",
        )
    ),
    (
        r"(.*)([Cc]'est quoi ton (pré|sur)?nom|[Tt]u t'appelles comment)(.*)",
        (
            "Je m'appelle "+NOM_CHATBOT+" !",          
        )
    ),
    (
        r"(.*)[Ss]alut(.*)",
        (    
            "Salut !",
        )
    ),
    (
        r"(.*)([Tt]u as quel|[Cc]'est quoi ton) [âa]ge(.*)",
        (
            "J'ai "+get_age()+" jours !",          
        )
    ),
    (
        r"(.*)([Qq]uelle est la date aujourd'hui|[Nn]ous sommes quel jour)(.*)",
        (
            "Aujourd'hui nous sommes le "+get_date(),
        )
    ),
    (
        "(.*)[Jj]e (pense|trouve) (que|qu'il|qu'elle) (.*)(\.?)",
        (
            "Tu %2s vraiment %3 %4?",
        )
    ),
    (
        r"(.*)[Pp]ourquoi ([^.!]*)\?(.*)",
        (
            "Je ne sais pas pourquoi %2, désolé.",
        )
    ),
    # Si c'est une question qui ne correspondait à aucun cas
    (
        r"(.*)\?(.*)",
        (
            "Je n'en ai aucune idée. Désolé...",
            "Je ne sais pas.",
            "On n'en reparle une prochaine fois ? La je n'ai pas les idées claires."
        )
    ),
    (
        r"^[Oo]ui",
        (
            "Ok !",
        )
    ),
    # Dans tous les autres cas
    (
        r"(.*)",
        (
            "Ok, je vois.",
            "C'est intéressant.",
        )
    )
)


# On instancie l'objet avec les pairs et les reflections
chatbot = Chat(pairs, reflections)


# Pour l'interface TKinter j'ai repris le code utiliser dans
# https://towardsdatascience.com/how-to-create-a-chatbot-with-python-deep-learning-in-less-than-an-hour-56a063bdfc44

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))

        # on récupère la réponse au message de l'objet chatbot
        res = chatbot.respond(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        

base = Tk()
base.title("Chatbot 7.2")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

# base.mainloop()
if __name__ == '__main__':
    base.mainloop()