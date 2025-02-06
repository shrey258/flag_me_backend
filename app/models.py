from typing import List, Dict, Tuple
from .gift_recommender import GiftRecommender

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

async def get_gift_recommendations(person_details: Dict) -> Tuple[List[str], List[str]]:
    """
    Generate gift recommendations using Gemini and convert them to search queries
    """
    # Get gift suggestions from Gemini
    recommender = GiftRecommender()
    gift_suggestions = await recommender.get_gift_suggestions(person_details)
    
    # Convert gift suggestions to search queries
    search_queries = []
    budget = person_details.get('budget', 'medium').lower()
    
    for suggestion in gift_suggestions:
        # Add budget qualifier to search
        if budget == 'low':
            search_queries.append(f"budget {suggestion}")
        elif budget == 'high':
            search_queries.append(f"premium {suggestion}")
        else:
            search_queries.append(f"best {suggestion}")
    
    return gift_suggestions, search_queries
