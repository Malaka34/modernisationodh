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