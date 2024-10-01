import streamlit as st
import pandas as pd
from datetime import datetime

# Titre de l'application
st.title("MinerTrack")

# Champs de saisie pour les paramètres
machine_power = st.number_input(
    "Puissance de votre machine (en TH/s)",
    value=21.0,
    step=1.0,
    format="%.2f"
)

# Entrée pour la croissance mensuelle du réseau en PH/s
network_growth_per_month_phs = st.number_input(
    "Croissance mensuelle du réseau (en PH/s)",
    value=100.0,  # Valeur par défaut 100 PH/s
    step=1.0,
    format="%.2f"
)

# Conversion de PH/s en TH/s pour les calculs
network_growth_per_month = network_growth_per_month_phs * 1e3  # 1 PH/s = 1000 TH/s

# Nouveau : Champs pour la consommation électrique et le prix de l'électricité
power_consumption = st.number_input(
    "Consommation électrique de la machine (en kW/h)",
    value=3.5,  # Valeur par défaut
    step=0.1,
    format="%.2f"
)

electricity_price = st.number_input(
    "Prix de l'électricité (en $/kW)",
    value=0.05,  # Valeur par défaut
    step=0.01,
    format="%.2f"
)

# Nouveau : Prix du KAS
kas_price = st.number_input(
    "Prix du KAS (en $)",
    value=0.16,  # Valeur de référence
    step=0.01,
    format="%.2f"
)

# Nouveau : Date de branchement
connection_date = st.date_input(
    "Date de branchement de la machine",
    value=datetime.now()
)

# Obtenir le mois de branchement
start_month = (connection_date.year - 2024) * 12 + (connection_date.month - 10) + 36  # Ajuster si nécessaire

# Liste complète des données d'émission de KAS
data = {
    "Month": list(range(36, 87)),
    "Total KAS Emitted": [
        216713637, 204550435, 193069902, 182233721, 172005728, 162351788, 153239683, 144639000,
        136521037, 128858700, 121626417, 114800050, 108356819, 102275218, 96534951, 91116860,
        86002864, 81175894, 76619841, 72319500, 68260518, 64429350, 60813208, 57140025,
        54178409, 51137609, 48267475, 45558430, 43001432, 40587947, 38309921, 36159750,
        34130259, 32214675, 30406604, 28700013, 27089205, 25568804, 24133738, 22779215,
        21500716, 20293974, 19154960, 18079875, 17065130, 16107337, 15203302, 14350006,
        13544602, 12784402, 12066869
    ],
}

# Créer un DataFrame pour les données d'émission et filtrer à partir de la date de branchement
df = pd.DataFrame(data)
df_filtered = df[df["Month"] >= start_month].head(24)  # Sélectionner les 24 mois suivants

# Initialiser les paramètres
initial_network_power = st.number_input(
    "Puissance initiale du réseau (en TH/s)",
    value=1.1e6,  # 1.1 EH/s en TH/s
    step=1e5,
    format="%.0f"
)

# Calcul du coût d'électricité mensuel (30 jours)
electricity_cost_per_month = power_consumption * 24 * 30 * electricity_price

# Afficher le coût mensuel d'électricité avec séparateur de milliers et en gras
st.markdown(f"**Coût mensuel de l'électricité : {electricity_cost_per_month:,.2f} $ /mois**")

# Calcul de la marge de l'électricité sur 24 mois
electricity_margin = electricity_cost_per_month * 24

# Calcul des récompenses pour les 24 mois à venir
rewards = []

for idx, row in enumerate(df_filtered.itertuples(), start=0):
    month = row.Month
    total_kas = row.Total_KAS_Emitted

    # Calcul de la puissance totale du réseau pour ce mois
    network_power = initial_network_power + idx * network_growth_per_month

    # Calcul de la part de la puissance de la machine sur le réseau
    machine_share = machine_power / network_power

    # Calcul de la récompense en KAS pour ce mois
    reward = machine_share * total_kas

    # Ajouter le résultat à la liste
    rewards.append({
        "Mois": idx + 1,
        "Month": month,
        "Puissance du réseau (TH/s)": network_power,
        "Total KAS émis": total_kas,
        "Part de la machine": machine_share,
        "Récompense (KAS)": reward
    })

# Créer un DataFrame pour afficher les résultats
result_df = pd.DataFrame(rewards)

# Afficher les résultats
st.write("Récompenses projetées sur 24 mois")
st.dataframe(result_df)

# Calculer la somme des récompenses sur 24 mois
total_rewards = result_df['Récompense (KAS)'].sum()

# Afficher la somme totale des récompenses avec séparateur de milliers et en gras
st.markdown(f"**Somme totale des récompenses sur 24 mois : {total_rewards:,.2f} KAS**")

# Calcul : Production totale sur 24 mois en fonction du prix du KAS
optimal_sale_price = total_rewards * kas_price

# Afficher le prix de vente optimal de la machine avec séparateur de milliers et en gras
st.markdown(f"**Prix de vente optimal de la machine : {optimal_sale_price:,.2f} $**")

# Afficher la marge de l'électricité sur 24 mois
st.markdown(f"**Marge de l'électricité sur 24 mois : {electricity_margin:,.2f} $**")

# Calcul du delta prix de vente - bénéfice
delta = optimal_sale_price - electricity_margin

# Afficher le delta avec couleur selon le signe
if delta >= 0:
    st.markdown(f"**Delta prix de vente - bénéfice : <span style='color:green'>{delta:,.2f} $</span>**", unsafe_allow_html=True)
else:
    st.markdown(f"**Delta prix de vente - bénéfice : <span style='color:red'>{delta:,.2f} $</span>**", unsafe_allow_html=True)
