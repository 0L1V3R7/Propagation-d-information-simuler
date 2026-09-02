import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from mmm import animate_propagation, animate_propagationbis,IC,RIS,tracer_evolution_temporelle,tracer_evolution_temporellebis,tracer_evolution_temporelle_cinem, tracer_evolution_temporelle_cinembis

st.title("PROPAGATION D'INFORMATION")  
st.sidebar.header("PARAMETRE")


Lancer = st.sidebar.button("Launch")



slidenodes = st.sidebar.slider("Nombre de internaut",3,100)
slideegdes = st.sidebar.slider("Nombre de connexion par internaut ",1,slidenodes-1)


type = st.sidebar.selectbox("Type de propagation", ["Independant Cascade (IC)", "Susceptible-Infecté-Retiré (SIR)"])
cinem = st.sidebar.selectbox("Type de lecture ", ["Automatique","Manuel"])


D = nx.barabasi_albert_graph(slidenodes,slideegdes)

colon1,colon2 = st.columns(2)

filename="propagation.gif"
filenamebis="propagationbis.gif"



#Bloc de st.session_state
if "fig" not in st.session_state:
    st.session_state.fig = None

if "pos" not in st.session_state:
    st.session_state.pos = nx.spring_layout(D,seed = 42)

if "history" not in st.session_state:
    st.session_state.history = None

if "step" not in st.session_state:
    st.session_state.step = [[]]

if "stepbis" not in st.session_state:
    st.session_state.stepbis = [[]]

if "D" not in st.session_state:
    st.session_state.D = None

if "animate_propagation" not in st.session_state:
    st.session_state.animate_propagation = None

if "animate_propagationbis" not in st.session_state:
    st.session_state.animate_propagationbis = None


if "courbe" not in st.session_state:
    st.session_state.courbe = None


if "courbebis" not in st.session_state:
    st.session_state.courbebis = None

if "tab" not in st.session_state:
        st.session_state.tab = []


if "tabbis" not in st.session_state:
        st.session_state.tabbis = []


if "tabc" not in st.session_state:
        st.session_state.tabc = []


if "tabcbis" not in st.session_state:
        st.session_state.tabcbis = []




if type == "Independant Cascade (IC)":
    slidep = st.sidebar.slider("Propabilité de propagation",0.0,1.0,0.1)
    slides = st.sidebar.slider("Nombre de source",1,slidenodes)

    if Lancer:
        st.session_state.tab.clear()
        st.session_state.tabc.clear()
        st.session_state.D = D
        st.session_state.step = IC(st.session_state.D,slidep,slides)
        st.session_state.pos = nx.spring_layout(st.session_state.D ,seed=42)


        if st.session_state.step != [[]]  and st.session_state.pos is not None:
            for step in range( len(st.session_state.step[0])):
                    
                    nodes,edges,cs = st.session_state.step
                    node = nodes[step]
                    edge = edges[step]
                    fig,ax = plt.subplots(figsize = (8, 6))

                    color_n = [ "red" if n in node  else "lightblue" for n in st.session_state.D.nodes() ]
                    color_e = [ "red" if n in edge  else "lightgray" for n in st.session_state.D.edges() ]

                    nx.draw(st.session_state.D,st.session_state.pos,node_color=color_n,edge_color=color_e ,with_labels=True,ax = ax,node_size=200)

                    legend_elements = [
                    mp.Patch(color = "red",label = "Diffuseur"),
                    mp.Patch(color = "lightblue",label = "Ignorants"),
                    ]
                    ax.legend(handles= legend_elements ,loc = "upper right")  
                    ax.set_title(f"Etape {step}")
                    st.session_state.tab.append(fig)

                    figs = tracer_evolution_temporelle_cinem(cs,step)
                    st.session_state.tabc.append(figs)
                        
                            


                                            
        history,arret,courbe = st.session_state.step
        with st.spinner():
            st.session_state.animate_propagation = animate_propagation(st.session_state.D,history,arret,st.session_state.pos,filename)
            st.session_state.courbe = tracer_evolution_temporelle(courbe)
    with colon1 : 
        if st.session_state.step != [[]]  and st.session_state.pos is not None:
            if cinem == "Automatique":
                    st.image(filename,caption="Automatique")
    with colon2:
            if st.session_state.courbe is not None :
                if cinem == "Automatique":
                    st.pyplot(st.session_state.courbe)  

    with colon1 : 
        if st.session_state.step != [[]]  and st.session_state.pos is not None:
            if cinem == "Manuel":
                step = st.bottom.slider(
                "Étape",0,len(st.session_state.step[0]) - 1)
        
                st.pyplot(st.session_state.tab[step])
                plt.close(st.session_state.tab[step])

                with colon2:
                    if st.session_state.courbe is not None :
                        st.pyplot(st.session_state.tabc[step])
                        plt.close(st.session_state.tabc[step])
                        
                        
                    


