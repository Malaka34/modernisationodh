#!/usr/bin/env python
# coding: utf-8



def connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port):
    
    """
    Données : Nom_base est un string qui represente le nom de la base de données à la quelle on souhaite se connecter
              Nom_utilisateur est un string qui represente le nom de pgAdmin de l'utilisateur qui souhaite de connecter
              mot_de_passe est un string qui represente le mot de passe de l'utilisateur
              nom_host est un string qui represente le nom de l'hebergeur de la base de données
              port est un string numerique qui represente le port de connexion à la base de données
              
    Résultat : Affiche une phrase (string) indiquant si la connexion est réussie ou non et retourne con (à re-définir)
    """
    import psycopg2
    
    try:
        # connexion
        con = psycopg2.connect(database= Nom_base, user= Nom_utilisateur, password= mot_de_passe, host= nom_host, port= port)
        #print("Connexion réussie \n")
        return con
    

    except (Exception, psycopg2.Error) as error :
        print ("Erreur lors de la connexion à PostgreSQL", error)


##########################################################################################################################################
def creationTableAvecFichierComplet(fichierCSV, nom, nom_schema, con, nbclE, CleFK, ClePK, tableRef, path_vars):
    """
    données : fichierCsv est un fichier CSV dont on veut reproduire la strucure sur une base de données
    
              nom est un string qui représente le nom du fichier
              
              nom_schema est un string représentant le nom du schema de la base de données où va être créé la table
              
              con = une instance de la fonction connexion
              
              nbclE est le nombre (en int) de clées étrangères
              
              CleFK est une liste des clées étrangères
              
              ClePK est un string qui représente la clée primaire
              
              tableRef est une liste des tables de références des clées étrangères
              
              (Dossier est un string qui indique le nom du dossier dans lequel se trouve le fichier)
              
    résultats : créé une table sur une base de données. 
                Affiche une phrase indiquant si la table à été créée ou pas et retourne le nom de la table créée
                
    remarques : il faut déja se connecter avec la fonction 'connexion'
    """
     # importation de packages
    import pandas as pd
    import psycopg2
    import csv
    import numpy as np
    
    newTab = fichierCSV
    
    con = con

    # dictionnaire des metas infos à remplir
    infoMeta = {
        'nom':[],
        'colonnes': [],
        'types': [],
        'primary_key' : [],
        'foreign_Keys' : [],
        'tableRefFK' : []
    }

    # nom de la table à créer
    nom=nom.replace(path_vars,'')
    nom=nom.replace('.csv','') 
    infoMeta['nom'].append(nom.lower())
    
    #noms colonnes de la nouvelle table
    newTabCol =  newTab.columns

    for col in range(len(newTabCol)):
        nomCol = newTabCol[col]
        infoMeta['colonnes'].append(nomCol)
        
        #types des colonnes
        Col1 = newTab.iloc[0][col]

        
        #if(nomCol == 'Categ_regroupement'): # attention ===> même nom que celui dans la table modalités
            #infoMeta['types'].append(type('a'))

        if(type(Col1)==type(np.float64(1.0))):
            infoMeta['types'].append(type(1.0))

        elif(type(Col1)==type(np.float64(1))):
            infoMeta['types'].append(type(1))

        elif(str(Col1).isnumeric()):
            infoMeta['types'].append(type(1))
        

        else:
            infoMeta['types'].append(type(Col1))
            
    #clée primaire

    # saisie de la clée primaire de la table

    InClePrim = ClePK
    #print(InClePrim)

    # adding the primary key into infoMeta

    infoMeta['primary_key'].append(InClePrim)

    if(InClePrim == ''):
           print('pas de clé primaire')
           # max value de la clée primaire
           max_value = 0

    else:

        #indice de position de la clée primaire dans liste des colonnes
        j=0
        trouve = False
        indicePK= 'rien'
        while(j<=len(newTabCol) and trouve== False):
            #print(infoMeta['primary_key'])
            if (infoMeta['primary_key'][0] ==newTabCol[j]):
                #print('here')
                indicePK= j
                #print(indicePK)
                trouve = True

            j+=1
        # max value de la clée primaire
        max_value = str(np.max(newTab[ClePK]))

        #changement en text du type de la clée primaire
        infoMeta['types'][indicePK] = type(1)
        #print(infoMeta['types'])

    #print(max_value) 
   #clée étrangère

    nbcleEtran = int(nbclE)
    if (nbcleEtran != 0):

        # saisie des clées étrangères de la table

        InCleEtrang = CleFK

        for i in range(len(InCleEtrang)):
            InCleEtrang[i] = InCleEtrang[i].strip()


        # adding the foreign keys into infoMeta
        for i in range(len(InCleEtrang)):
            infoMeta['foreign_Keys'].append(InCleEtrang[i]) 



        # saisie des tables de références des clées étrangères
        InRefFK = tableRef


        for i in range(len(InRefFK)):
            InRefFK[i] = InRefFK[i].strip()

        # adding tab refs 
        for i in range(len(InRefFK)):
            infoMeta['tableRefFK'].append(InRefFK[i])

         #indice de position des clées étrngères dans liste des colonnes

        for cleEtrangere in range(nbcleEtran):

            j=0

            trouve = False
            indicePK= 'rien'

            while(j<=len(newTabCol) and trouve == False):
                #print(infoMeta['foreign_Keys'][cleEtrangere])
                #print('newTabCol[j] :', newTabCol[j])
                if (infoMeta['foreign_Keys'][cleEtrangere] == newTabCol[j]):
                    #print('here')
                    indicePK= j 
                    trouve = True

                j+=1

            #changement en int tu type de la clée etrangère
