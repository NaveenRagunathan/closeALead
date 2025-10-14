from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from core.database import get_db
from core.security import get_current_user
from models.user import User, PlanType
from models.offer import Offer
from services.pdf_service import generate_pdf

router = APIRouter()

PLAN_LIMITS = {
    PlanType.FREE: {"offers": 1, "edits": 5},
    PlanType.PROFESSIONAL: {"offers": 4, "edits": 15},
    PlanType.AGENCY: {"offers": float('inf'), "edits": float('inf')}
}

class PriceData(BaseModel):
    amount: float
    currency: str = "USD"
    interval: str = "one-time"

class OfferCreate(BaseModel):
    title: str
    subtitle: str = ""
    description: str = ""
    clientName: str = ""
    price: PriceData
    features: List[str] = []
    template: str = "modern"
    brandColors: dict = {}
    logoUrl: str = ""
    images: List[str] = []

class OfferUpdate(BaseModel):
    title: str = None
    subtitle: str = None
    description: str = None
    clientName: str = None
    price: PriceData = None
    features: List[str] = None
    template: str = None
    brandColors: dict = None
    logoUrl: str = None
    images: List[str] = None

@router.get("")
async def get_offers(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    offers = db.query(Offer).filter(Offer.user_id == user.id).all()
    return [offer.to_dict() for offer in offers]

@router.get("/{offer_id}")
async def get_offer(
    offer_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    offer = db.query(Offer).filter(
        Offer.id == offer_id,
        Offer.user_id == user.id
    ).first()
    
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    return offer.to_dict()

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_offer(
    offer_data: OfferCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check offer limit
    limits = PLAN_LIMITS[user.plan]
    current_count = db.query(Offer).filter(Offer.user_id == user.id).count()
    
    if current_count >= limits["offers"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You have reached your offer limit. Please upgrade your plan."
        )
    
    # Create offer
    offer = Offer(
        user_id=user.id,
        title=offer_data.title,
        subtitle=offer_data.subtitle,
        description=offer_data.description,
        client_name=offer_data.clientName,
        price_amount=offer_data.price.amount,
        price_currency=offer_data.price.currency,
        price_interval=offer_data.price.interval,
        features=offer_data.features,
        template=offer_data.template,
        brand_colors=offer_data.brandColors,
        logo_url=offer_data.logoUrl,
        images=offer_data.images,
        edit_limit=limits["edits"]
    )
    
    db.add(offer)
    db.commit()
    db.refresh(offer)
    
    return offer.to_dict()

@router.put("/{offer_id}")
async def update_offer(
    offer_id: str,
    offer_data: OfferUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    offer = db.query(Offer).filter(
        Offer.id == offer_id,
        Offer.user_id == user.id
    ).first()
    
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    # Check edit limit
    if offer.edit_count >= offer.edit_limit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have reached your edit limit for this offer"
        )
    
    # Update fields
    update_data = offer_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "price" and value:
            offer.price_amount = value.amount
            offer.price_currency = value.currency
            offer.price_interval = value.interval
        elif field == "brandColors":
            offer.brand_colors = value
        elif field == "logoUrl":
            offer.logo_url = value
        elif field == "clientName":
            offer.client_name = value
        else:
            setattr(offer, field, value)
    
    # Increment edit count
    offer.edit_count += 1
    
    db.commit()
    db.refresh(offer)
    
    return offer.to_dict()

@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offer(
    offer_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    offer = db.query(Offer).filter(
        Offer.id == offer_id,
        Offer.user_id == user.id
    ).first()
    
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    db.delete(offer)
    db.commit()
    
    return None

@router.post("/{offer_id}/export")
async def export_offer_pdf(
    offer_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    offer = db.query(Offer).filter(
        Offer.id == offer_id,
        Offer.user_id == user.id
    ).first()
    
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    # Generate PDF
    pdf_content = generate_pdf(offer)
    
    from fastapi.responses import Response
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{offer.title}.pdf"'
        }
    )
