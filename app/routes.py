from fastapi import APIRouter, HTTPException, Request
from app.gift_recommender import GiftRecommender
from app.message_generator import MessageGenerator
from app.schemas import (
    ProductSearchRequest,
    ProductSearchResponse,
    GiftRecommendationRequest,
    GiftRecommendationResponse,
    MessageGenerationRequest,
    MessageGenerationResponse
)
from app.ecommerce import EcommerceSearcher
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
ecommerce_searcher = EcommerceSearcher()
gift_recommender = GiftRecommender()
message_generator = MessageGenerator()

@router.post('/gift-suggestions', response_model=GiftRecommendationResponse)
async def get_gift_suggestions(request: GiftRecommendationRequest):
    """
    Get personalized gift suggestions using Gemini AI based on person details
    """
    try:
        logger.info(f"Received gift suggestion request: {request.person_details}")
        
        # Get gift suggestions from Gemini
        suggestions = await gift_recommender.get_gift_suggestions(request.person_details.dict())
        
        if not suggestions:
            logger.warning("No gift suggestions received from Gemini")
            raise HTTPException(status_code=500, detail="Failed to generate gift suggestions")
            
        logger.info(f"Generated gift suggestions: {suggestions}")
        
        return {
            'gift_suggestions': suggestions,
        }
        
    except Exception as e:
        logger.error(f"Error in get_gift_suggestions: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/search-products', response_model=ProductSearchResponse)
async def search_products(request: ProductSearchRequest):
    try:
        logger.info(f"Received product search request: {request.query}")
        
        # Log price range if provided
        if request.min_price is not None or request.max_price is not None:
            logger.info(f"Price range filter: min=₹{request.min_price}, max=₹{request.max_price}")
        
        # Log platforms if provided
        if request.platforms:
            logger.info(f"Platform filter: {', '.join(request.platforms)}")
        else:
            logger.info("No platform filter specified, using all platforms")
        
        print(f"Starting search for query: '{request.query}' with platforms: {set(request.platforms) if request.platforms else None}")
        
        # Create searcher instance
        searcher = EcommerceSearcher()
        
        # Search across platforms
        products = await searcher.search_all(
            request.query,
            min_price=request.min_price,
            max_price=request.max_price,
            platforms=set(request.platforms) if request.platforms else None
        )
        
        logger.info(f"Found {len(products)} products for query: {request.query}")
        print(f"Search completed. Found {len(products)} products.")
        
        # Convert to a list of dictionaries for JSON response
        product_list = [
            {
                'title': product.title,
                'price': product.price,
                'url': product.url,
                'platform': product.platform,
                'image_url': product.image_url
            }
            for product in products
        ]
        
        return {
            'products': product_list
        }
    except Exception as e:
        logger.error(f"Error searching products: {str(e)}")
        print(f"Error in search_products: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")

@router.post('/generate-message', response_model=MessageGenerationResponse)
async def generate_message(request: MessageGenerationRequest):
    """
    Generate a personalized message using Gemini AI based on recipient details
    """
    try:
        logger.info(f"Received message generation request for {request.name} on {request.occasion}")
        
        # Generate personalized message
        message = await message_generator.generate_personalized_message(
            name=request.name,
            age=request.age,
            occasion=request.occasion,
            gender=request.gender,
            relationship=request.relationship,
            length=request.length
        )
        
        if not message:
            logger.warning("No message generated from Gemini")
            raise HTTPException(status_code=500, detail="Failed to generate message")
            
        logger.info(f"Successfully generated message for {request.name}")
        
        return {
            'message': message,
        }
        
    except Exception as e:
        logger.error(f"Error in generate_message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
