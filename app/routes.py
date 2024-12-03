from fastapi import APIRouter
from app.models import get_recommendations
from app.schemas import RecommendationRequest, RecommendationResponse

router = APIRouter()

@router.post('/recommendations', response_model=RecommendationResponse)
async def recommend_gifts(request: RecommendationRequest):
    try:
        recommendations = get_recommendations(request.dict())
        return {'recommendations': recommendations}
    except Exception as e:
        return {'error': str(e)}