#             infoMeta['types'][cleEtrangere] = type('a')
            #print(infoMeta['types'])
            #print(cleEtrangere)


    else :
        print('Pas de clé étrangère')

        
       # switching to sql types
    for j in range(len(infoMeta['types'])):
        
        if(infoMeta['types'][j]==type(1)):
            if((infoMeta['colonnes'][j]==infoMeta['primary_key'][0]) and len(max_value)>10):
                #print(infoMeta['colonnes'][j])
                infoMeta['types'][j]= 'text' # je laisse cette condition au cas où on voudrait garder des colonnes en integer==> remplacer 'text' par 'int'
            else:
                infoMeta['types'][j]= 'text'
        elif(infoMeta['types'][j]==type(1.0)):
            infoMeta['types'][j]= 'float'
        elif(infoMeta['types'][j]== type('a')):
            infoMeta['types'][j]= 'text'



    #affichage
    print(infoMeta)

            
    # sql query 
    #(début de la ligne de commande)
    sqlQuery = str("CREATE TABLE "+ nom_schema+ "."+infoMeta['nom'][0]+"(")
    
     
    
    lignesCommande=[]
    for l in range(len(infoMeta['colonnes'])):
        ligne = str(infoMeta['colonnes'][l]+" ")+str(infoMeta['types'][l])
        #primary key query
        if(InClePrim != ''):
            if(infoMeta['primary_key'][0] == infoMeta['colonnes'][l]):
                ligne = ligne+" "+ 'PRIMARY KEY'
                
        lignesCommande.append(ligne)
    
    sqlQuery = sqlQuery +str(lignesCommande)
    
    # creation the query for a possible foreign keys
    table_sqlQF = []
    if (nbcleEtran != 0):

        for f in range(len(infoMeta['foreign_Keys'])):
            sqlQF = str('CONSTRAINT fk_')+str(infoMeta['tableRefFK'][f]+ ' FOREIGN KEY('+ infoMeta['foreign_Keys'][f]+ ') REFERENCES '+ infoMeta['tableRefFK'][f]
                    +' ('+infoMeta['foreign_Keys'][f]+')')
            table_sqlQF.append(sqlQF)

        sqlQuery =sqlQuery + ','+ str(table_sqlQF)+')'
        
    else:
        sqlQuery= sqlQuery + ')'
    sqlQuery = sqlQuery.replace('[','')
    sqlQuery = sqlQuery.replace(']','')
    sqlQuery = sqlQuery.replace("'","")
    
    
    ## Création de la table
    
    try:
        cur = con.cursor()
        dropingLine = 'DROP TABLE IF EXISTS "' + infoMeta['nom'][0]+ '";'
        cur.execute(dropingLine)

         # Creating Table infoMeta['nom'][0]
        cur.execute(sqlQuery)
        con.commit()
        print('______________________________________________________________________________')
        print("La table "+infoMeta['nom'][0]+ " à été créée avec succès dans PostgreSQL \n")
    except (Exception, psycopg2.Error) as error :
        print ("Erreur lors de la création de la table 'Variables' dans PostgreSQL: ", error)
        print(sqlQuery)
    return infoMeta['nom']

############################################################################################################################################
############################################################################################################################################

def insertionDonnees(fichierCSVpath, con, table, sep):
    """
    Données : fichierCsv est un fichier CSV dont on veut reproduire la structure sur une base de données
              con = une instance de la fonction connexion
              table = nom (en string) de la table où vont être insérées les données
              sep = separateur de text, could be : ';' or '\t' for exemple
            
    résultat : insere les données de fichierCSV dans la table "table", dans une base de données. 
                Affiche une phrase indiquant si les données ont été insérées ou pas
    remarques : il faut déja se connecter avec la fonction 'connexion'. ne marche pas tres bien pour les schemas non publics
    """
    
    import psycopg2
    import traceback
    
    try:
        with open(fichierCSVpath, 'r', encoding="utf8") as Vars:
            next(Vars)# Skip the header row.
            
            # Insertion des données dans la table 
            cur = con.cursor()
            cur.copy_from(Vars, table, sep=sep)
            
        print('la requête a été executée')
        
    except (Exception, psycopg2.Error) as error :
        print(traceback.format_exc())
        print ("Erreur lors de l'insertion des données importées dans la table {} :".format(str(table)), error)
        con.rollback()
        
    else:
        con.commit()
        print("Les données importées ont été inserées avec succès dans la table {} \n".format(str(table)))

##################################################################################################################################
def insertionDonnees2(fichierCSVpath, con, table, sep):
    """
    Données : fichierCsv est un fichier CSV dont on veut reproduire la structure sur une base de données
              con = une instance de la fonction connexion
              table = nom (en string) de la table où vont être insérées les données
              sep = separateur de text, could be : ';' or '\t' for exemple
            
    résultat : insere les données de fichierCSV dans la table "table", dans une base de données. 
                Affiche une phrase indiquant si les données ont été insérées ou pas
    remarques : il faut déja se connecter avec la fonction 'connexion'. cette fonction marche bien pour les schemas non publics
    # peut etre demander le nombre de colonnes pour plus generaliser cette fonction
    """
    
    import psycopg2
    import csv
    import traceback
    
    try:
        
        cur = con.cursor()
        #table_try = "'"+nom_schema_donnees.lower()+"'."+result[0][0]
        with open(fichierCSVpath, 'r', encoding="utf8") as file:
            reader = csv.reader(file, delimiter=sep)
            next(reader)# Skip the header row.
            
            # Insertion des données dans la table 
            for row in reader:
                values = [x if x!='NULL' else None for x in row]
                cur.execute( "INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s)".format(table),values)
                
        print('la requête a été executée')
        
        
    except (Exception, NameError, psycopg2.Error) as error :
        print(traceback.format_exc())
        print ("Erreur lors de l'insertion des données importées dans la table {} :".format(str(table)), error)
        con.rollback()        
        
    else:
        con.commit()
        print("Les données importées ont été inserées avec succès dans la table {} \n".format(str(table)))




        
