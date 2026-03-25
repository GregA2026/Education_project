# Education_project
Projet Final de la DAFS-FT-17 (Jedha Bootcamp).

# Notre projet final de certification!  

![final project](https://images.pexels.com/photos/669610/pexels-photo-669610.jpeg?_gl=1*9ifwbs*_ga*MjAzMjYyNjU3Ni4xNzcxNDIzNDY0*_ga_8JE65Q40S6*czE3NzE0MjM0NjQkbzEkZzEkdDE3NzE0MjM2NTIkajU5JGwwJGgw)

# A propos du Dataset  

Ce jeu de données contient les données du baccalauréat en France par académie.  
Les données sont aggrégées par académie, voie, statut du candidat, genre, série, diplôme et session pour les années 2021 à 2025.  
Les données numériques aggrégées sont le nombre d'inscrits, de présents, d'admis, de refusés, de mentions obtenues selon les différentes mentions et nombre de passage au rattrapage.  

# Problèmatique liée au projet  

Quels sont les facteurs régionaux et démographiques qui influencent les performances des élèves en France au baccalauréat ?  
Peut-on prédire le taux de réussite et les mentions efficacement à partir de ces données ?  

# Data  

CSV file : fr-en-baccalaureat-par-academie    

## Source du dataset :  

https://www.data.gouv.fr/datasets/le-baccalaureat-par-academie  

# Environnement

Vous devez installer les différentes librairies d'envrionnement pour executer les notebooks présent dans la section "mention" et "streamlit"  
Ecrivez dans votre terminal :  

```powershell  
pip install -r requirements.txt  
```  

Pour la section "mention" présent dans le dossier "mention" de notre repository.  
Pour la section "streamlit" présent dans le dossier "streamlit" de notre repository.  

# Architecture

```
├── data
│   └── clean_dataset.csv
│   └── fr-en-baccalaureat-par-academie.csv
├── mention
│   └── EDA.ipynb
│   └── ML1_mention.ipynb
│   └── ML2_proportion.ipynb
│   └── ML3_mention_majoritaire.ipynb
│   └── requirements.txt
├── powerBI
│   └── education_academie.pbix
├── streamlit
│   └── data/
│   │   └── bac_prepared.csv
│   └── .gitattributes
│   └── README.md
│   └── app.py
│   └── model_bac.pkl
│   └── requirements.txt
│   └── taux_reussite_regress.ipynb
├── .gitignore
├── README.md
```
# Contenu du repositorie  

📁 data :  
  dataset original et dataset nettoyé pour le Machine Learning des mentions  
  
📁 mention :  
  EDA du datset dédié aux mentions accompagné de 3 approches de prédictions grâce à du Machine Learning  
  
📁 streamlit :  
  Machine Learning pour prédire le taux de réussite et application streamlit associé (hégergé sur huggingface)  
  
📁 powerBI :  
  présentation powerBI du dataset  

## lien Huggingface

https://huggingface.co/spaces/smithhannah/projet_taux_reussite_bac

# Membre de l'équipe

- Hannah Smith 
- Eric Tabiou 
- Patrick Grouillet 
- Antoine Smith 
- Grégory Augis 

# Demoday

Date : 2026-03-27
