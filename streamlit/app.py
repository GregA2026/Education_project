import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Anticiper la Réussite au Baccalauréat",
    layout="wide",
    page_icon="🎓"
)

## CHARTE GRAPHIQUE
# couleurs issues du dahsboard Power BI Taux de réussite
BLEU   = "#3F44A6"
BLANC  = "#F2F2F2"
ROUGE  = "#D90416"

# header coloré 
st.markdown(f"""
<style>
    h2, h3 {{ color: {BLEU} !important; }}
</style>
""", unsafe_allow_html=True)

## CHARGEMENT DES DONNEES
# Modèle et données chargés une seule fois grâce au cache streamlit.
# bac_prepared.csv est exporté depuis le notebook ML
# - il contient déjà toutes les transformations (aggrégation, harmonisation, taux_hist)

@st.cache_resource
def load_model():
    # Pipeline Ridge complet (préprocesseur + modèle) -- joblib
    return joblib.load("model_bac.pkl")

@st.cache_data
def load_data():
    # Dataset préparé en sortie du notebook - aucun preprocessing nécessaire ici
    return pd.read_csv("data/bac_prepared.csv")

## CONSTANTES

# Voie est exclue du modèle (redondante avec Série) mais sert à guider
# l'utilisateur : il choisit d'abord la voie, puis la série filtrée
VOIE_SERIES = {
    "BAC_GENERAL": ["BAC GENERAL"],
    "BAC TECHNOLOGIQUE": ["BAC S2TMD", "BAC ST2S", "BAC STAV", "BAC STD2A",
                           "BAC STHR", "BAC STI2D", "BAC STL", "BAC STMG"],
    "BAC PROFESSIONNEL": ["BAC PRO PROD", "BAC PRO PRODUCTION AGRI", "BAC PRO PRODUCTION MEN",
                           "BAC PRO SERV", "BAC PRO SERVICES AGRI", "BAC PRO SERVICES MEN"],
}

# seuils de performance
SEUIL_MAUVAIS = 75
SEUIL_BON = 90

## FONCTIONS UTILITAIRES

def get_taux_hist(df, serie, sexe, statut, academie):
    """
    Récupère le taux_hist du groupe dans le dataset (dernière session connue).
    Fallback sur la moyenne globale si le groupe n'existe pas dans le dataset.
    """
    grp = df[
        (df["Série"] == serie) &
        (df["Sexe"] == sexe) &
        (df["Statut du candidat"] == statut) &
        (df["Libellé académie"] == academie)
    ]
    if grp.empty:
        return df["taux_reussite"].mean()
    return grp["taux_hist"].iloc[-1]


def predict(model, serie, sexe, statut, academie, taux_hist):
    """
    Construit le DataFrame d'entrée attendu par le pipeline et retourne
    la prédiction clippée entre 0 et 100.
    """
    X = pd.DataFrame([{
        "Série":               serie,
        "Sexe":                sexe,
        "Statut du candidat":  statut,
        "Libellé académie":    academie,
        "taux_hist":           taux_hist,
    }])
    return float(np.clip(model.predict(X)[0], 0, 100))

def performance(t):
    """
    Etiquette de performance selon les seuils définis.
    """
    if t < SEUIL_MAUVAIS: return "Mauvaise"
    elif t < SEUIL_BON: return "Modérée"
    else: return "Bonne"

def color_perf(val):
    """Couleurs rouge/orange/vert pour le tableau — convention universelle."""
    colors = {
        "Mauvaise": "background-color:#FCEBEB; color:#A32D2D",
        "Modérée":  "background-color:#FAEEDA; color:#854F0B",
        "Bonne":    "background-color:#EAF3DE; color:#27500A",
    }
    return colors.get(val, "")


## INITIALISATION

model     = load_model()
df        = load_data()
academies = sorted(df["Libellé académie"].unique())
statuts   = sorted(df["Statut du candidat"].unique())

## HEADER
col_logo, _ = st.columns([1, 3])

with col_logo:
    st.markdown(f"""
    <a href="https://www.data.gouv.fr/datasets/le-baccalaureat-par-academie" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/fr/thumb/e/ec/MIN_Education_Nationale_et_Jeunesse_RVB.jpg/960px-MIN_Education_Nationale_et_Jeunesse_RVB.jpg" width="120">
    </a>
    """, unsafe_allow_html=True)

    st.caption("*Cliquez sur l'image pour accéder au dataset utilisé*")


## SCAN ACADEMIQUE
# Prédiciton automatique pour tous les groupes d'une académie,
# triés par taux croissant pour identifier les groupes à risque

