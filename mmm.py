import networkx as nx
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import random
from PIL import Image, ImageTk, ImageSequence

def IC(D:nx.Graph(),p:float,initial):  # type: ignore
    dico_etat  = { a:"ignorant" for a in D.nodes() } # Creer un dictionnaire avec touts les etats de noeuds ignorant
    source = random.sample(list(D.nodes()),min(initial,D.number_of_nodes()))#Tire au hasard "initial" noeuds 
    arrettab = [list(D.edges())[0]] #initialisation de la liste des arrets
    

    for a in source:
        dico_etat[a] = "diffuseur" #Si ce trouve dans source on change directement l'etat

    
    historique = [infecte_lister (dico_etat)]#historique initialisation première vague
    courbe =[compteur(dico_etat)]

    if p > 0.0:
        while set(source):#tant qu'il y des sources (si source vide set renvoie false)
            source_nouve = [] # pour arrêter la boucle
            arrettabinf = []
            for noeuds in source: #on balaye les noeuds source
                for voisin in D.neighbors(noeuds):#on inspecte chaque voisin de chaque noeuds sources
                    if dico_etat[voisin] == "ignorant":#si il est ignorant on change l'etat on diffuseur 
                        if random.random() < p :
                            dico_etat[voisin] = "diffuseur"
                            source_nouve.append(voisin)#on ajoute dans source_nouv pour enregistrer les nouveaus source plus tard
                            if noeuds < voisin: 
                                arrettabinf.append((noeuds,voisin))
                            elif noeuds > voisin:  
                                arrettabinf.append((voisin,noeuds))

            #pour pouvoir utiliser les nouveaux source tout en ignorant celui utilisés précedemment
            #si il n'y a plus d'ignorant, il n'y a pas de (source_nouve.append(voisin)) alors source_nouve reste vide
            arrettab.append(arrettabinf)
            source = source_nouve
            historique.append(infecte_lister (dico_etat))
            courbe.append(compteur(dico_etat))

    return historique,arrettab,courbe

def RIS(D:nx.Graph(),p:float,q:float,initial):#type:ignore
    dico_etat = {noeuds : "ignorant" for noeuds in D.nodes()}
    source = random.sample(list(D.nodes()),min(initial,D.number_of_nodes()))
    arrettab = [list(D.edges())[0]]

    for o in source:
        dico_etat[o] = "diffuseur"

    history = [infecte_lister(dico_etat)]
    historique = [lasser_lister(dico_etat)]   
    courbe  = [compteurbis(dico_etat)]

    if p == 0.0:
        while "diffuseur" in dico_etat.values() and q!=0.0:    
            for o in source: 
                if random.random()<q:
                    dico_etat[o] = "lasser"

            history.append(infecte_lister(dico_etat))
            historique.append(lasser_lister(dico_etat))
            courbe.append(compteurbis(dico_etat))
            arrettab.append(list(D.edges())[0])
    
   

    if p>0.0:
        
        while "diffuseur" in dico_etat.values():
            arrettabinf = []
                    
            nouv = dict(dico_etat)

            
            for noeuds,v in dico_etat.items():
                pr = False
                if v != "diffuseur":
                    continue

                
                for voisin in D.neighbors(noeuds):
                    if nouv[voisin] =="ignorant":
                        if random.random()<p :
                            nouv[voisin] = "diffuseur"
                            if noeuds < voisin: 
                                arrettabinf.append((noeuds,voisin))
                            elif noeuds > voisin:  
                                arrettabinf.append((voisin,noeuds))
                    else:   
                        pr = True
                if pr:
                    if random.random()<q:
                        nouv[noeuds] = "lasser"
                    else:
                        for voisin in D.neighbors(noeuds):
                            if random.random()<p :
                                if noeuds < voisin: 
                                        arrettabinf.append((noeuds,voisin))
                                elif noeuds > voisin:  
                                        arrettabinf.append((voisin,noeuds))

                
           
            arrettab.append(arrettabinf)
            dico_etat= nouv
            history.append(infecte_lister(dico_etat))
            historique.append(lasser_lister(dico_etat))
            courbe.append(compteurbis(dico_etat))
            

            if len(history) > 500 or ("ignorant" not in dico_etat.values() and q == 0.0):  # garde-fou contre une boucle infinie improbable
                break
    return history,historique,arrettab,courbe



def infecte_lister (dico_etat):
    history = []
    for k,v in dico_etat.items():
        if v == "diffuseur" : 
            history.append(k)
    return history

def lasser_lister (dico_etat):
    history = []
    for k,v in dico_etat.items():
        if v == "lasser" : 
            history.append(k)
    return history



def animate_propagation(G,history,arrettab,pos, filename):
    fig, ax = plt.subplots(figsize=(8, 6))
    def update(frame):
        ax.clear()
        ax.set_facecolor("black")
        active = history[frame]
        arr    = arrettab[frame]

        colors_arr = ['red' if n in arr else 'lightgray'  for n in G.edges()]
        colors_nodes = ['red' if n in active else 'lightblue'  for n in G.nodes()]

        nx.draw(G, pos, ax=ax, node_color=colors_nodes,edge_color=colors_arr,with_labels=True, node_size=300)
        ax.set_title(f"Etape {frame}")

        legend_elements = [
            mp.Patch(color = "red",label = "Diffuseur"),
            mp.Patch(color = "lightblue",label = "Ignorants"),
        ]
        ax.legend(handles= legend_elements ,loc = "upper right")  
           
    anim = FuncAnimation(fig, update, frames=len(history),interval=1000, repeat=False)
    anim.save(filename, writer=PillowWriter(fps=1))
    plt.close()

