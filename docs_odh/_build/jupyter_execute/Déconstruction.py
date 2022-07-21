#!/usr/bin/env python
# coding: utf-8

# ![](Bandeau_seul_ODH.png)

# # II - Déconstruction

# ## A.	Premières question, création automatique de dossier temporaire

# Le traitement à proprement parler commence qui commence par la cellule suivante :

# In[ ]:


new_millesime = fonctions.traitementDonneesComplet(chemin,annee,nom_Fichier_Variable,source,nom_Fichier_Modalite,path_vars,suffix_nom_schema)


# Cette première étape va permettre de restructurer et de télécharge tous les fichiers csv créés dans la partie précédente, sous la structure pré-définie et importable vers la base pgAdmin. L'exécution de la fonction fonction 'traitementDonneesComplet' va dérouler deux de questions.
# 
# - La première concerne l'exsistance d'un schéma non vide dans pgAdmin pour acceuillir ces nouvelles données. Attention : répondre par oui écrasera l'ancienne version des fichiers variables et modalités s'ils existent déjà.
# - Ensuite il faut choisir l'echelle (commune, epci ect...) des données en cours de traitement.
# 
# Un dossier temporaire va être créer localement pour gérer la suite du traitement. C'est le dossier 'DosierFichierstraités'
# 

# ## B. Vérification de modalités et variables

# Pour créer ou mettre à jour la liste des variables de la source de données qui est en train d'être traité, à chaque nouvelle variable rencontrée la fonction va demander de renseigner le libellé long de cette nouvelle variable.
# Elle procédera de la même manère pour les modalités sauf que dans ce cas, elle demandera en plus la catégorie de regroument de cette nouvelle modalité.
# 
# suggestion : préparér à l'avance une table comprenant toutes les information bien rangés des variables et une autre table pour les modalités (créer une métadonnées).

# A la fin de l'excusion de cette fonction, les fichiers csv à la structuration adéquate sont créés et se trouvent dans le dossier temporaire 'DossierFichiersTraités'.
# On va donc passer à la suite et verser les données dans la base relationelle pgAdmin.

# ```{note}
# 
# Si l'exécution de cette cellule produit une erreur, procédez comme suit :
# - allez manuellement supprimer le dossier temporaire 'DossierFichiersTraités'
# - réexécuter la cellule en répondant 'NON' à la premère question (Question concernant l'existance de schéma non vide)
# 
# Attention !!! ==> Avant de passer au versement, pensez donc à créer une nouvelle cellule de code (dans la barre en haut, appuyer sur le bouton + . il permet d'insérer une nouvelle cellule) contenant : new_millesime = 1.
# 
# Vous la supprimerez à la fin de l'exécution de tout le programme.
# ```

# ![](logo_bandeau.jpg)
