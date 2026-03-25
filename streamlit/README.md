---
title: "Anticiper la Réussite au Bac"
colorFrom: "blue"
colorTo: "green"
sdk: "streamlit"
sdk_version: "1.24.1"
python_version: "3.11"
app_file: "app.py"
pinned: false
---

# Anticiper la Réussite au Baccalauréat

> Ce projet permet d’anticiper les performances au baccalauréat afin d’identifier en amont les groupes à risque et d’optimiser les actions pédagogiques à l’échelle des académies.
> 

---

## Contexte & Problématique

Le taux de réussite au baccalauréat varie selon de nombreux facteurs : série, académie, statut du candidat, etc.

Aujourd’hui, les décisions pédagogiques sont souvent prises **après les faits**, une fois les résultats connus.

-> Problème :

- difficulté à **anticiper les performances**
- manque d’outils pour **cibler les groupes à risque**
- allocation des ressources souvent non optimisée

---

## Objectif

Développer un outil permettant de :

- prédire le **taux de réussite au bac**
- identifier les **groupes en difficulté**
- fournir une **aide à la décision pédagogique**

Cette partie du projet repose sur :

- un **modèle de machine learning**
- une **application interactive Streamlit**

---

## Modèle de Machine Learning

### Type de modèle

Modèle de **régression Ridge** intégré dans un pipeline complet :

- encodage des variables catégorielles
- standardisation
- modèle de régression régularisée

-> Sauvegardé avec `joblib` (`model_bac.pkl`)

---

### Variables utilisées

- Série
- Sexe
- Statut du candidat
- Académie
- `taux_hist` (taux de réussite historique)

-> Cette variable est clé : elle introduit une **mémoire des performances passées**.

---

### Optimisation

- sélection des variables pertinentes
- gestion de la multicolinéarité avec Ridge
- tuning des hyperparamètres
- pipeline complet pour éviter toute incohérence entre entraînement et prédiction

---

## Performance du modèle

### Métriques

- **R² (coefficient de détermination)**
- **MAE (Mean Absolute Error)**

---

### Résultats

- **R² :** `0.82`
- **MAE :**  `3.32 points de pourcentage`

---

### Interprétation

- Le modèle explique une part importante de la variance du taux de réussite.
- L’erreur moyenne est de **±3.32 points**.

-> Exemple :

> Une prédiction à 82% correspond généralement à un taux réel entre ~78.7% et ~85.3%.
> 

---

## Interprétation Business

### Utilité concrète

Le modèle permet de passer d’une logique **réactive** (analyse après résultats), à une logique **proactive** (anticipation avant examens)

---

### 1. Identification des groupes à risque

- taux prédit < 75%
- détection des groupes nécessitant une attention prioritaire

-> Impact :

- mise en place de soutien ciblé
- réduction des échecs

---

### 2. Priorisation des actions

- allocation des ressources sur les groupes critiques
- optimisation du temps des enseignants

---

### 3. Pilotage académique

- vision globale des performances :
    - 🔴 mauvaises
    - 🟠 modérées
    - 🟢 bonnes

-> aide à la décision stratégique

---

### Cas d’usage

- établissements scolaires
- enseignants
- institutions publiques

---

### Limites

- modèle dépendant des données historiques
- ne capture pas tous les facteurs externes (sociaux, pédagogiques)
- outil d’aide à la décision, pas de décision automatique

---

## Application Streamlit

L’application :

1. charge le modèle (`joblib`)
2. charge les données préparées
3. applique directement le pipeline
4. génère les prédictions

-> Aucun preprocessing nécessaire côté app

---

### Fonctionnalités

### Scan académique

- analyse automatique par académie
- classement des groupes par performance

---

### KPIs

- nombre de groupes :
    - 🔴 mauvaise performance
    - 🟠 modérée
    - 🟢 bonne

---

### Export

- téléchargement CSV des résultats

---

### Recommandations

- soutien intensif
- examens blancs
- suivi individualisé
- ateliers méthodologiques

---

## Architecture

```
├── app.py
├── model_bac.pkl
├── data/
│   └── bac_prepared.csv
│   └── fr-en-baccalaureat-par-academie.csv
├── taux_reussite_regress.ipynb
└── README.md
```

---

## Problèmes rencontrés

### Données

- données hétérogènes
- besoin de nettoyage et harmonisation

---

### Feature engineering

- difficulté à intégrer le temps (la feature “Session” a une corrélation d’environ -0.08 avec le taux de réussite)
-> solution : création de feature `taux_hist`

---

### Modélisation

- testé plusieurs modèles (Ridge, Random Forest, XGBoost), et fait une cross-validation (K-Folds)
-> Meilleur modèle: Ridge

---

### Déploiement

- cohérence preprocessing / app
-> pipeline complet sauvegardé

---

## Choix techniques

| Élément | Choix | Pourquoi |
| --- | --- | --- |
| Modèle | Ridge Regression | robuste, interprétable, meilleur R² |
| App | Streamlit | facile à utiliser |
| Sauvegarde | joblib | standard ML |
| Visualisation | Plotly | interactif |

---

## Améliorations possibles

- ajout de variables socio-économiques
- utiliser un dataset avec des données par individuel, pas seulement pas groupe aggrégé

---

## Source des données

Données publiques :

https://www.data.gouv.fr/datasets/le-baccalaureat-par-academie

---