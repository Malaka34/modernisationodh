#!/usr/bin/env python
# coding: utf-8

# # Nettoyage du WorkBook Excel

# La première étape consiste à nettoyer le WorkBook Excel afin qu’il soit prêt à être passé à la fonction de déconstruction. Dans cette il faut que les règles ci-dessus soient respectés :
# 1.	Pas de parenthèses dans les noms de colonnes, ni dans les noms d’onglets
# 2.	Pas de caractères spéciaux (<,>,=,-, .) dans les noms de colonnes, ni dans les noms d’onglets
# 3.	Ne pas laisser d’espace à la fin du nom de colonne ou d’onglet
# 4.	Ne pas commencer le nom d’une colonne par des chiffres
# 5.	Ne pas mettre des chiffres comme nom de colonnes ni dans les noms d’onglets
# 6.	Ne mettre qu’une table (information / données) par onglet, car chaque onglet va être transformé en fichier CSV
# 7.	Les données doivent être de la même échelle (commune / Epci / Iris) dans un WorkBook
# 8.	Lorsqu’il y a des non renseignés, laisser leurs cellules vides. Ne surtout pas mettre ‘ns’ au risque de compromettre la cohérence du typage de cette colonne
# 9.	La règle 8 s’applique aussi pour les données secrétisées. Laisser leurs cellules vides.
# Par ailleurs il existe une fonction dans le processus de déconstruction qui vérifie les premières règles. Les noms de colonnes sont transformés en modalités et ceux des onglets en variables.
# 10. Ne garder dans les fichiers Excel que les lignes à charger dans la base de données
# 

# In[ ]:




