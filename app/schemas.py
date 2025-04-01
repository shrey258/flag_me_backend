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
    min_price: Optional[float] = None
    max_price: Optional[float] = None

class ProductSearchResponse(BaseModel):
    products: List[ProductResult]

class GiftPersonDetails(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    interests: List[str] = []
    occasion: Optional[str] = None
    budget: Optional[str] = None
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    relationship: Optional[str] = None
    additional_notes: Optional[str] = None

class GiftRecommendationRequest(BaseModel):
    person_details: GiftPersonDetails

class GiftRecommendationResponse(BaseModel):
    gift_suggestions: List[str]
