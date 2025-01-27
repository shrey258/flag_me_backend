from fastapi import APIRouter, HTTPException
from app.models import get_recommendations
from app.schemas import RecommendationRequest, RecommendationResponse, ProductSearchRequest, ProductSearchResponse
from app.ecommerce import EcommerceSearcher

router = APIRouter()
ecommerce_searcher = EcommerceSearcher()

@router.post('/recommendations', response_model=RecommendationResponse)
async def recommend_gifts(request: RecommendationRequest):
    try:
        # Get search queries based on user preferences
        search_queries = get_recommendations(request.user_preferences)
        
        # Search for products using the generated queries
        all_products = []
        for query in search_queries:
            products = await ecommerce_searcher.search_all(query)
            all_products.extend(products)
        
        # Sort and deduplicate products
        unique_products = {}
        for product in all_products:
            if product.title not in unique_products:
                unique_products[product.title] = product
        
        # Get top 10 products sorted by rating and price
        top_products = sorted(
            unique_products.values(),
            key=lambda x: (-x.rating if x.rating else 0, x.price if x.price else float('inf'))
        )[:10]
        
        return {
            'recommendations': search_queries,
            'products': [
                {
                    'title': p.title,
                    'price': p.price,
                    'url': p.url,
                    'platform': p.platform,
                    'image_url': p.image_url
                } for p in top_products
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/search-products', response_model=ProductSearchResponse)
async def search_products(request: ProductSearchRequest):
    try:
        products = await ecommerce_searcher.search_all(request.query)
        return {
            'products': [
                {
                    'title': p.title,
                    'price': p.price,
                    'url': p.url,
                    'platform': p.platform,
                    'image_url': p.image_url
                } for p in products
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
