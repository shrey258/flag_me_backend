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
model = genai.GenerativeModel('gemini-pro')

class GiftRecommender:
    @staticmethod
    def _create_prompt(person_details: Dict) -> str:
        """Create a structured prompt for Gemini based on person details"""
        logger.info(f"Creating prompt with person details: {person_details}")
        prompt = f"""
        Based on the following details about a person, suggest 5 specific gift products that would be perfect for them.
        Format each suggestion as a clear product name that can be searched on e-commerce platforms.
        
        Person Details:
        - Age: {person_details.get('age', 'Not specified')}
        - Gender: {person_details.get('gender', 'Not specified')}
        - Interests: {', '.join(person_details.get('interests', []))}
        - Occasion: {person_details.get('occasion', 'Not specified')}
        - Budget Range: {person_details.get('budget', 'Not specified')}
        - Relationship: {person_details.get('relationship', 'Not specified')}
        
        Additional Notes: {person_details.get('additional_notes', '')}
        
        Please provide 5 specific product suggestions that are:
        1. Readily available on e-commerce platforms
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
                # Remove numbering and common prefixes
                if line and any(c.isdigit() for c in line[:2]):  # Check if line starts with a number
                    # Remove the number and dot/period
                    cleaned_line = line.split('.', 1)[1].strip()
                    # Remove quotes if present
                    cleaned_line = cleaned_line.strip('"')
                    if cleaned_line:
                        suggestions.append(cleaned_line)
            
            logger.info(f"Extracted suggestions: {suggestions}")
            return suggestions[:5]
            
        except Exception as e:
            logger.error(f"Error in get_gift_suggestions: {str(e)}", exc_info=True)
            raise
