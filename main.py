import streamlit as st
import pandas as pd
from datetime import datetime

# Titre de l'application
st.title("MinerTrack")

# Obtenir la date actuelle
today = datetime.now()

# Champ pour la date de branchement (avec la date d'aujourd'hui comme valeur par défaut)
start_date = st.date_input("Date de branchement", today)

# Calculer le mois à partir de la date de branchement
months_passed = (start_date.year - 2024) * 12 + (start_date.month - 10) + 36

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

# Créer un DataFrame pour les données d'émission et filtrer à partir de la date de branchement
df = pd.DataFrame(data)
df_filtered = df[df["Month"] >= months_passed].head(24)  # Sélectionner les 24 mois à partir de la date de branchement

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

market_price = st.number_input(
    "Prix actuel du marché (en $)", 
    value=2000, 
    step=100
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

kas_monthly_increase = st.number_input("Pourcentage d'augmentation mensuel du KAS (en %)", value=2.0, step=0.1, format="%.2f")

# Calculer le coût d'électricité mensuel
electricity_cost_per_month = power_consumption * 24 * 30 * electricity_price  # 24 heures/jour, 30 jours/mois

# Calculer le nombre de KAS pouvant être acheté avec le prix actuel du marché
initial_kas_amount = market_price / kas_price  # $2000 ÷ prix du KAS

# Conversion du pourcentage d'augmentation du KAS en un facteur multiplicatif
kas_growth_factor = 1 + (kas_monthly_increase / 100)

# Calcul des récompenses pour les 24 prochains mois (précises par mois)
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
    
    # Ajouter uniquement la valeur des rewards à la liste
    rewards.append(reward)

# Créer un DataFrame avec les valeurs des rewards uniquement
result_df = pd.DataFrame({
    "Month": df_filtered["Month"],
    "Reward (KAS)": rewards  # Utilisation directe des rewards en float
})

# Afficher les résultats
st.write("Récompenses projetées sur 24 mois")
st.dataframe(result_df)

# Calculer la somme des récompenses sur 24 mois (cela devrait fonctionner maintenant)
total_rewards = result_df['Reward (KAS)'].sum()

# Afficher la somme totale des récompenses avec séparateur de milliers et en gras
st.markdown(f"Somme totale des récompenses sur 24 mois : **{total_rewards:,.2f} KAS**")

# Fonction de calcul sans réinvestissement (en utilisant les rewards précises)
def calculate_months_no_reinvestment(kas_amount, rewards, max_months=24, min_kas_threshold=0.01):
    months = 0
    for reward in rewards:  # 'reward' est directement une valeur float
        if kas_amount <= min_kas_threshold or months >= max_months:
            break
        kas_amount -= reward  # Déduire directement la valeur de reward (en KAS)
        months += 1
    return months

# Fonction de calcul avec réinvestissement (en utilisant les rewards précises)
def calculate_months_with_reinvestment(kas_amount, rewards, electricity_cost, kas_growth_factor, kas_price, reinvest_percentage=0.5, max_months=24, min_kas_threshold=0.01):
    months = 0
    current_kas_price = kas_price  # Prix initial du KAS
    for reward in rewards:  # 'reward' est directement une valeur float
        if kas_amount <= min_kas_threshold or months >= max_months:
            break
        
        # Réinvestir 50% du coût de l'électricité pour acheter du KAS
        kas_bought_with_reinvestment = (electricity_cost * reinvest_percentage) / current_kas_price
        kas_amount += kas_bought_with_reinvestment
        
        # Déduire directement la valeur de reward (en KAS)
        kas_amount -= reward
        
        # Augmenter le prix du KAS pour le mois suivant
        current_kas_price *= kas_growth_factor
        
        months += 1
    
    return months

# Calcul sans réinvestissement
months_no_reinvestment = calculate_months_no_reinvestment(initial_kas_amount, rewards)

# Calcul avec réinvestissement
months_with_reinvestment = calculate_months_with_reinvestment(initial_kas_amount, rewards, electricity_cost_per_month, kas_growth_factor, kas_price)

# Affichage des résultats
st.write(f"Nombre de mois garantis sans réinvestissement : {months_no_reinvestment} mois")
st.write(f"Nombre de mois garantis avec réinvestissement de 50% du coût d'électricité : {months_with_reinvestment} mois")
