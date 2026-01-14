def calculate_risk_score(amount, probability, country, velocity):
    """Calculate comprehensive risk score"""
    risk = probability
    
    # Amount multiplier
    if amount > 10000:
        risk *= 1.3
    elif amount > 5000:
        risk *= 1.15
    
    # Country risk
    high_risk_countries = ['RU', 'CN', 'NG', 'VE']
    if country in high_risk_countries:
        risk *= 1.25
    
    # Velocity multiplier
    if velocity == 'High':
        risk *= 1.2
    elif velocity == 'Extreme':
        risk *= 1.4
    
    return min(risk, 1.0)
