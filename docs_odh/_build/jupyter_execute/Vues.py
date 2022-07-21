#!/usr/bin/env python
# coding: utf-8

# ![](Bandeau_seul_ODH.png)

# # IV - Création et mise à jour des Vues

# Comme dans la partie traitement, on commence ce programme avec l'importations des librairies necésseraire.
# L’avant dernière ligne qui ressemble à la ligne de code suivante renseigne la locatisation du fichier fonctions.py et donc est à adapter selon sa localisation dans votre ordinateur.

# In[ ]:


sys.path.insert(0, r"C:/Users/malaka/Documents/prog/BDD") # à adpter à partir de malaka


# Ensuite toujours comme le script de traitement et versement de données, on va renseigner les paramètres

# In[ ]:


######## PARAMETRES :: CONNEXION à LA BASE DE DONNES #########
Nom_base = "bdsociohab"                             # à adapter
Nom_utilisateur = "Votre_d'utilisateur_pgAdmin"     # à adapter
mot_de_passe = "Votre_mot_de_passe"                 # à adapter
nom_host = "s934" 
port = "5441"

suffix_nom_schema = 'sne'                           # à adapter
nom_schema_donnees = str('socio_hab_' + suffix_nom_schema)


# La dernière cellule contient la fonction creationVuesSchema. Elle permet de créer ou de mettre à jour les vues, sous la structure originale des tables excel versés dans pgAdmin.
# Elle affiche la progression de l'exécution des tâches

# ![](logo_bandeau.jpg)