##################################################################################################################################
##################################################################################################################################
def replacingSpaceModa(fichier_A_traiter):
     # création de la liste ds modalités de la variable
    listeCols = fichier_A_traiter.columns
    listeCols.tolist()
    
    
    #transformer les charactères en unicode
    import unidecode
    ModasinAcc = []
    for modalite in range(len(listeCols)):
        new_string = listeCols[modalite].replace(listeCols[modalite],unidecode.unidecode(listeCols[modalite])).title()
        ModasinAcc.append(new_string)
      # removing commas and points
    for modalite in range(len(ModasinAcc)):
        if((',') in ModasinAcc[modalite]):
            ModasinAcc[modalite]= ModasinAcc[modalite].replace(',','')

        if(('.') in ModasinAcc[modalite]):
            ModasinAcc[modalite]= ModasinAcc[modalite].replace('.','')
            
        if(('(') in ModasinAcc[modalite]):
            ModasinAcc[modalite]= ModasinAcc[modalite].replace('(','')
            
        if((')') in ModasinAcc[modalite]):
            ModasinAcc[modalite]= ModasinAcc[modalite].replace(')','')

        if(('/') in ModasinAcc[modalite]):
            ModasinAcc[modalite]= ModasinAcc[modalite].replace('/','_')

        if((' ') in ModasinAcc[modalite]):
            firstStr = ModasinAcc[modalite][0]
            lastStr = ModasinAcc[modalite][-1]
            if( firstStr==' '):
                firstStr = firstStr.replace(' ','',1)
            if(lastStr==' '):
                lastStr = ''.join(lastStr.rsplit(' ', 1))

            middle = ModasinAcc[modalite][1:-1].replace(' ','_')

            ModasinAcc[modalite] = firstStr + middle + lastStr
        
        if(("'") in ModasinAcc[modalite]):
            ModasinAcc[modalite]= ModasinAcc[modalite].replace("'",'_')
            
    fichier_A_traiter.columns = ModasinAcc


############################################################################################################################################
def checkingModalites(fichier_A_traiter, nom_Fichier_Modalite, path_vars):
    
    """
    Donnée : fichier_A_traiter est le fichier csv original à traiter
    
            nom_Fichier_Modalite est le nom exacte du fichier CSV des modalités de cette source
             
             
    Résultat : retourne la liste des modalités avec toutes les eventuelles nouvelles modalités 
    """
    import pandas as pd
    import unidecode
    
    # téléchargement du fichier Modalites_.csv', qui se trouve dans le dossier 'vars'
    Modalites= pd.read_csv(path_vars+nom_Fichier_Modalite, delimiter=';', encoding='utf-8')
    
    #Liste des modalités et de leurs codes
    listeCodeModa = pd.DataFrame(columns = ['code', 'noms', 'Lib_long','categ_regroupement'])
    
    #remplacement des caractères spéciaux
    repmplacerCaratereSpeciaux(fichier_A_traiter)
    
    #transformer les charactères en unicode et les premiers lettres en capitales (avec la fonction .title())
    replacingSpaceModa(fichier_A_traiter)

    # checking 
    
    for modalite in range(len(fichier_A_traiter.columns)):
        print('Modalité recherché :', fichier_A_traiter.columns[modalite], '\n')
        # test
        if(fichier_A_traiter.columns[modalite].lower() in Modalites['CodeModalEXT'].tolist() ):
            print('trouvé \n')
            ligne = Modalites.loc[(Modalites['CodeModalEXT'] == fichier_A_traiter.columns[modalite].lower())]
            #print(ligne)
            ligne = ligne.reset_index(drop=True)
            listeCodeModa= listeCodeModa.append({
                    'code': ligne.CodeModalID[0],
                    'noms': fichier_A_traiter.columns[modalite],
                    'Lib_long': ligne.Libelle_long[0],
                    'categ_regroupement': ligne.Categ_regroupement[0]
                }, ignore_index=True)


        else:
            print('nouveau \n')
            print('Veuillez saisir le libellé long de cette modalité')

            lib = input()

            print('Veuillez saisir la catégorie de regroupement de cette modalité')
            categ_regroupement = input()
            if(categ_regroupement == ''):
                categ_regroupement = fichier_A_traiter.columns[modalite]

            listeCodeModa= listeCodeModa.append({
                    'code': len(Modalites)+1,
                    'noms': fichier_A_traiter.columns[modalite],
                'Lib_long': lib,
                'categ_regroupement': categ_regroupement
                },ignore_index=True)

            Modalites = Modalites.append({
                'CodeModalID' : len(Modalites)+1,
                'CodeModalEXT' : fichier_A_traiter.columns[modalite].lower(),
                'LibelleModal' : fichier_A_traiter.columns[modalite],
                'Libelle_long' : lib,
                'Categ_regroupement': categ_regroupement

            }, ignore_index=True)
            
    Modalites.to_csv(path_vars+nom_Fichier_Modalite,index=False,sep=';', encoding='utf-8') 
    return listeCodeModa

##################################################################################################################################
##################################################################################################################################
def checkingVariable(csv_files,nom_Fichier_Variable,source,path_vars ):
    import unidecode
    '''
    Données : csv_files = liste des fichiers csv dont les variables sont à checker,
    
              origine = source,
              
              nom_Fichier_Variable est le nom exacte du fichier CSV des variables de cette source
              
              source = nom de la source (ex : 'FSL')

    Résultat : retourne la liste des modalités avec toutes les eventuelles nouvelles modalités, pour les fichiers FSL
    '''
    import pandas as pd
    
    Variables = pd.read_csv(path_vars+nom_Fichier_Variable, delimiter=';', encoding='utf-8')
    for Variable in range(len(csv_files)):
        trouve = False
        i = 0
        new_var = False
        if(len(Variables)==0):
            new_var = True
        else:
            while(i<len(Variables) and trouve == False):
                #print('variable existante : {}'.format(Variables.CodeVarEXT[i]))
                #print('variable recherchée : {}'.format(csv_files[Variable].lower()))
                if(unidecode.unidecode(csv_files[Variable]).lower() == unidecode.unidecode(Variables.CodeVarEXT[i]).lower()):
                    trouve = True
                    
                if(i == len(Variables)-1 and trouve == False): 
                    new_var = True
                    #print('second true')
                i+=1
        if(new_var == True):
            print('nouvelle variable : {}'.format(csv_files[Variable]))
            print('Veuillez saisir le libellé long de cette variable')
            lib = input()
            if(lib == ''):
                lib = csv_files[Variable]
            Variables = Variables.append({
                'CodeVarID' : len(Variables)+1,
                'CodeVarEXT' : unidecode.unidecode(csv_files[Variable]).lower(),
                'LibAxeAnalyse' : lib,
                'Origine' : source.lower()
                


            }, ignore_index=True)
                
            print('la variable {} à été insérée \n '.format(csv_files[Variable]))   
    Variables.to_csv(path_vars+nom_Fichier_Variable,index=False,sep=';', encoding='utf-8')

    
    
##################################################################################################################################
##################################################################################################################################

