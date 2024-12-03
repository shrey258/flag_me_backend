from pydantic import BaseModel
from typing import List

class RecommendationRequest(BaseModel):
    relationship: str
    preferences: List[str]
    budget: int

class RecommendationResponse(BaseModel):
    recommendations: List[str]