st.title("Anticiper la Réussite au Baccalauréat", text_alignment="center", width="stretch")
st.subheader("Outil de simulation et d'analyse des performances par académie, pour préparer la prochaine session de bac.", width="stretch", text_alignment="center")

c1, c2, c3 = st.columns(3)
academie_scan = c1.selectbox("Académie", academies, key="acad_scan")
serie_scan = c2.selectbox("Série", ["Toutes"] + sorted(df["Série"].unique()), key="series_scan")
statut_scan = c3.selectbox("Statut", ["Tous"] + statuts, key="statut_scan")

# filtres sur série et statut
df_scan = df[df["Libellé académie"] == academie_scan].copy()
if serie_scan != "Toutes": df_scan = df_scan[df_scan["Série"] == serie_scan]
if statut_scan != "Tous": df_scan = df_scan[df_scan["Statut du candidat"] == statut_scan]

# on garde la dernière session connue par groupe - taux_hist le plus récent
df_latest = (df_scan.sort_values("Session")
                .groupby(["Série", "Sexe", "Statut du candidat", "Libellé académie"], as_index=False)
                .last())
    
# prédiciton pour chaque groupe
df_latest["taux_prédit"] = df_latest.apply(
    lambda r: round(predict(model, 
                            r["Série"], 
                            r["Sexe"], 
                            r["Statut du candidat"],
                            r["Libellé académie"],
                            r["taux_hist"]
                        ), 1), axis=1
)
df_latest = df_latest.sort_values("taux_prédit")
df_latest["Performance"] = df_latest["taux_prédit"].apply(performance)

# Vérification : aucun groupe trouvé avec ces filtres
if df_latest.empty:
    st.warning("Aucun groupe trouvé pour cette sélection. Essayez d'élargir les filtres.")
    st.stop()

# KPIs 
st.subheader("Nombre de groupes par niveau de performance")
k1, k2, k3 = st.columns(3)
k1.metric("Mauvaise Performance", (df_latest["Performance"] == "Mauvaise").sum())
k2.metric("Performance Modérée", (df_latest["Performance"] == "Modérée").sum())
k3.metric("Bonne Performance", (df_latest["Performance"] == "Bonne").sum())

# légende des couleurs
st.markdown(f"""
---
**Guide de lecture**
 
🔴 **Mauvaise** — taux prédit < {SEUIL_MAUVAIS} % : groupe nécessitant une attention prioritaire  
🟠 **Modérée** — taux prédit entre {SEUIL_MAUVAIS} % et {SEUIL_BON} % : groupe à surveiller  
🟢 **Bonne** — taux prédit > {SEUIL_BON} % : groupe dans les normes attendues
 
---
""")

# tableau 
df_display = df_latest[
    ["Série", "Sexe", "Statut du candidat", "taux_prédit", "Performance"]
].copy()
df_display.columns = ["Série", "Sexe", "Statut", "Taux prédit (%)", "Performance"]

st.dataframe(
    df_display.style
        .applymap(color_perf, subset=["Performance"])
        .format({"Taux prédit (%)": "{:.1f}"}),
    use_container_width=True,
    hide_index=True
)

# bouton d"export en csv
csv = df_display.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇ Télécharger CSV",
    csv,
    file_name=f"scan_{academie_scan}.csv",
    mime="text/csv"
)

## RECOMMANDATIONS
n_mauvais = (df_latest["Performance"] == "Mauvaise").sum()
n_modere = (df_latest["Performance"] == "Modérée").sum()

if n_mauvais > 0 or n_modere > 0:
    st.subheader("Recommandations")
    st.caption("*Actions suggérées selon le niveau de performance prédit.*")

if n_mauvais > 0:
    with st.expander(f"Groupes à performance mauvaise ({n_mauvais} groupe(s))"):
        st.markdown( f"""
        **Soutien intensif avant les épreuves**:
        Mettre en place des **heures de soutien supplémentaires** ciblées sur les matières clés de la série concernée.
        
        **Examens blancs**:
        Organiser des **épreuves blanches** pour familiariser les candidats avec les conditions d'examen et identifier les lacunes en amont.
        
        **Lien avec les familles**:
        Organiser des réunions d'information pour impliquer les familles et coordonner le **suivi à domicile**.
            """)

if n_modere > 0:
    with st.expander(f"Groupes à performance modérée ({n_modere} groupe(s))"):
        st.markdown(f"""
        **Ateliers de méthodologie**:
        Proposer des **ateliers de travail** sur la gestion du temps, la structuration des réponses et la prise de notes efficace.
        
        **Groupes de travail collaboratif**:
        Encourager la formation de **groupes de révision** encadrés par un enseignant référent.
        
        **Suivi individualisé**:
        Identifier les élèves proches du seuil et leur proposer un **plan de progression personnalisé**.
            
        """)

