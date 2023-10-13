import matplotlib.pyplot as plt
from landfiles import LandfilesClient 
import tkinter as tk

#%% gui




def on_submit():
    global username, password, basic_token
    username = entry_username.get()
    password = entry_password.get()
    basic_token = entry_basic_token.get()
    root.destroy()

def toggle_password_visibility():
    current_state = entry_password.cget("show")
    if current_state == "":
        entry_password.config(show="*")
        show_password_button.config(text="Afficher")
    else:
        entry_password.config(show="")
        show_password_button.config(text="Masquer")

root = tk.Tk()
root.title("Saisie de données")

tk.Label(root, text="Nom d'utilisateur:").grid(row=0, column=0)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1)

tk.Label(root, text="Mot de passe:").grid(row=1, column=0)
entry_password = tk.Entry(root, show="*")  
entry_password.grid(row=1, column=1)

# Bouton pour afficher/masquer le mot de passe
show_password_button = tk.Button(root, text="Afficher", command=toggle_password_visibility)
show_password_button.grid(row=1, column=2)  # Place le bouton à côté du champ de mot de passe

tk.Label(root, text="Basic Token:").grid(row=2, column=0)
entry_basic_token = tk.Entry(root)
entry_basic_token.grid(row=2, column=1)

submit_button = tk.Button(root, text="Soumettre", command=on_submit)
submit_button.grid(row=3, column=0, columnspan=2)

root.mainloop()



print("Nom d'utilisateur:", username)
print("Mot de passe:", password)
print("Basic Token:", basic_token)
#%% cnx API et extraction de la liste des goupes
client = LandfilesClient(username, password, basic_token)

groups=client.list_groups()

#%%exemple : extraire les datas du 1er groupe de la liste

df=groups[0].api_data

#%% extraction des observations du groupe

observations=groups[0].list_observations()

#%% préparation des données pour le graphique

    
#________________FONCTION____________________
    
def pts(data1, data2, data3):

    points = [
        {
            "x": obs.measures[A].value,
            "y": obs.measures[B].value,
            "label": obs.measures[C].value
        }
        for parcelId, parcel_observations in observations.items()
        for obs in parcel_observations
        if all(measure_type in obs.measures for measure_type in [A, B])
    ]

    x_values = [point["x"] for point in points]
    y_values = [point["y"] for point in points]
    text_values = [point["label"] for point in points]

    sorted_indices = sorted(range(len(x_values)), key=lambda k: x_values[k])


    x_values_sorted = [float(x_values[i]) for i in sorted_indices]
    y_values_sorted = [float(y_values[i]) for i in sorted_indices]
    text_values_sorted = [text_values[i] for i in sorted_indices]

    
    points = [
        {
            "x": x_values_sorted[i],
            "y": y_values_sorted[i],
            "label": text_values_sorted[i]
        }
        for i in range(len(points))
    ]

    return points


def graph_analyse (axe_y,axe_x,title,x,y,text):
    plt.figure()
    plt.scatter(x, y)
    
    for i, label in enumerate(text):
        plt.annotate(label, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')
   
    plt.xlabel(axe_ab)
    plt.ylabel(axe_ord)
    plt.title(title)
    plt.grid(True)
    plt.show()
#%%Exemple
def sauvegarder_donnees():
    global A, B, C, axe_ab, axe_ord, titre
    A = entry_A.get()
    B = entry_B.get()
    C = entry_C.get()
    axe_ab = entry_axe_ab.get()
    axe_ord = entry_axe_ord.get()
    titre = entry_titre.get()
    fenetre.destroy()
    


# Initialisation des variables
A = ""
B = ""
C = ""
axe_ab = ""
axe_ord = ""
titre = ""

fenetre = tk.Tk()
fenetre.title("Saisie de données")


label_A = tk.Label(fenetre, text="Valeur pour les X :")
label_A.pack()
entry_A = tk.Entry(fenetre)
entry_A.pack()

label_B = tk.Label(fenetre, text="Valeur pour les Y :")
label_B.pack()
entry_B = tk.Entry(fenetre)
entry_B.pack()

label_C = tk.Label(fenetre, text="Valeur pour les labels :")
label_C.pack()
entry_C = tk.Entry(fenetre)
entry_C.pack()

label_axe_ab = tk.Label(fenetre, text="Légende axe d'abscisses :")
label_axe_ab.pack()
entry_axe_ab = tk.Entry(fenetre)
entry_axe_ab.pack()

label_axe_ord = tk.Label(fenetre, text="Légende axe des ordonnées :")
label_axe_ord.pack()
entry_axe_ord = tk.Entry(fenetre)
entry_axe_ord.pack()

label_titre = tk.Label(fenetre, text="Titre du graphique :")
label_titre.pack()
entry_titre = tk.Entry(fenetre)
entry_titre.pack()


button_sauvegarde = tk.Button(fenetre, text="Valider", command=sauvegarder_donnees)
button_sauvegarde.pack()


fenetre.mainloop()

# Affichage des données que l'utilisateur les a rentrées

print("Valeur pour les X :", A)
print("Valeur pour les Y :", B)
print("Valeur pour les labels :", C)
print("Légende axe d'abscisses :", axe_ab)
print("Légende axe des ordonnées :", axe_ord)
print("Titre du graphique :", titre)


points= pts(A,B,C)

x_values = [point["x"] for point in points]
y_values = [point["y"] for point in points]
text_values = [point["label"] for point in points]

graph_analyse (axe_ab,axe_ord,titre,x_values,y_values,text_values)
