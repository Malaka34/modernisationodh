#!/usr/bin/env python
# coding: utf-8

# ![](Bandeau_seul_ODH.png)

# # Nettoyage du WorkBook Excel

# ```{note}
# - **Suggestion :**
# 
# Il est fortement conseillé d'utilisé des **classeurs Excel dont les extentions sont `xlsx`**. Convertiser donc si besoin vos classeurs `xls` en `xlsx`.
# ```

# La première étape consiste à nettoyer le classeur Excel afin qu’il soit prêt à être passé à la fonction de déconstruction. Dans cette il faut que les règles ci-dessus soient respectées :

# 
# 1 -	Pas de parenthèses dans les noms de colonnes, ni dans les noms d’onglets <br>
# 
# 
# 2 -	Pas de caractères spéciaux (<,>,=,-, .) dans les noms de colonnes, ni dans les noms d’onglets<br>
# 
# 
# 3 -	Ne pas laisser d’espace à la fin du nom de colonne ou d’onglet<br>
# 
# 
# 4 -	Ne pas commencer le nom d’une colonne par des chiffres<br>
# 
# 
# 5 -	Ne pas mettre des chiffres comme nom de colonnes ni dans les noms d’onglets<br>
# 
# 
# 6 -	Ne mettre qu’une table par onglet, car chaque onglet va être transformé en fichier CSV<br>
# 
# 
# 7 -	Les données doivent être de la même échelle (commune / Epci / Iris) dans un classeur<br>
# 
# 
# 8 -	Lorsqu’il y a des informations non renseignés, laisser leurs cellules vides. Ne surtout pas mettre "ns" au risque de compromettre la cohérence du typage de cette colonne<br>
# 
# 
# 9 - Ne garder dans les fichiers Excel que les lignes à charger dans la base de données<br>
# 
# 10 - La règle 8 s’applique aussi pour les données secrétisées. Laisser leurs cellules vides.<br>
# 
# Par ailleurs il existe une fonction dans le processus de déconstruction qui vérifie les premières règles. Les noms de colonnes sont transformés en modalités et ceux des onglets en variables (voir la section **FAQ**).
# 

# ![](logo_bandeau.jpg)

# In[ ]:




