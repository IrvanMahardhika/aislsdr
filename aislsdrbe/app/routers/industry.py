from fastapi import APIRouter
from typing import List

router = APIRouter(prefix="/industry", tags=["industry"])

@router.get("/options", response_model=List[str])
def get_industry_options():
    """
    Get a list of available industry options.
    """
    return [
        "Technology & Artificial Intelligence (AI)",
        "Healthcare & Pharmaceuticals",
        "Renewable Energy",
        "Financial Services & FinTech",
        "Manufacturing",
        "E-commerce & Retail",
        "Logistics & Transportation",
        "Hospitality & Tourism",
        "Education & E-Learning",
        "Telecommunications"
    ]