def traitementDonnees(fichier_A_traiter,nomFichier,codevarid,annee,nom_Fichier_Modalite,path_vars,echelle):
    """
    Donnée : fichier_A_traité est le fichier csv original à traiter
    
             nomFichier est un string représentant le nom du fichier "fichier_A_traité"
             
             codevarid est un int qui represente l'identifiant de la variable traité dans le fichier "fichier_A_traité"
             
             annee est l'année de production des requêtes dans le fichier "fichier_A_traité"
             
             path_vars est le chemin du dossier "vars"
             
    Résultat : un nouveau fichier csv prête à exporter vers la base de données sur pgAdmin
    Remarque :  
    
    """
    
    #Importations des packages nécessaires pour traiter les fichiers
    import glob
    import pandas as pd
    import os
    
    
    
    

    #Création de la table à exporter plus tard
    newTabTraite = pd.DataFrame(columns = ['CodeVarID', 'Annee', 'codeEntite', 
                                 'CodeModalID', 'Echelle', 
                                 'IndicePosition', 'Valeur'])
    
    tabATraite = fichier_A_traiter

    # pour avoir la liste des modalitées
    listeCodeModa = checkingModalites(tabATraite,nom_Fichier_Modalite,path_vars)
    
    #renommer la premier colonne en "codeEntite"
    tabATraite.rename(columns={ tabATraite.columns[0]: 'codeEntite'}, inplace = True)
    
    
    
    for ligne in range(len(tabATraite)):
        valeur = []
        codeModa = []
        code_ent = tabATraite['codeEntite'][ligne]
        

        for col in range(1,len(listeCodeModa),1):
            valeur.append(tabATraite.iloc[ligne][col])
            codeModa.append(listeCodeModa['code'][col])

        #insertion de la ligne
        for i in range(len(valeur)):
            newTabTraite=newTabTraite.append({
                'CodeVarID':codevarid,
                'Annee':annee,
                'Echelle': echelle,
                'codeEntite':code_ent,
                'CodeModalID':codeModa[i],
                'Valeur': valeur[i],
                'IndicePosition': str(codevarid)+str(code_ent)+str(codeModa[i])+str(annee)
            },ignore_index=True)


        #Remplacement des cellules vides par des zeros
        newTabTraite.fillna('NULL', inplace=True)
        
         
    #the new file's name
    newName = nomFichier +'.csv'
    
    # exportation du nouveau fichier newName_Demandes
    pd.DataFrame(newTabTraite).to_csv(newName, index=False,encoding='utf-8',sep=';')
    
    return newName
       
##################################################################################################################################
##################################################################################################################################
def traitementDonneesComplet(chemin,annee,nom_Fichier_Variable,source,nom_Fichier_Modalite,path_vars,suffix_nom_schema):
    """
        Donnée : 

                annee = année de collecte
                
                chemin = le nom du dossier où se trouve le fichier csv à traiter

                nom_Fichier_Modalite est le nom exacte du fichier CSV des modalités de cette source

                source = nom de la source (ex : 'FSL')

                nom_Fichier_Variable est le nom exacte du fichier CSV des variables de cette source


        Résultat : Traite et télécharge le fichier fichier_A_traiter sous le format importable vers la base pgAdmin

    """
        
    ####### IMPORT #######
    import glob
    import pandas as pd
    import os
    import shutil # to move files 
    import pathlib # to get the path of files
    import fonctions
    from tqdm import tqdm
    ################################################################################################################

    print('Est-ce la première fois que cette source de données va être traitée ? \n',
      'Est-ce le premier millésime de cette base de données qui va être traité ? (Répondez par : OUI ou NON) ')

    OK = False

    while( not  OK):
        reponse = input().upper()

        if(reponse == ''):
            print('Veuillez répondre à la question par OUI ou NON \n ')


        elif(reponse == "OUI"):
            print("Attention ! Création d'une nouvelle liste de modalités et de variables pour cette nouvelle source de données \n")

            modalites = pd.DataFrame(columns={'CodeModalID','CodeModalEXT','LibelleModal', 'Libelle_long','Categ_regroupement'})
            modalites.to_csv(path_vars+nom_Fichier_Modalite,index=False,sep=';', encoding='utf-8')

            variables = pd.DataFrame(columns={'LibAxeAnalyse','CodeVarID','CodeVarEXT','Origine' })
                                          
            variables.to_csv(path_vars+nom_Fichier_Variable,index=False,sep=';', encoding='utf-8')
            
            posseder = pd.DataFrame(columns={'CodeVarID','CodeModalID'})
            posseder.to_csv(path_vars+'posseder_'+ suffix_nom_schema +'.csv',index=False,sep=';', encoding='utf-8')
            #{}posseder_{}.csv'.format(path_vars,suffix_nom_schema)
            

            OK = True
            new_millesime = 1

        elif(reponse == "NON"):
            print('listes de modalités et de variables déja existantes \n')
            OK = True
            new_millesime = 0

        else:
             print('Veuillez répondre à la question par OUI ou NON \n ')
                
    #choix de l'echelle des données ==> doit etre en while
    echelle_ok=False
    while(not echelle_ok):
        print(""" Veuillez Choisir l'echelle correspondant à l'echelle de vos données :\n
                        1 pour Commune
                        2 pour EPCI
                        3 pour IRIS
                        4 pour Canton
                        5 pour Logement
                        6 pour Parcelle
                        7 pour Section cadastrale
                        8 pour Département
                        9 pour Autre

                        """)
        echelleIndicatif = input()
        if(int(echelleIndicatif) == 1):
            echelle = 'Commune'
            echelle_ok = True
        elif(int(echelleIndicatif) == 2):
            echelle = 'EPCI'
            echelle_ok = True
        elif(int(echelleIndicatif) == 3):
            echelle = 'IRIS'
            echelle_ok = True
        elif(int(echelleIndicatif) == 4):
            echelle = 'Canton'
            echelle_ok = True
        elif(int(echelleIndicatif) == 5):
            echelle = 'Logement'
            echelle_ok = True
        elif(int(echelleIndicatif) == 6):
            echelle = 'Parcelle'
            echelle_ok = True
        elif(int(echelleIndicatif) == 7):
            echelle = 'Section cadastrale'
            echelle_ok = True
            
        elif(int(echelleIndicatif) == 8):
            echelle = 'Département'
            echelle_ok = True
            
        elif(int(echelleIndicatif) == 9):
            print(" Veuillez saisir l'echelle correspondant à l'echelle de vos données :\n")
            echelleSaisie = input()
            echelle = echelleSaisie
            echelle_ok = True
        else:
            print('Réponse Invalide')
            echelle_ok = False

    ########################### get all csv files ########################################
    
    cheminCsv = chemin+'/*.csv'

    csv_files = glob.glob(cheminCsv )
    dfs = [pd.read_csv(x, sep=';', encoding='utf-8') for x in csv_files]

    cheminbar = chemin + '\\'

    #removing "DossierFichiersbrutesCsv\\" files's names 
    for fsl in range(len(csv_files)):
        csv_files[fsl]= csv_files[fsl].replace(cheminbar,'')
        csv_files[fsl]= csv_files[fsl].replace('.csv','')
        
    ############## CHECKING LA LISTE DES VARIABLES ##########################
    
    # téléchargement du fichier Variables_FSL.csv', qui se trouve dans le dossier 'vars'
    
    fonctions.checkingVariable(csv_files,nom_Fichier_Variable,source,path_vars)
    
    Variables= pd.read_csv(path_vars+nom_Fichier_Variable, delimiter=';', encoding='utf-8')
    
    ############## CREATION DE LA TABLE A EXPORTER PLUS TARD ################
    
    #création d'un dossier
    os.mkdir('DossierFichiersTraités')
    
    for file in tqdm(range(len(dfs))):
        #print(file, "file")
        nomFichier= csv_files[file]
        print(' nom ::::: ', nomFichier)
        fichier_A_traiter = dfs[file]
        var = Variables.loc[Variables['CodeVarEXT'].str.contains(nomFichier, case=False)]
        var.reset_index(drop=True, inplace=True)
        codevarid= var['CodeVarID'][0] 
        

        #localisation
        currentPath = pathlib.Path().absolute()
        destination = currentPath/'DossierFichiersTraités'

        newName = fonctions.traitementDonnees(fichier_A_traiter,nomFichier,codevarid,annee,
                                              nom_Fichier_Modalite,path_vars,echelle)

        #localistion du fichier traité
        source = currentPath/newName

        # deplacer le fichier traité vers le dossier des fichiers traités
        shutil.move(str(source), str(destination))


    ######## CREATION DU FICHIER POSSEDER ###################################
    posseder= pd.read_csv('{}posseder_{}.csv'.format(path_vars,suffix_nom_schema), delimiter=';', encoding='utf-8')
    csv_files_PS = glob.glob('DossierFichiersTraités/*.csv')
    # dfs comprend la liste des fichiers CSV
    dfs_PS = [pd.read_csv(x, sep=';', encoding='utf-8') for x in csv_files_PS]
    for csv in range(len(dfs_PS)):
        fichier = dfs_PS[csv]
        fichierMask = fichier[['CodeVarID','CodeModalID']]
        tableNomcomEPCI = pd.DataFrame({'CodeVarID':[fichier['CodeVarID'][0]],
                                       'CodeModalID':[1]})
        posseder = posseder.append(tableNomcomEPCI,ignore_index = True)
        posseder = posseder.append(fichierMask,ignore_index = True)

    posseder['CC']= posseder['CodeVarID'].map(str)+posseder['CodeModalID'].map(str)
    posseder.drop_duplicates(subset ='CC',
                         keep = 'first', inplace = True, ignore_index = True)
    posseder.drop(columns=['CC'], inplace = True)

    posseder.to_csv('{}posseder_{}.csv'.format(path_vars,suffix_nom_schema),index=False,sep=';', encoding='utf-8')
        
    
    
    return new_millesime




