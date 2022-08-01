#!/usr/bin/env python
# coding: utf-8

# ![](Bandeau_seul_ODH.png)

# # II - Déconstruction

# ## A.	Premières question, création automatique de dossier temporaire

# Le traitement  proprement dit commence par la cellule suivante :

# In[ ]:


new_millesime = fonctions.traitementDonneesComplet(chemin,annee,nom_Fichier_Variable,source,nom_Fichier_Modalite,path_vars,suffix_nom_schema)


# Cette première étape va permettre de restructurer et de télécharge tous les fichiers csv créés dans la partie précédente, sous la structure prédéfinie et importable vers la base de données **pgAdmin 4**. L'exécution de la fonction fonction **`"traitementDonneesComplet"`** va dérouler deux questions:
# 
# - La première concerne l'exsistence d'un schéma non vide dans pgAdmin pour accueillir ces nouvelles données. `Attention : répondre par oui écrasera l'ancienne version des fichiers variables et modalités s'ils existent déjà`.
# - Ensuite il faut choisir l'echelle (commune, epci etc.) des données en cours de traitement.
# 
# Un dossier temporaire va être créer localement pour gérer la suite du traitement. C'est le dossier **"DosierFichierstraités"**.
# 

# ## B. Vérification de modalités et variables

# Pour créer ou mettre à jour la liste des variables de la source de données  en cours de traitement, pour chaque nouvelle variable rencontrée, la fonction demandera de saisir le libellé long de cette nouvelle variable. Elle procédera de la même manière pour les modalités sauf que dans ce cas, elle demandera en plus la catégorie de regroupement de cette nouvelle modalité.
# 
# **suggestion :** préparer à l'avance une table comprenant toutes les informations bien rangéss des variables et une autre table pour les modalités (créer une métadonnée).

# À la fin de l'exécusion de cette fonction, les fichiers **csv** à la structuration adéquate sont créés et se trouvent dans le dossier temporaire **"DosierFichierstraités"**.
# On va donc passer à la suite et verser les données dans la base relationnelle **pgAdmin**.

# ```{note}
# 
# Si l'exécution de cette cellule produit une erreur, procédez comme suit :
# - allez manuellement supprimer le dossier temporaire **"DosierFichierstraités"**
# - réexécuter la cellule en répondant "NON" à la première question (Question concernant l'existence de schéma non vide)
# 
# `Attention !!!` : Avant de passer au versement, pensez donc à créer une nouvelle cellule de code (dans la barre en haut, appuyer sur le bouton **+** . il permet d'insérer une nouvelle cellule) contenant : new_millesime = 1.
# 
# Vous la supprimerez à la fin de l'exécution de tout le programme.
# ```

# ![](logo_bandeau.jpg)
