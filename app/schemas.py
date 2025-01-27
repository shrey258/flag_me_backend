from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    user_preferences: dict

class ProductResult(BaseModel):
    title: str
    price: float
    url: str
    platform: str
    image_url: Optional[str] = None

class RecommendationResponse(BaseModel):
    recommendations: List[str]
    products: Optional[List[ProductResult]] = None

class ProductSearchRequest(BaseModel):
    query: str

class ProductSearchResponse(BaseModel):
    products: List[ProductResult]