#################################################################################################################################
#################################################################################################################################               
from ast import Try


def versementDonnes2(Nom_base,Nom_utilisateur,mot_de_passe,nom_host,port,source,nom_schema_donnees,
                    nom_Fichier_Variable,nom_Fichier_Modalite,new_millesime,path_vars,suffix_nom_schema):
    """
        Donnée : 
        
            ######## PARAMETRES :: CONNEXION à LA BASE DE DONNES #########
            
            Nom_base = 
            Nom_utilisateur = 
            mot_de_passe = 
            nom_host = 
            port = 
        
            ######## PARAMETRES :: CREATION DE TABLES #########

            nom_Fichier_Variable = 
            nom_Fichier_Modalite =
            new_millesime = 
            
            ######## PARAMETRES :: INSERTION DES DONNEES #########
            source =
            nom_schema_donnees =
            
             
    
                

        Résultat :         

    """
    ######## IMPORT #############################
    
    import glob
    import pandas as pd
    import fonctions
    from io import StringIO
    import csv
    import psycopg2
    import traceback
    from tqdm import tqdm
    ######## STEP 1 ::: CHOIX DU TRAITEMENT SELON SI C'EST UNE NOUVELLE SOURCE OU NON #####################
    variable = nom_Fichier_Variable.replace('.csv','')
    modalite = nom_Fichier_Modalite.replace('.csv','')
    posseder = 'posseder_{}'.format(suffix_nom_schema)
    
    
    if(new_millesime == 1): #premier millésime de cette source
        ######## STEP 1a ::: CREATION DES TABLES VARIABLES ET MODALITES #####################
        ########## VARIABLES ################
        for nom in glob.glob(path_vars+nom_Fichier_Variable): 
        #print(nom)

            print('Création de la table variable \n')
            nom_schema = 'Public'
            nbclE = 0
            CleFK = []

            print('Veuillez saisir la clé primaire de table variable ')
            ClePK = input()

            tableRef = []

            # attribution du fichier Variables.csv à la variable fichierCSV
            fichierCSV = pd.read_csv(nom, delimiter=';', encoding='utf-8')
            con = fonctions.connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
            fonctions.creationTableAvecFichierComplet(fichierCSV, nom, nom_schema, con, nbclE, CleFK, ClePK, tableRef,path_vars)

        ########### MODALITES ################
        for nom in glob.glob(path_vars+nom_Fichier_Modalite): 
        #print(nom)

            print('Création de la table Modalité \n')
            nom_schema = 'Public'
            nbclE = 0
            CleFK = []

            print('Veuillez saisir la clé primaire de la table Modalité ')
            ClePK = input()

            tableRef = []

            # attribution du fichier Modalite.csv à la variable fichierCSV
            fichierCSV = pd.read_csv(nom, delimiter=';', encoding='utf-8')
            fichierCSV["Libelle_long"].fillna("", inplace = True)
            con = fonctions.connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
            fonctions.creationTableAvecFichierComplet(fichierCSV, nom, nom_schema, con, nbclE, CleFK, ClePK, tableRef,path_vars)   

        ########## POSSEDER ##################

        #variable = nom_Fichier_Variable.replace('.csv','')
        #modalite = nom_Fichier_Modalite.replace('.csv','')
        #posseder = 'posseder_' + source

        for nom in glob.glob('{}posseder_{}.csv'.format(path_vars,suffix_nom_schema)): 
        #print(nom)

            print('Création de la table de jointure "Posseder" \n')
            nom_schema = 'Public'
            nbclE = 2
            CleFK = ['CodeVarID','CodeModalID']

            ClePK = ''

            tableRef = [variable, modalite]

            # attribution du fichier Modalite.csv à la variable fichierCSV
            fichierCSV = pd.read_csv(nom, delimiter=';', encoding='utf-8')
            con = fonctions.connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
            fonctions.creationTableAvecFichierComplet(fichierCSV, nom, nom_schema, con, nbclE, CleFK, ClePK, tableRef, path_vars) 



        ######## STEP 1b ::: INSERTION DES DONNEES DES TABLES VARIABLES ET MODALITES  #######################################


            ########## VARIABLES ################
        print('Insertion de données dans la table variable \n')
        for nom in glob.glob(path_vars+nom_Fichier_Variable):
             # attribution du fichier Variables_FSL.csv à la variable fichierCSV
            fichierCSVpath = nom
            con = connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
            table = variable.lower()
            print('table variable avant insertion', table)
            sep = ';'
            fonctions.insertionDonnees(fichierCSVpath, con, table, sep)

            ########### MODALITES ################
        print('Insertion de données dans la table Modalité \n')
        for nom in glob.glob(path_vars+nom_Fichier_Modalite):
             # attribution du fichier Variables_FSL.csv à la variable fichierCSV
            fichierCSVpath = nom
            con = connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
            table = modalite.lower()
            sep = ';'
            fonctions.insertionDonnees(fichierCSVpath, con, table, sep)

            ########## POSSEDER ##################
        print('Insertion de données dans la table de jointure "Posseder" \n')
        for nom in glob.glob('{}posseder_{}.csv'.format(path_vars,suffix_nom_schema)):
             # attribution du fichier Variables_FSL.csv à la variable fichierCSV
            fichierCSVpath = nom
            con = connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
            table = posseder.lower()
            sep = ';'
            fonctions.insertionDonnees(fichierCSVpath, con, table, sep)
            
        ########### STEP 1c ::: CREATION DES NOUVELLES TABLES DE DONNEES  ##################
        csv_files, path = glob.glob('DossierFichiersTraités/*.csv'), glob.glob('DossierFichiersTraités/*.csv')

        # dfs comprend la liste des fichiers CSV
        dfs = [pd.read_csv(x, sep=';', encoding='utf-8') for x in csv_files]

        for i in range(len(csv_files)):
            csv_files[i]= csv_files[i].replace('DossierFichiersTraités\\','')
        
        for fichier in tqdm(range(len(csv_files))):

            fichierCSV = dfs[fichier]
            ClePK = fichierCSV.columns[-2]
            nom = csv_files[fichier]
            nom_schema_donnees = nom_schema_donnees
            con = fonctions.connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
            nbclE = 2  
            tableRef = [variable, modalite]
            CleFK = [fichierCSV.columns[0], fichierCSV.columns[3]]
            table = nom.replace('.csv','').lower()
            try:
                con = connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
                print('Création de la table des données {} \n'.format(table))
                nomTableCree = fonctions.creationTableAvecFichierComplet(fichierCSV, nom, nom_schema_donnees,con, nbclE, CleFK, ClePK, tableRef, path_vars)
                #table = str(nom_schema_donnees + "."+nomTableCree[0]).lower()
                sep = ';'
                fichierCSVpath = path[fichier]
                print('Insertion de données \n')
                table = str(nom_schema_donnees+ "."+nom.replace('.csv','').lower())
                fonctions.insertionDonnees2(fichierCSVpath, con, table,sep)

            except (Exception, NameError, psycopg2.Error) as error :
                    print(traceback.format_exc())
                    print ("Erreur lors de l'insertion des données importées dans la table dans le try :", error)
                    con.rollback()
        
    else: #il existe déja d'autres millésime de cette source
        ######## STEP 2 ::: Mise à jour des Tables existantes #####################

        # création de la liste des tables existantes de la source (Publique comme schema privé)
        con = fonctions.connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)

                # création du dictionaire qui contient les tables existantes
        dictCons = fonctions.dict_cleEtrangere(nom_schema_donnees,Nom_base,Nom_utilisateur,mot_de_passe,nom_host,port)

        try :
            if(len(dictCons)!=0):
                ##################### broking the foreign keys ##################
                for key, value in dictCons.items():
                    print('DROPPING foreign keys')
                    for cons in range(len(value)):
                        drop_Query = "ALTER TABLE "+nom_schema_donnees.lower()+"." +key+" "+"DROP CONSTRAINT "+ value[cons]+";"
                        with con.cursor() as c:
                            c.execute(drop_Query)
                            con.commit()
                            #con.close()
                        
            ########## VARIABLES ################
            print('Mise à jour de la table variable \n')
            for nom in glob.glob(path_vars+nom_Fichier_Variable):
                fichierCSV = pd.read_csv(nom, delimiter=';', encoding='utf-8')
                con = fonctions.connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
                table=variable.lower()
                sep = ';'
                fonctions.copy_from_stringio(con, fichierCSV, table, sep)

            ########### MODALITES ################
            print('Mise à jour de la table Modalité \n')
            for nom in glob.glob(path_vars+nom_Fichier_Modalite):
                fichierCSV = pd.read_csv(nom, delimiter=';', encoding='utf-8')
                con = fonctions.connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
                table = modalite.lower()
                sep = ';'
                fonctions.copy_from_stringio(con, fichierCSV, table, sep)

            ########## POSSEDER ##################
            print('Insertion de données dans la table de jointure "Posseder" \n')
            for nom in glob.glob('{}posseder_{}.csv'.format(path_vars,suffix_nom_schema)):
                fichierCSV = pd.read_csv(nom, delimiter=';', encoding='utf-8')
                con = fonctions.connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
                table=posseder.lower()
                sep = ';'
                fonctions.copy_from_stringio(con, fichierCSV, table, sep)

            ########## MISE A JOUR DES TABLES DE DONNEES EXISTANTES ###################

            csv_files, path = glob.glob('DossierFichiersTraités/*.csv'), glob.glob('DossierFichiersTraités/*.csv')

            # dfs comprend la liste des fichiers CSV
            dfs = [pd.read_csv(x, sep=';', encoding='utf-8') for x in csv_files]

            for i in range(len(csv_files)):
                csv_files[i]= csv_files[i].replace('DossierFichiersTraités\\','')

            for fichier in tqdm(range(len(csv_files))):

                fichierCSV = dfs[fichier]
                fichierCSVpath = path[fichier]
                ClePK = fichierCSV.columns[-2]
                nom = csv_files[fichier]
                nom_schema_donnees = nom_schema_donnees
                #con = connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
                nbclE = 2  
                tableRef = [variable, modalite]
                CleFK = [fichierCSV.columns[0], fichierCSV.columns[3]]
                table = nom.replace('.csv','').lower()
                sep = ';'

                con = fonctions.connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
                cur = con.cursor()
                sqlCheckTable = "SELECT EXISTS ( SELECT FROM pg_tables WHERE schemaname = "+\
                            "{nom_schema_donnees} AND tablename  = {table} );"
                sqlCheckTable= sqlCheckTable.format(nom_schema_donnees="'"+nom_schema_donnees+"'", table="'"+table+"'")
                cur.execute(sqlCheckTable)
                result = cur.fetchall()
                #print('result[0][0] {}'.format(result[0][0]))
                if(result[0][0]==True):
                    print("Mise à jour de la table {}\n".format(table))
                    table = str(nom_schema_donnees+ "."+nom.replace('.csv','').lower())
                    #fichierCSV = pd.read_csv(fichierCSVpath, delimiter=sep)
                    fonctions.insertionDonnees2(fichierCSVpath, con, table, sep)

                else:
                    print('Création de la table des données {} \n'.format(table))
                    nomTableCree = fonctions.creationTableAvecFichierComplet(fichierCSV, nom, nom_schema_donnees,con, nbclE, CleFK, ClePK, tableRef, path_vars)
                    table = str(nom_schema_donnees + "."+nomTableCree[0]).lower()
                    sep = ';'
                    #fichierCSVpath = path[fichier]
                    print('Insertion de données \n')
                    table = str(nom_schema_donnees+ "."+nom.replace('.csv','').lower())
                    fonctions.insertionDonnees2(fichierCSVpath, con, table, sep)

        except (Exception, NameError, psycopg2.Error) as error :
            print(traceback.format_exc())
            print ("Erreur lors de l'insertion des données importées dans la table dans le try :", error)
            con.rollback()


        finally:
            ################################ putting back the foreign keys ############################
            fk_columns = ["codevarid", "codemodalid"]
            parent_table = [variable.lower() , modalite.lower()]
            parent_key_columns = ["codevarid", "codemodalid"]

            con = fonctions.connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
            if(len(dictCons)!=0):
                for key, value in dictCons.items():
                    print('RE-ADDING foreign keys')
                    for cons in range(len(value)):
                        re_add_fk_Query = str("ALTER TABLE ")+nom_schema_donnees.lower()+str(".") +key+str(" ADD CONSTRAINT ")+value[cons] +str(" FOREIGN KEY (")+fk_columns[cons]+str(") REFERENCES ")+parent_table[cons]+str("(") +parent_key_columns[cons]+str(");")
                        with con.cursor() as c:
                            c.execute(re_add_fk_Query)
                            con.commit()
                            #con.close()

