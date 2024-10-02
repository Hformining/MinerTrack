import streamlit as st
import pandas as pd
from datetime import datetime

# Titre de l'application
st.title("MinerTrack")

# Obtenir la date actuelle
today = datetime.now()

# Ajouter une sidebar avec la sélection des monnaies
selected_coin = st.sidebar.selectbox(
    "Choisissez la monnaie", 
    options=["KAS", "Alephium"]
)

# Ajouter un titre à la sidebar
st.sidebar.markdown(f"Monnaie sélectionnée : **{selected_coin}**")

# Variables et paramètres par défaut pour KAS et Alephium
if selected_coin == "KAS":
    kas_price = 0.16
    power_consumption = 3.5
    electricity_price = 0.05
    kas_monthly_increase = 2.0
    initial_network_power = 1.1e6  # 1.1 EH/s en TH/s
    network_growth_per_month_phs = 100  # Croissance mensuelle du réseau en PH/s
    machine_power = 21.0  # Puissance de la machine en TH/s

elif selected_coin == "Alephium":
    machine_power = 16600  # Puissance de la machine en GH/s
    market_price = 10000  # Prix actuel du marché en $
    network_growth_per_month_phs = 6.5  # Croissance/mois du réseau en PH/s
    initial_network_power = 17090  # Hashrate actuel du réseau ALEPH en PH/s
    power_consumption = 3.5  # Conso élec de la machine en kW/h
    aleph_price = 1.65  # Prix du ALEPH en $
    daily_coin_yield_per_gh = 0.0051  # Rendement journalier en ALEPH par GH/s
    monthly_increase_aleph = 2.0  # Augmentation du ALEPH par mois

# Organiser les champs de saisie sur 3 colonnes
col1, col2, col3 = st.columns(3)

if selected_coin == "KAS":
    # Colonne 1 pour KAS
    with col1:
        start_date = st.date_input("Date de branchement", datetime.now())
        
        initial_network_power = st.number_input(
            "Puissance initiale du réseau (TH/s)", 
            value=float(initial_network_power),  # Assurez-vous que le type soit float
            step=1e5,  # Assurez-vous que le pas soit float également
            format="%.0f"
        )
        
        market_price = st.number_input(
            "Prix actuel du marché ($)", 
            value=float(2000),  # Assurez-vous que le type soit float
            step=100.0  # Assurez-vous que le type de `step` soit cohérent
        )

    # Colonne 2 pour KAS
    with col2:
        machine_power = st.number_input(
            "Puissance de la machine (TH/s)", 
            value=float(machine_power),  # Assurez-vous que le type soit float
            step=1.0,  # Assurez-vous que le type de `step` soit cohérent
            format="%.2f"
        )
        
        network_growth_per_month_phs = st.number_input(
            "Croissance/mois du réseau (PH/s)", 
            value=float(network_growth_per_month_phs),  # Assurez-vous que le type soit float
            step=1.0, 
            format="%.2f"
        )
        
        power_consumption = st.number_input(
            "Conso élec de la machine (kW/h)", 
            value=float(power_consumption),  # Assurez-vous que le type soit float
            step=0.1, 
            format="%.2f"
        )

    # Colonne 3 pour KAS
    with col3:
        electricity_price = st.number_input(
            "Prix de l'électricité (en $/kW)", 
            value=float(electricity_price),  # Assurez-vous que le type soit float
            step=0.01, 
            format="%.2f"
        )
        
        kas_price = st.number_input(
            "Prix du KAS (en $)", 
            value=float(kas_price),  # Assurez-vous que le type soit float
            step=0.01, 
            format="%.2f"
        )
        
        kas_monthly_increase = st.number_input(
            "% d'augmentation du KAS (par mois)", 
            value=float(kas_monthly_increase),  # Assurez-vous que le type soit float
            step=0.1, 
            format="%.2f"
        )

