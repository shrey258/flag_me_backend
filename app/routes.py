from fastapi import APIRouter, HTTPException
from app.gift_recommender import GiftRecommender
from app.schemas import (
    ProductSearchRequest,
    ProductSearchResponse,
    GiftRecommendationRequest,
    GiftRecommendationResponse
)
from app.ecommerce import EcommerceSearcher
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
ecommerce_searcher = EcommerceSearcher()
gift_recommender = GiftRecommender()

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
        
        products = await ecommerce_searcher.search_all(
            request.query,
            min_price=request.min_price,
            max_price=request.max_price
        )
        
        logger.info(f"Found {len(products)} products for query: {request.query}")
        return {
            'products': [
                {
                    'title': p.title,
                    'price': p.price,
                    'url': p.url,
                    'platform': p.platform,
                    'image_url': p.image_url
                } for p in products[:10]
            ]
        }
    except Exception as e:
        logger.error(f"Error in search_products: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