def animate_propagationbis(G,historique,history,arrettab,pos, filename):
    fig, ax = plt.subplots(figsize=(8, 6))
    def update(frame):
        ax.clear()
        ax.set_facecolor("black")
        active = historique[frame]
        lasser = history[frame]
        arr    = arrettab[frame]
        colors_arr = ['red' if n in arr else 'lightgray'  for n in G.edges()]
        colors_nodes = ['red' if n in active else 'green' if n in lasser else "lightblue"  for n in G.nodes()]
        nx.draw(G, pos, ax=ax, node_color=colors_nodes,edge_color=colors_arr,with_labels=True, node_size=300)
        ax.set_title(f"Etape {frame}")
        legend_elements = [
            mp.Patch(color = "red",label = "Diffuseur"),
            mp.Patch(color = "green",label = "Lasser"),
            mp.Patch(color = "lightblue",label = "Ignorants"),
        ]
        ax.legend(handles=legend_elements,loc = "upper right")
        
        
    anim = FuncAnimation(fig, update, frames=len(history),interval=1000, repeat=False)
    anim.save(filename, writer=PillowWriter(fps=1))
    plt.close()


def compteur(dico_etat):
    diffuseur = 0
    ignorant = 0
    for etats in dico_etat.values():
        if etats == "diffuseur":
            diffuseur +=1
        elif etats == "ignorant":
            ignorant +=1

    return { "diffuseur":diffuseur, "ignorant" : ignorant}



def compteurbis(dico_etat:dict):
    diffuseur = 0
    ignorant = 0
    lasser = 0
    for etats in dico_etat.values():
        if etats == "diffuseur":
            diffuseur +=1
        elif etats == "ignorant":
            ignorant +=1
        elif etats == "lasser":
            lasser +=1

    return { "diffuseur":diffuseur, "ignorant" : ignorant,"lasser":lasser}


def tracer_evolution_temporellebis(historique: list):
    """Trace l'évolution du nombre d'ignorants/diffuseurs/lassés au fil du temps."""
    etapes = list(range(len(historique)))
    ignorants = [h["ignorant"] for h in historique]
    diffuseurs = [h["diffuseur"] for h in historique]
    lasses = [h["lasser"] for h in historique]

    fig, ax = plt.subplots()
    ax.plot(etapes, ignorants, label="Ignorants", color="lightblue")
    ax.plot(etapes, diffuseurs, label="Diffuseurs", color="red")
    ax.plot(etapes, lasses, label="Lassés", color="green")
    plt.xlabel("Étape de simulation")
    plt.ylabel("Nombre d'utilisateurs")
    plt.title("Évolution de la propagation de l'information dans le réseau")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig

def tracer_evolution_temporelle(historique: list):
    """Trace l'évolution du nombre d'ignorants/diffuseurs/lassés au fil du temps."""
    etapes = list(range(len(historique)))
    ignorants = [h["ignorant"] for h in historique]
    diffuseurs = [h["diffuseur"] for h in historique]
    
    fig, ax = plt.subplots()
    ax.plot(etapes, ignorants, label="Ignorants", color="lightblue")
    ax.plot(etapes, diffuseurs, label="Diffuseurs", color="red")
    plt.xlabel("Étape de simulation")
    plt.ylabel("Nombre d'utilisateurs")
    plt.title("Évolution de la propagation de l'information dans le réseau")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig

def tracer_evolution_temporelle_cinem(historique: list,step:int  = 0):
    """Trace l'évolution du nombre d'ignorants/diffuseurs/lassés au fil du temps."""
    
    his = []
    for i in range(step):
        his.append(historique[i])

    etapes = list(range(len(his)))
    ignorants = [h["ignorant"] for h in his]
    diffuseurs = [h["diffuseur"] for h in his]
    
    fig, ax = plt.subplots()
    ax.plot(etapes, ignorants, label="Ignorants", color="lightblue")
    ax.plot(etapes, diffuseurs, label="Diffuseurs", color="red")
    plt.xlabel("Étape de simulation")
    plt.ylabel("Nombre d'utilisateurs")
    plt.title("Évolution de la propagation de l'information dans le réseau")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def tracer_evolution_temporelle_cinembis(historique: list,step:int  = 0):
    """Trace l'évolution du nombre d'ignorants/diffuseurs/lassés au fil du temps."""
    
    his = []
    for i in range(step):
        his.append(historique[i])

    etapes = list(range(len(his)))
    ignorants = [h["ignorant"] for h in his]
    diffuseurs = [h["diffuseur"] for h in his]
    lasses = [h["lasser"] for h in his]

    fig, ax = plt.subplots()
    ax.plot(etapes, ignorants, label="Ignorants", color="lightblue")
    ax.plot(etapes, diffuseurs, label="Diffuseurs", color="red")
    ax.plot(etapes, lasses, label="Lassés", color="green")
    plt.xlabel("Étape de simulation")
    plt.ylabel("Nombre d'utilisateurs")
    plt.title("Évolution de la propagation de l'information dans le réseau")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig