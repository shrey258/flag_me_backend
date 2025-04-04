from pydantic import BaseModel, Field
from typing import List, Optional, Set

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
    platforms: Optional[Set[str]] = None

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
    platforms: Optional[List[str]] = None

class GiftRecommendationRequest(BaseModel):
    person_details: GiftPersonDetails

class GiftRecommendationResponse(BaseModel):
    gift_suggestions: List[str]

class MessageGenerationRequest(BaseModel):
    name: str
    age: int = Field(..., ge=1, le=120)
    occasion: str
    gender: str
    relationship: str
    length: int = Field(..., ge=10, le=500)

class MessageGenerationResponse(BaseModel):
    message: str
