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

# Calcul du coût d'électricité mensuel (30 jours)
electricity_cost_per_month = power_consumption * 24 * 30 * electricity_price

# Calcul du coût total de l'électricité sur 24 mois
total_electricity_cost = electricity_cost_per_month * 24

# Calcul de la quantité initiale de KAS achetée avec le prix du marché
initial_kas = market_price / kas_price

# Pourcentage d'augmentation du prix du KAS converti en multiplicateur
kas_growth_factor = 1 + (kas_monthly_increase / 100)


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

# Afficher le coût mensuel et le coût total d'électricité
st.markdown(f"Coût mensuel de l'électricité : **{electricity_cost_per_month:,.2f} $ /mois**")
st.markdown(f"Marge de l'électricité sur 24 mois : **{total_electricity_cost:,.2f} $**")

# Calcul : Production totale sur 24 mois en fonction du prix du KAS
optimal_sale_price = total_rewards * kas_price

# Afficher le prix de vente optimal de la machine avec séparateur de milliers et en gras
st.markdown(f"Prix de vente optimal de la machine : **{optimal_sale_price:,.2f} $**")

# Calcul du Delta prix de vente - bénéfice
delta_profit = optimal_sale_price - total_electricity_cost

# Afficher le Delta prix de vente - bénéfice avec couleur (vert si positif, rouge si négatif)
if delta_profit >= 0:
    st.markdown(f"<span style='color:green'>Delta prix de vente optimal - bénéfice : **{delta_profit:,.2f} $**</span>", unsafe_allow_html=True)
else:
    st.markdown(f"<span style='color:red'>Delta prix de vente optimal - bénéfice : **{delta_profit:,.2f} $**</span>", unsafe_allow_html=True)


def calculate_months(kas_amount, electricity_cost, kas_growth_factor, percentage_conserved, max_months=24, min_kas_threshold=0.01):
    """
    Calcule le nombre de mois pendant lesquels il est possible de tenir avec la quantité initiale de KAS,
    en prenant en compte l'augmentation du prix du KAS et le réinvestissement.
    """
    
    months = 0
    current_kas_price = kas_price  # Le prix du KAS évolue chaque mois
    
    # Calculer les pourcentages une seule fois pour éviter les recalculs dans la boucle
    percentage_conserved_factor = percentage_conserved / 100
    percentage_reinvested_factor = (100 - percentage_conserved) / 100

    while kas_amount > min_kas_threshold and months < max_months:
        months += 1
        
        # 1. Calculer la quantité de KAS nécessaire pour payer l'électricité
        kas_needed_for_electricity = electricity_cost * percentage_conserved_factor / current_kas_price
        kas_amount -= kas_needed_for_electricity
        
        # Vérifier si le montant restant de KAS est suffisant pour continuer
        if kas_amount <= min_kas_threshold:
            break
        
        # 2. Calculer combien de KAS est acheté avec le réinvestissement
        # Nous ajustons ici la manière dont l'achat de KAS se fait pour refléter une plus forte dégradation avec l'augmentation du prix.
        kas_bought_with_reinvested_money = (electricity_cost * percentage_reinvested_factor) / (current_kas_price * kas_growth_factor)
        kas_amount += kas_bought_with_reinvested_money
        
        # 3. Augmenter le prix du KAS pour le mois suivant
        current_kas_price *= kas_growth_factor  # Le KAS devient plus cher chaque mois

    return months
    
# Calcul du nombre de mois garantis pour chaque scénario
months_100 = calculate_months(initial_kas, electricity_cost_per_month, kas_growth_factor, 100)
months_75 = calculate_months(initial_kas, electricity_cost_per_month, kas_growth_factor, 75)

# Afficher les résultats pour les trois scénarios de conservation de la marge électrique
st.write(f"Nombre de mois garantis si marge électrique 100% conservée : {months_100} mois")
st.write(f"Nombre de mois garantis si marge électrique 75% conservée : {months_75} mois")

