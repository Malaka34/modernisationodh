#!/usr/bin/env python
# coding: utf-8

# ![](Bandeau_seul_ODH.png)

# 
# # I -  Paramètres à renseigner sur le script
# 

# Avant de démarrer l'exécution de ces cellules, vous devez avoir déjà créé dans **pgAdmin** le schéma dans lequel les données du classeur Excel seront chargées et traitées.
# Il est en outre nécessaire de fermer tous les fichiers Excel qui seront utilisés pendant ce traitement.

# Le script commence par une cellule qui importe les bibliothèques nécessaires au bon déroulement du traitement et du transfert des données.
# L'avant-dernière ligne similaire à la ligne de code suivante représente l'emplacement du fichier **`fonctions.py`**, il doit donc être ajusté en fonction de son emplacement sur votre ordinateur.

# In[ ]:


sys.path.insert(0, r"C:/Users/malaka/Documents/prog/BDD") # à adpter à partir de malaka


# Dans l'exemple ci-dessus , mon fichier fonction se trouve dans dans le dossier **"BDD"** dont le chemin est `"C:/Users/malaka/Documents/prog/BDD"`.
# La cellule  après celle des imports de librairies, permet ed créer un dossier temporaire nommé **"DossierFichiersbrutesCsv"** qui sera supprimer à la fin du programme.
# 
# Il faudrait ensuite changer dans la cellule suivante, **"SNE_Demande_2020_com.xlsx"** par le nom du fichier à traiter (le classeur Excel). L'exécution de la prochaine cellule permettra d'enregistrer les feuilles Excel du classeur en fichier **csv**. Ce format est important pour la suite du programme. les noms des feuilles Excel vont s'afficher au fur et à mesure qu'ils sont enregistrés en format csv.
# 
# On va entrer les paramètres du programme universel :

# In[ ]:


annee = 2020                                         # à adapter
path_vars ='../vars/'                                # à adapter

######## PARAMETRES :: CREATION DE TABLES #########
suffix_nom_schema = 'SNE'                            # à adapter

nom_Fichier_Variable = 'variables_{}.csv'.format(suffix_nom_schema)
nom_Fichier_Modalite = 'Modalites_{}.csv'.format(suffix_nom_schema)

######## PARAMETRES :: CONNEXION à LA BASE DE DONNES #########
Nom_base = "bdsociohab"                             # à adapter
Nom_utilisateur = "Votre_d'utilisateur_pgAdmin"     # à adapter
mot_de_passe = "Votre_mot_de_passe"                 # à adapter
nom_host = "s934" 
port = "5441"

######## PARAMETRES :: INSERTION DES DONNEES #########
source ='SNE'                                       # à adapter
nom_schema_donnees = str('socio_hab_' + suffix_nom_schema).lower()


# - `annee` = année de collecte
# - `suffix_nom_schema` = le nom qui est donné au shéma dans lequel va être versé ces données, sans la partie 'socio_hab_'
# - `source` = nom de la source (ex : 'FSL')
# - `path_vars` = le chemin du dossier "vars"
# - `Nom_base` = un string qui represente le nom de la base de données à la quelle on souhaite se connecter
# - `Nom_utilisateur` = un string qui represente le nom de pgAdmin de l'utilisateur qui souhaite de connecter
# - `mot_de_passe` = un string qui represente le mot de passe de l'utilisateur
# - `nom_host` = un string qui represente le nom de l'hebergeur de la base de données
# - `port` = un string numerique qui represente le port de connexion à la base de données

# ![](logo_bandeau.jpg)