elif selected_coin == "Alephium":
    # Colonne 1 pour Alephium
    with col1:
        start_date = st.date_input("Date de branchement", datetime.now())
        
        machine_power = st.number_input(
            "Puissance de la machine (GH/s)", 
            value=float(machine_power),  # Assurez-vous que le type soit float
            step=100.0,  # Utilisez un pas en float ici aussi
            format="%.0f"
        )
        
        market_price = st.number_input(
            "Prix actuel du marché ($)", 
            value=float(market_price),  # Assurez-vous que le type soit float
            step=100.0  # Step float ici aussi
        )

    # Colonne 2 pour Alephium
    with col2:
        network_growth_per_month_phs = st.number_input(
            "Croissance/mois du réseau (PH/s)", 
            value=float(network_growth_per_month_phs),  # Assurez-vous que le type soit float
            step=0.1, 
            format="%.2f"
        )
        
        power_consumption = st.number_input(
            "Conso élec de la machine (kW/h)", 
            value=float(power_consumption),  # Assurez-vous que le type soit float
            step=0.1, 
            format="%.2f"
        )

    # Colonne 3 pour Alephium
    with col3:
        electricity_price = st.number_input(
            "Prix de l'électricité (en $/kW)", 
            value=float(electricity_price),  # Assurez-vous que le type soit float
            step=0.01, 
            format="%.2f"
        )
        
        aleph_price = st.number_input(
            "Prix du ALEPH (en $)", 
            value=float(aleph_price),  # Assurez-vous que le type soit float
            step=0.01, 
            format="%.2f"
        )
        
        monthly_increase_aleph = st.number_input(
            "% d'augmentation du ALEPH (par mois)", 
            value=float(monthly_increase_aleph),  # Assurez-vous que le type soit float
            step=0.1, 
            format="%.2f"
        )

# Conversion de PH/s en TH/s pour les calculs
if selected_coin == "KAS":
    network_growth_per_month = network_growth_per_month_phs * 1e3  # Conversion de PH/s en TH/s

# Calculer le mois à partir de la date de branchement
months_passed = (start_date.year - 2024) * 12 + (start_date.month - 10) + 36

# Calcul spécifique à Alephium (simplifié)
if selected_coin == "Alephium":
    # Calcul des récompenses mensuelles basées sur le rendement journalier
    daily_reward = machine_power * daily_coin_yield_per_gh  # ALEPH par jour
    monthly_reward = daily_reward * 30  # ALEPH par mois (environ 30 jours par mois)
    
    rewards = []
    network_power = initial_network_power  # Puissance initiale du réseau en PH/s

    for month in range(1, 25):  # 24 mois
        machine_share = machine_power / (network_power * 1e3)  # Conversion PH/s en GH/s
        reward = machine_share * monthly_reward
        rewards.append(reward)
        network_power += network_growth_per_month_phs  # Augmentation mensuelle du réseau

elif selected_coin == "KAS":
    # Liste complète des données d'émission de KAS (comme avant)
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

    df = pd.DataFrame(data)
    df_filtered = df[df["Month"] >= months_passed].head(24)  # Sélectionner les 24 mois à partir de la date de branchement

    rewards = []
    for i, row in df_filtered.iterrows():
        total_kas = row['Total KAS Emitted']
        network_power = initial_network_power + i * network_growth_per_month
        machine_share = machine_power / network_power
        reward = machine_share * total_kas
        rewards.append(reward)

# Calculs communs : coût de l'électricité, réinvestissements, etc.

electricity_cost_per_month = power_consumption * 24 * 30 * electricity_price  # 24 heures/jour, 30 jours/mois
# Calcul du coût total de l'électricité sur 24 mois
total_electricity_cost = electricity_cost_per_month * 24

# Calculer le nombre de coins (KAS ou ALEPH) pouvant être acheté avec le prix actuel du marché
if selected_coin == "KAS":
    initial_coin_amount = market_price / kas_price  # $2000 ÷ prix du KAS
    coin_growth_factor = 1 + (kas_monthly_increase / 100)
    coin_label = "KAS"
