#!/usr/bin/env python
# coding: utf-8

# ![](Bandeau_seul_ODH.png)

# # III - Versement de données et suppression des dossiers temporaire

# In[ ]:


fonctions.versementDonnes2(Nom_base,Nom_utilisateur,mot_de_passe,nom_host,port,source,nom_schema_donnees,
                    nom_Fichier_Variable,nom_Fichier_Modalite,new_millesime,path_vars,suffix_nom_schema)


# Cette cellule ci-dessus permet de lancer le versement des données toutes récement restructurées.
# selon la à la première question de la partie II, cette fonction va créer des nouvelles tables et insérer de nouvelles données, ou elle mettra à jour les tables existantes. 
# 
# - Lorsqu'il sagit d'une insertion de données dans un nouveau schéma vide, les tables des variables, modalitées et celle de la jointure Posseder vont être créées. Ainsi, la fonction demandera les clés primaires (sauf celles de la table Posseder qui se créé automatiquement).
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
# - Lorsqu'il sagit d'une mise à jour de données dans un schéma existant (par exemple l'insertion des données d'une nouvelle année, ou encore l'insertion de données avec une nouvelle échelle ), 
# la fonction va chercher les tables concernées et insérer les données, voir créer de nouvelles tables si besoin.

# Une fois les versement terminés, la cellule suivante va permettre de supprimer tous les dossiers temporaires créés au début de ce programme.

# ![](logo_bandeau.jpg)
