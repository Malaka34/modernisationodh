---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
![](Bandeau_seul_ODH.png)

# FAQ

## 1- Comment assurer la cohérence avec les fichiers locaux après une modification de table ou téléchargement de fichiers depuis pgAdmin 4 ?

Après un téléchargement depuis pgAdmin, il faut s'assurer que le séparateur de texte du fichier téléchargé est **`';'`**. Ceci en le réenregistrant via Excel et en choisissant  **`';'`** comme séparateur. Il faut aussi s'assurer que l'encodage soit en **`utf-8`**.
    Voici des exemples de comment faire :

### a- Fichier des Modalités
```{code-cell}
# Chargement du fichier des modalités (explain all the params)
Modalites = pd.read_csv(path_vars+nom_Fichier_Modalite, delimiter=';', encoding='latin1')
```


```{code-cell}
# renommage des colonnes (explain why ?)
Modalites.rename(columns={'codemodalid':'CodeModalID', 'categ_regroupement':'Categ_regroupement', 'libelle_long	':'Libelle_long', 'codemodalext':'CodeModalEXT', 'libellemodal':'LibelleModal'}, inplace=True)
```


```{code-cell}
# Enregistrement des modifications
Modalites.to_csv(path_vars+nom_Fichier_Modalite,index=False,sep=';', encoding='utf-8')
```
### b-Fichier des Variables
```{code-cell}
# Chargement du fichier des modalités (explain all the params)
Variables = pd.read_csv(path_vars+nom_Fichier_Variable,sep=';',encoding='latin1')
```


```{code-cell}
# renommage des colonnes (explain why ?)
Variables.rename(columns={'codevarid':'CodeVarID','libaxeanalyse':'LibAxeAnalyse','origine':'Origine','codevarext':'CodeVarEXT'},inplace=True)
```


```{code-cell}
# Enregistrement des modifications
Variables.to_csv(path_vars+nom_Fichier_Variable,index=False,sep=';',encoding='utf-8')
```

### c- Fichier de jointure Posseder
```{code-cell}
# Chargement du fichier des modalités (explain all the params)
Posseder = pd.read_csv(path_vars+'posseder_aides_personne.csv',sep=',',encoding='utf-8')
```


```{code-cell}
# renommage des colonnes (explain why ?)
Posseder.rename(columns={'codevarid':'CodeVarID','codemodalid':'CodeModalID'},inplace=True)
```


```{code-cell}
# Enregistrement des modifications
Posseder.to_csv(path_vars+'posseder_aides_personne.csv',index=False,sep=';',encoding='utf-8')
```
## 2- Erreur UnicodeDecodeError
Cette erreur se produit lorsque vous essayez d'ouvrir un fichier avec l'encodage **`utf-8`**, alors qu'il est encodé différement.
```{code-cell}
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 1665: invalid continuation byte
```
Pour régler ce problème, exécutez les mêmes cellules que dans la question précédente, sauf la cellule du renommage.


## 3- Erreur FileExistsError: [WinError 183] 
Lorsque vous rencontrez sur ce type d'erreur comme par exemple :

```{code-cell}
FileExistsError: [WinError 183] Impossible de créer un fichier déjà existant: 'DossierFichiersTraités'
```
Cela indique que vous essayer de créer un dossier qui existe déjà. Vous devez donc supprimer le dossier existant et réexécuter votre code.


## 4- Erreur ModuleNotFoundError 
Ce type d'erreur se produit quand vous essayez d'utiliser une bibliothèque / un package non importé.

```{code-cell}
ModuleNotFoundError: No module named 'fonctions'
```
Dans cet exemple, c'est parce que le chemin d'accès au fichier **`fonctions.py`** n'est pas spécifié correctement. la ligne de code suivante doit être modifiée :

```{code-cell}
sys.path.insert(0, r"C:/Users/malaka/Documents/BDD")  # à adapter a partir de malaka
```


## 5- Erreur AttributeError

```{code-cell}
AttributeError: 'NoneType' object has no attribute 'cursor'
```
lorsque le mauvais mot de passe et/ou  nom d'utilisateur est entré pour se connecter au serveur.


## 6- Erreur psycopg2.errors.UniqueViolation

```{code-cell}
psycopg2.errors.UniqueViolation: ERREUR:  la valeur d'une clé dupliquée rompt la contrainte unique « age_demandeur_attribution_pkey »
DETAIL:  La clé « (indiceposition)=(15340031522020) » existe déjà.
```
Cela indique que vous avez peut-être entré le paramètre de l'année de manière incorrecte.

![](logo_bandeau.jpg)