else:
    initial_coin_amount = market_price / aleph_price  # $10,000 ÷ prix du ALEPH
    coin_growth_factor = 1 + (monthly_increase_aleph / 100)
    coin_label = "ALEPH"

# Fonction de calcul sans réinvestissement
def calculate_months_no_reinvestment(coin_amount, rewards, max_months=24, min_coin_threshold=0.01):
    months = 0
    for reward in rewards:
        if coin_amount <= min_coin_threshold or months >= max_months:
            break
        coin_amount -= reward
        months += 1
    return months

# Fonction de calcul avec réinvestissement
def calculate_months_with_reinvestment(coin_amount, rewards, electricity_cost, coin_growth_factor, coin_price, reinvest_percentage=0.5, max_months=24, min_coin_threshold=0.01):
    months = 0
    current_coin_price = coin_price
    for reward in rewards:
        if coin_amount <= min_coin_threshold or months >= max_months:
            break

        # Réinvestir une partie du coût de l'électricité pour acheter plus de coins
        coins_bought_with_reinvestment = (electricity_cost * reinvest_percentage) / current_coin_price
        coin_amount += coins_bought_with_reinvestment

        # Déduire directement la récompense du mois en coins
        coin_amount -= reward

        # Augmenter le prix des coins pour le mois suivant
        current_coin_price *= coin_growth_factor

        months += 1
    return months

# Calcul sans réinvestissement
months_no_reinvestment = calculate_months_no_reinvestment(initial_coin_amount, rewards)

# Calcul avec réinvestissement de 50% du coût de l'électricité
months_with_50_percent_reinvestment = calculate_months_with_reinvestment(
    initial_coin_amount, rewards, electricity_cost_per_month, coin_growth_factor, kas_price if selected_coin == "KAS" else aleph_price
)

# Calcul avec réinvestissement de 75% du coût de l'électricité
months_with_75_percent_reinvestment = calculate_months_with_reinvestment(
    initial_coin_amount, rewards, electricity_cost_per_month, coin_growth_factor, kas_price if selected_coin == "KAS" else aleph_price, reinvest_percentage=0.75
)

# Calcul du montant total des récompenses sur 24 mois
total_rewards = sum(rewards)

# Calcul du prix de vente optimal de la machine sur 24 mois en fonction des rewards
optimal_sale_price = total_rewards * (kas_price if selected_coin == "KAS" else aleph_price)

# Calcul du Delta prix de vente - bénéfice
delta_profit = optimal_sale_price - total_electricity_cost

# Organiser les résultats en deux colonnes
col4, col5 = st.columns(2)

with col4:
    # Utiliser des metrics pour afficher les résultats
    st.metric(label="Coût mensuel de l'électricité", value=f"{electricity_cost_per_month:,.2f} $/mois")
    st.metric(label="Marge de l'électricité sur 24 mois", value=f"{total_electricity_cost:,.2f} $")
    st.metric(label=f"Prix de vente optimal de la machine (en {coin_label})", value=f"{optimal_sale_price:,.2f} $")
    
    # Delta avec une couleur conditionnelle en fonction du signe du delta
    if delta_profit >= 0:
        st.metric(label="Delta prix de vente optimal - bénéfice", value=f"{delta_profit:,.2f} $", delta="Profit", delta_color="normal")
    else:
        st.metric(label="Delta prix de vente optimal - bénéfice", value=f"{delta_profit:,.2f} $", delta="Perte", delta_color="inverse")

with col5:
    # Utiliser des metrics pour afficher les résultats sur les mois garantis
    st.metric(label="Nombre de mois garantis sans réinvestissement", value=f"{months_no_reinvestment}")
    st.metric(label="Nombre de mois garantis avec réinvestissement de 50%", value=f"{months_with_50_percent_reinvestment}")
    st.metric(label="Nombre de mois garantis avec réinvestissement de 75%", value=f"{months_with_75_percent_reinvestment}")

# Résumé des résultats
st.markdown("---")
st.write(f"Somme totale des récompenses sur 24 mois : **{total_rewards:,.2f} {coin_label}**")