##################################################################################################################################
def traitement_versement(annee,chemin,nom_Fichier_Modalite,source,nom_Fichier_Variable,
                        Nom_base,Nom_utilisateur,mot_de_passe,nom_host,port,nom_schema_donnees, path_vars,suffix_nom_schema):
    """
        Donnée : 

                annee = année de collecte
                
                chemin = le nom du dossier où se trouve le fichier csv à traiter

                nom_Fichier_Modalite est le nom exacte du fichier CSV des modalités de cette source

                source = nom de la source (ex : 'FSL')

                nom_Fichier_Variable est le nom exacte du fichier CSV des variables de cette source
                
                Nom_base est un string qui represente le nom de la base de données à la quelle on souhaite se connecter
                
                Nom_utilisateur est un string qui represente le nom de pgAdmin de l'utilisateur qui souhaite de connecter
                
                mot_de_passe est un string qui represente le mot de passe de l'utilisateur
                
                nom_host est un string qui represente le nom de l'hebergeur de la base de données
                
                port est un string numerique qui represente le port de connexion à la base de données
                
                nom_schema_donnees = 
                
                path_vars =
                
                suffix_nom_schema =

        Résultat : Dans un premier temps, cette fonction traite et télécharge le fichier fichier_A_traiter sous le format 
                    exportable vers la base pgAdmin, et dans un second temps, elle effectue l'export sur pgAdmin
    """
    import glob
    import pandas as pd
    import os
    import shutil # to move files 
    import pathlib # to get the path of files
    from io import StringIO
    import csv
        
    print('PREMIERE PARTIE : TRAITEMENT DES DONNEES \n')
    
    
    new_millesime = traitementDonneesComplet(chemin,annee,nom_Fichier_Variable,source,nom_Fichier_Modalite,path_vars)
    print('\n FIN DE LA PREMIERE \n')
    
    
    ######## CREATION DU FICHIER POSSEDER ###################################
    posseder= pd.read_csv('{}posseder_{}.csv'.format(path_vars,suffix_nom_schema), delimiter=';')
    csv_files_PS = glob.glob('DossierFichiersTraités/*.csv')
    # dfs comprend la liste des fichiers CSV
    dfs_PS = [pd.read_csv(x, sep=';') for x in csv_files_PS]
    for csv in range(len(dfs_PS)):
        fichier = dfs_PS[csv]
        fichierMask = fichier[['CodeVarID','CodeModalID']]
        tableNomcomEPCI = pd.DataFrame({'CodeVarID':[fichier['CodeVarID'][0]],
                                       'CodeModalID':[1]})
        posseder = posseder.append(tableNomcomEPCI,ignore_index = True)
        posseder = posseder.append(fichierMask,ignore_index = True)

    posseder['CC']= posseder['CodeVarID'].map(str)+posseder['CodeModalID'].map(str)
    posseder.drop_duplicates(subset ='CC',
                         keep = 'first', inplace = True, ignore_index = True)
    posseder.drop(columns=['CC'], inplace = True)

    posseder.to_csv('{}posseder_{}.csv'.format(path_vars,suffix_nom_schema),index=False,sep=';', encoding='utf-8')
    
    print('DEUXIEME PARTIE : VERSEMENT DES DONNEES \n')
    versementDonnes2(Nom_base,Nom_utilisateur,mot_de_passe,nom_host,port,source,nom_schema_donnees,
                    nom_Fichier_Variable,nom_Fichier_Modalite,new_millesime,path_vars,suffix_nom_schema)

    #suppression du dossier temporaire 
    try:
        shutil.rmtree('DossierFichiersbrutesCsv')
        shutil.rmtree('DossierFichiersTraités')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    
