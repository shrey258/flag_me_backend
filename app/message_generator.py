import google.generativeai as genai
import logging
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

class MessageGenerator:
    """Class for generating personalized messages using Gemini AI"""
    
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-flash")
    
    def refine_human_like_text(self, text, age, relationship):
        """
        Post-process AI-generated text to make it more human-like.
        If the recipient is young (<=28) and in a personal relationship, add casual slang.
        """
        text = text.replace("We", "I").replace("One", "You")
        text = text.replace("It is a pleasure", "I'm really happy").replace("Best wishes", "Wishing you all the best")
        text = text.replace("I hope this message finds you well", "I just wanted to say")
        
        # Apply slang only if recipient is young and in a personal relationship
        if age <= 28 and relationship.lower() in ["lover", "friend", "best friend"]:
            slang_dict = {
                "you": "u",
                "your": "ur",
                "because": "cuz",
                "great": "lit",
                "amazing": "fire",
                "funny": "LOL",
                "bro": "bruh",
                "talk to you later": "TTYL",
                "to be honest": "TBH",
                "oh my god": "OMG",
                "see you later": "cya",
                "birthday": "bday"
            }
            for word, slang in slang_dict.items():
                text = text.replace(f" {word} ", f" {slang} ")
                
        return text
    
    async def generate_personalized_message(self, name, age, occasion, gender, relationship, length):
        """
        Generates a personalized message using Gemini AI with improved human-like text.
        """
        try:
            logger.info(f"Generating message for {name} on {occasion}")
            
            prompt = f"""
            Write a heartfelt, natural, and warm message for {name} on {occasion}.
            - Keep it friendly, engaging, and natural, as if written by a close friend or family member.
            - Make sure it does not sound robotic or overly formal.
            - Gender: {gender}, Relationship: {relationship}, Age: {age}.
            - Length: {length} words.
            """
            
            response = await self.model.generate_content_async(prompt)
            
            if not response or not response.text:
                logger.error("Empty response from Gemini AI")
                return "Sorry, I couldn't generate a message at this time."
                
            refined_message = self.refine_human_like_text(response.text.strip(), age, relationship)
            logger.info(f"Successfully generated message for {name}")
            
            return refined_message
            
        except Exception as e:
            logger.error(f"Error generating message: {str(e)}", exc_info=True)
            return f"Error generating message: {str(e)}"