if type == "Susceptible-Infecté-Retiré (SIR)":
    slidep = st.sidebar.slider("Propabilité de propagation",0.0,1.0,0.1)
    slideq  = st.sidebar.slider("Propabilité de lassitude",0.0,1.0,0.1)
    slides = st.sidebar.slider("Nombre de source",1,slidenodes)

    if Lancer:
        st.session_state.tabbis.clear()
        st.session_state.tabcbis.clear()
        st.session_state.D = D
        st.session_state.stepbis = RIS(st.session_state.D,slidep,slideq,slides)
        st.session_state.pos = nx.spring_layout(st.session_state.D ,seed=42)
        his,hit,arrettab,courbebis = st.session_state.stepbis

        for step in range( len(st.session_state.stepbis[0])):
                            nodes,nodels,edges,cbs = st.session_state.stepbis
                            node = nodes[step]
                            nodel = nodels[step]
                            edge = edges[step]
                            fig,ax = plt.subplots(figsize = (8, 6))
        
                            color_n = [ "red" if n in node  else "green" if n in nodel else "lightblue" for n in st.session_state.D.nodes() ]
                            color_e = [ "red" if n in edge  else "lightgray" for n in st.session_state.D.edges() ]
        
                            nx.draw(st.session_state.D,st.session_state.pos,node_color=color_n,edge_color=color_e ,with_labels=True,ax = ax,node_size=300)
                            legend_elements = [
                            mp.Patch(color = "red",label = "Diffuseur"),
                            mp.Patch(color = "green",label = "Lasser"),
                            mp.Patch(color = "lightblue",label = "Ignorants"),
                            ]
                            ax.legend(handles=legend_elements,loc = "upper right")
                            ax.set_title(f"Etape {step}")
                            st.session_state.tabbis.append(fig)
        
                            figs = tracer_evolution_temporelle_cinembis(cbs,step)
                            st.session_state.tabcbis .append(figs)     
                    



        with st.spinner():
            st.session_state.animate_propagationbis = animate_propagationbis(st.session_state.D,his,hit,arrettab,st.session_state.pos,filenamebis)
            st.session_state.courbebis = tracer_evolution_temporellebis(courbebis)


    with colon1:       
        if st.session_state.stepbis != [[]]  and st.session_state.pos is not None:
            if cinem == "Automatique":
                    st.image(filenamebis,caption="Automatique")  
    with colon2:
            if st.session_state.courbebis is not None :
                if cinem == "Automatique":
                        st.pyplot(st.session_state.courbebis)  
                            
    with colon1:
        if st.session_state.stepbis != [[]]  and st.session_state.pos is not None:
            if cinem == "Manuel":
                step = st.bottom.slider(
                "Étape",0,len(st.session_state.stepbis[0]) - 1)
                st.pyplot(st.session_state.tabbis[step])
                plt.close(st.session_state.tabbis[step])

                with colon2:
                    if st.session_state.courbebis is not None :
                        st.pyplot(st.session_state.tabcbis[step])  
                        plt.close(st.session_state.tabcbis[step])      
                    