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


# FAQ

## Question 1 : Comment assurer la cohérence avec les fichiers locaux après une modification de table ou téléchargement de fichiers depuis pgAdmin 4 ?

Après un téléchargement depuis pgAdmin, il faut s'assurer que le séparateur de texte du fichier téléchargé est ';'. Ceci en le réenregistrant via Excel et en choisissant ';' comme séparateur. Il faut aussi s'assuer que l'encodage soit en utf8.
Voici des exemples de comment faire :

### Fichier des Modalités
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
### Fichier des Variables
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

### Fichier de jointure Posseder
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














