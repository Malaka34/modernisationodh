#!/usr/bin/env python
# coding: utf-8

# ![](Bandeau_seul_ODH.png)

# # III - Versement de données et suppression des dossiers temporaire

# In[ ]:


fonctions.versementDonnes2(Nom_base,Nom_utilisateur,mot_de_passe,nom_host,port,source,nom_schema_donnees,
                    nom_Fichier_Variable,nom_Fichier_Modalite,new_millesime,path_vars,suffix_nom_schema)


# In[ ]:





# Cette cellule ci-dessus permet de lancer le versement des données toutes récemment restructurées.
# selon la à la première question de la partie II, la fonction **`versementDonnes2`** va créer des nouvelles tables et insérer de nouvelles données, ou elle mettra à jour les tables existantes. 
# 
# - S'il s'agit d'une insertion de données dans un nouveau schéma vide, les tables des variables, modalités et celle de la jointure Posseder vont être créés. Ainsi, la fonction demandera les clés primaires (sauf celles de la table Posseder qui se créé automatiquement).
# 
# Voici les clés primaires par table :
# 
# 
# | **Nom table** |   **Clé**   |
# |---------------|:-----------:|
# | Variable      |  CodeVarID  |
# | Modalites     | CodeModalID |  
# 
# 
# - Dans le cas d'une mise à jour de données dans un schéma existant (par exemple l'insertion des données d'une nouvelle année, ou encore l'insertion de données avec une nouvelle échelle ), 
# la fonction va chercher les tables concernées et insérer les données, voire créer de nouvelles tables si besoin.

# Une fois les versements terminés, la cellule suivante vous permettra de supprimer tous les dossiers temporaires créés au début de ce programme.

# ![](logo_bandeau.jpg)