#######################################################################################################################################
#######################################################################################################################################
def copy_from_stringio(con, df, table,sep):

    """
    Here we are going save the dataframe in memory 
    and use copy_from() to copy it to the table
    """
    from io import StringIO
    import psycopg2
    # save dataframe to an in memory buffer
    buffer = StringIO()
    df.to_csv(buffer, index=False, header = False, sep=sep, encoding='utf-8')
    buffer.seek(0)
    cursor = con.cursor()
    try:
        cursor.execute('TRUNCATE'+' '+ table +' CASCADE;')
        cursor.copy_from(buffer, table, sep=";")
        
    except (Exception, psycopg2.DatabaseError) as error:        
        print("Error: %s" % error)
        con.rollback()
        cursor.close()
    
    else:
        con.commit()
        cursor.close()
        print("Les données importées ont été inserées avec succès dans la table \n")
    return 1
    
#########################################################################################################################################
##########################################################################################################################################
def repmplacerCaratereSpeciaux(fichier_A_traiter):
    """
    Donnée : fichier_A_traiter est le fichier (csv ou des sheets excel) original à traiter
             
             
    Résultat : retourne fichier_A_traiter avec des noms de colonnes sans caractères spéciaux
    """
    
    # création de la liste des noms de colonnes de fichier_A_traiter
    listeCols = fichier_A_traiter.columns
    listeCols.tolist()
    
    tabNewColonnes = []
    
    for i in range(len(listeCols)):
        new_name = listeCols[i]
        string1 = new_name[0]
        if(string1.isnumeric()):
            new_name = new_name.replace(string1, '_'+string1,1)   

        if(('+') in new_name):
            new_name = new_name.replace('+', 'plus')
            

        if(('-') in new_name):
            new_name = new_name.replace('-', 'moins')
            

        if(('<') in new_name):
            new_name = new_name.replace('<', 'inf')
            

        if(('>') in new_name):
            new_name = new_name.replace('>', 'sup')
            

        if(('=') in new_name):
            new_name = new_name.replace('=', 'egal')
            

        tabNewColonnes.append(new_name)

    
    fichier_A_traiter.columns = tabNewColonnes


    
