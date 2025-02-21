def calculate_co2_savings(waste_weight, co2_per_kg=0.9):
    return waste_weight * co2_per_kg

def format_date(date):
    return date.strftime("%Y-%m-%d")

def generate_reward_message(points):
    if points > 100:
        return "Congratulations! You've earned a bonus reward!"
    return "Keep going! Every point counts!"