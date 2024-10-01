import streamlit as st
import pandas as pd
from datetime import datetime

# Titre de l'application
st.title("MinerTrack")

# Obtenir la date actuelle
current_date = datetime.now()
current_month = (current_date.year - 2024) * 12 + (current_date.month - 10) + 36  # Calculer le mois correspondant

# Liste complète des données d'émission de KAS
data = {
    "Month": list(range(36, 87)),
    "Total KAS Emitted": [216713637, 204550435, 193069902, 182233721, 172005728, 162351788, 153239683, 144639000,
                          136521037, 128858700, 121626417, 114800050, 108356819, 102275218, 96534951, 91116860,
                          86002864, 81175894, 76619841, 72319500, 68260518, 64429350, 60813208, 57140025,
                          54178409, 51137609, 48267475, 45558430, 43001432, 40587947, 38309921, 36159750,
                          34130259, 32214675, 30406604, 28700013, 27089205, 25568804, 24133738, 22779215,
                          21500716, 20293974, 19154960, 18079875, 17065130, 16107337, 15203302, 14350006,
                          13544602, 12784402, 12066869],
}

# Créer un DataFrame pour les données d'émission et filtrer à partir du mois courant
df = pd.DataFrame(data)
df_filtered = df[df["Month"] >= current_month].head(24)  # Sélectionner les 24 prochains mois

# Champs de saisie pour les paramètres
initial_network_power = st.number_input(
    "Puissance initiale du réseau (en TH/s)", 
    value=1.1e6,  # 1.1 EH/s en TH/s
    step=1e5, 
    format="%.0f"
)

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

# Calcul du coût d'électricité mensuel (30 jours)
electricity_cost_per_month = power_consumption * 24 * 30 * electricity_price

# Afficher le coût mensuel d'électricité avec séparateur de milliers et en gras
st.markdown(f"**Coût mensuel de l'électricité : {electricity_cost_per_month:,.2f} $ /mois**")

# Calcul des récompenses pour les 24 prochains mois
rewards = []

for i, row in df_filtered.iterrows():
    month = row['Month']
    total_kas = row['Total KAS Emitted']
    
    # Calcul de la puissance totale du réseau pour ce mois
    network_power = initial_network_power + i * network_growth_per_month
    
    # Calcul de la part de la puissance de la machine sur le réseau
    machine_share = machine_power / network_power
    
    # Calcul de la récompense en KAS pour ce mois
    reward = machine_share * total_kas
    
    # Ajouter le résultat à la liste
    rewards.append({
        "Month": month,
        "Network Power (TH/s)": network_power,
        "Total KAS Emitted": total_kas,
        "Machine Share": machine_share,
        "Reward (KAS)": reward
    })

# Créer un DataFrame pour afficher les résultats
result_df = pd.DataFrame(rewards)

# Afficher les résultats
st.write("Récompenses projetées sur 24 mois")
st.dataframe(result_df)

# Calculer la somme des récompenses sur 24 mois
total_rewards = result_df['Reward (KAS)'].sum()
# Afficher la somme totale des récompenses avec séparateur de milliers et en gras
st.markdown(f"Somme totale des récompenses sur 24 mois : **{total_rewards:,.2f} KAS**")

# Afficher le coût mensuel d'électricité avec séparateur de milliers et en gras
st.markdown(f"Coût mensuel de l'électricité : **{electricity_cost_per_month:,.2f} $ /mois**")

# Calcul : Production totale sur 24 mois en fonction du prix du KAS
optimal_sale_price = total_rewards * kas_price

# Afficher le prix de vente optimal de la machine avec séparateur de milliers et en gras
st.markdown(f"Prix de vente optimal de la machine : **{optimal_sale_price:,.2f} $**")
