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
        platforms = person_details.get('platforms', ['Amazon', 'Flipkart', 'Myntra'])
        platforms_str = ', '.join(platforms)
        
        prompt = f"""
        Based on the following details about a person, suggest 5 specific gift products that would be perfect for them.
        Format each suggestion as a clear product name that can be searched on e-commerce platforms.
        
        Person Details:
        - Age: {person_details.get('age', 'Not specified')}
        - Gender: {person_details.get('gender', 'Not specified')}
        - Interests: {', '.join(person_details.get('interests', []))}
        - Occasion: {person_details.get('occasion', 'Not specified')}
        - Budget Range: {budget_info}
        - Relationship: {person_details.get('relationship', 'Not specified')}
        
        Additional Notes: {person_details.get('additional_notes', '')}
        
        Please provide 5 specific product suggestions that are:
        1. Readily available on Indian e-commerce platforms ({platforms_str})
        2. Match the specified budget range
        3. Align with the person's interests and the occasion
        4. Are appropriate for the age group
        
        Format your response as a simple list of products, one per line.
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
