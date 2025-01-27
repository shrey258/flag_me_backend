from typing import List, Dict

def get_recommendations(user_preferences: Dict) -> List[str]:
    """
    Generate search queries based on user preferences
    """
    recommendations = []
    
    # Extract interests and preferences
    interests = user_preferences.get('interests', [])
    price_range = user_preferences.get('price_range', 'medium')
    
    # Map price ranges to search terms
    price_terms = {
        'low': 'budget',
        'medium': 'best value',
        'high': 'premium'
    }
    
    # Generate search queries based on interests
    for interest in interests:
        price_term = price_terms.get(price_range, '')
        if price_term:
            recommendations.append(f"{price_term} {interest} products")
        recommendations.append(f"best {interest} products")
    
    return recommendations[:3]  # Return top 3 search queries
