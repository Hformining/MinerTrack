import streamlit as st
import pandas as pd

# Titre de l'application
st.title("MinerTrack")

# Champs de saisie pour les paramètres
initial_network_power = st.number_input("Puissance initiale du réseau (en TH/s)", value=1.1e6, step=1e5, format="%.0f")
machine_power = st.number_input("Puissance de votre machine (en TH/s)", value=21, step=1.0, format="%.0f")
network_growth_per_month = st.number_input("Croissance mensuelle du réseau (en TH/s)", value=100e3, step=1e3, format="%.0f")

# Données d'émission de KAS par mois
data = {
    "Month": [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
    "Total KAS Emitted": [216713637, 204550435, 193069902, 182233721, 172005728, 162351788, 153239683, 144639000, 
                          136521037, 128858700, 121626417, 114800050, 108356819, 102275218, 96534951, 91116860, 
                          86002864, 81175894, 76619841, 72319500, 68260518, 64429350, 60813208, 57140025]
}

# Créer un DataFrame pour les données d'émission
df = pd.DataFrame(data)

# Calcul des récompenses pour les 24 prochains mois
rewards = []

for i, row in df.iterrows():
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
st.write(f"Somme totale des récompenses sur 24 mois : {total_rewards:.2f} KAS")