##########################################################################################################################################
##########################################################################################################################################
def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value
        
##########################################################################################################################################
##########################################################################################################################################

def dict_cleEtrangere(nom_schema_donnees,Nom_base,Nom_utilisateur,mot_de_passe,nom_host,port):
    """
    Donnée : nom_schema_donnees est le nom du schéma duquel l'on veut obtenir la liste des tables et de leurs clés étrangères
             Nom_base est un string qui represente le nom de la base de données à la quelle on souhaite se connecter
             Nom_utilisateur est un string qui represente le nom de pgAdmin de l'utilisateur qui souhaite de connecter
             mot_de_passe est un string qui represente le mot de passe de l'utilisateur
             nom_host est un string qui represente le nom de l'hebergeur de la base de données
             port est un string numerique qui represente le port de connexion à la base de données
    
    Résultat : retourne un dictionaire contenant les tables en clés (key) et les relations (constraints) étrangères en valeurs
    """
    import pandas as pd
    # getting all the foreign keys per table
    con = connexion(Nom_base, Nom_utilisateur, mot_de_passe, nom_host, port)
    cur = con.cursor()
    sqlCheckTable = "SELECT  INFORMATION_SCHEMA.TABLE_CONSTRAINTS.constraint_name ,INFORMATION_SCHEMA.TABLE_CONSTRAINTS.table_name "+\
                    "FROM  INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_TYPE='FOREIGN KEY' "+\
                    "AND INFORMATION_SCHEMA.TABLE_CONSTRAINTS.table_schema = {nom_schema_donnees}"

    sqlCheckTable= sqlCheckTable.format(nom_schema_donnees="'"+nom_schema_donnees+"'")
    cur.execute(sqlCheckTable)
    result = cur.fetchall()
    #print(result)

    # turning the result into a dataframe
    tab_cons = pd.DataFrame(columns={'constraint_name',  'table_name'})
    for res in range(len(result)):
        cons_name = result[res][0]
        tab_name = result[res][1]
        tab_cons = tab_cons.append({
            'constraint_name':cons_name,
            'table_name':tab_name
        },ignore_index=True)


    #turning the result into a dictionnary
    dict_cons = {}
    if(len(tab_cons)!=0):
        dict_cons[tab_cons.table_name[0]] = tab_cons.constraint_name[0]
        tab = 1
        while(tab < len(tab_cons)):

            if(tab_cons.table_name[tab] == tab_cons.table_name[tab - 1]):
                append_value(dict_cons, tab_cons.table_name[tab - 1], tab_cons.constraint_name[tab])

            else:
                append_value(dict_cons, tab_cons.table_name[tab], tab_cons.constraint_name[tab])
            tab += 1
        
    return dict_cons
    
##########################################################################################################################################
##########################################################################################################################################

