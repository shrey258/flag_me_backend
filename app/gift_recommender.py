import os
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

class GiftRecommender:
    @staticmethod
    def _create_prompt(person_details: Dict) -> str:
        """Create a structured prompt for Gemini based on person details"""
        # Based on the following details about a person, suggest 5 gift products that would be perfect to gift them.
        # The gift product should be available on e-commerce websites and the title shouldn't be longer than 2-3 words for display.
        # Dont give brand names along with the product name.
        #  Based on the following details about a person, suggest 5 specific gift products that would be perfect for them.
        # Format each suggestion as a clear product name that can be searched on e-commerce platforms.
        # The name of these products should make sense based on user preferences and occasion. It should not be too long for a title of product.
        logger.info(f"Creating prompt with person details: {person_details}")
        
        # Determine budget information to include in the prompt
        budget_info = person_details.get('budget', 'Not specified')
        if person_details.get('min_budget') is not None and person_details.get('max_budget') is not None:
            budget_info = f"₹{person_details.get('min_budget')} - ₹{person_details.get('max_budget')}"
        
        # Get platforms from person details or use default (all platforms)
        platforms = person_details.get('platforms')
        if platforms is None:
            platforms = ['Amazon', 'Flipkart', 'Myntra']
        elif not isinstance(platforms, list):
            platforms = [platforms]
        platforms_str = ', '.join(platforms)
        
        prompt = f"""
Suggest 5 **highly specific and relevant** gift products for the person described below.
The product names should be concise but **specific enough to identify the item** (e.g., 'Sony Noise Cancelling Headphones', 'Fitbit Charge 5', 'JBL Flip 6 Speaker'). 
Include **brand names or specific models** where appropriate to enhance clarity and searchability on Indian e-commerce sites.

**Critically consider all the following details** to ensure the suggestions are truly suitable:

Person Details:
- Age: {person_details.get('age', 'Not specified')}
- Gender: {person_details.get('gender', 'Not specified')}
- Interests: {', '.join(person_details.get('interests', ['None specified']))}
- Occasion: {person_details.get('occasion', 'Not specified')}
- Budget Range: {budget_info}
- Relationship: {person_details.get('relationship', 'Not specified')}
- Platforms: {platforms_str}
Additional Notes: {person_details.get('additional_notes', 'None')}

**Requirements for the 5 suggestions:**
1. **Specificity:** Avoid generic categories. Suggest actual, identifiable products. Include brand/model if helpful (e.g., 'Bose QuietComfort Earbuds II' instead of just 'Earbuds').
2. **Availability:** Should be readily findable on platforms like {platforms_str}.
3. **Budget:** Must align with the budget range: {budget_info}.
4. **Relevance:** Deeply consider the person's interests, age, occasion, and relationship.

**Format:** Output ONLY a simple list of the 5 product names, one per line. No other text.
"""
        return prompt

    async def get_gift_suggestions(self, person_details: Dict) -> List[str]:
        """Get gift suggestions from Gemini based on person details"""
        try:
            logger.info("Starting gift suggestion generation")
            prompt = self._create_prompt(person_details)
            logger.info(f"Generated prompt: {prompt}")
            
            response = await model.generate_content_async(prompt)
            logger.info(f"Received response from Gemini: {response.text}")
            
            # Extract product suggestions from the response
            suggestions = []
            for line in response.text.split('\n'):
                line = line.strip()
                # Remove bullet points, asterisks, or numbering
                if line:
                    # Remove bullet points or asterisks
                    if line.startswith('*'):
                        cleaned_line = line.lstrip('* ').strip()
                        suggestions.append(cleaned_line)
                    # Handle numbered items
                    elif any(c.isdigit() for c in line[:2]):
                        cleaned_line = line.split('.', 1)[1].strip() if '.' in line else line
                        suggestions.append(cleaned_line)
                    # Handle plain text items
                    elif len(suggestions) < 5 and len(line) > 3 and not line.startswith('-'):
                        suggestions.append(line)
                
            logger.info(f"Extracted suggestions: {suggestions}")
            return suggestions[:5]
            
        except Exception as e:
            logger.error(f"Error in get_gift_suggestions: {str(e)}", exc_info=True)
            raise
