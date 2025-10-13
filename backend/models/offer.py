from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from core.database import Base

class Offer(Base):
    __tablename__ = "offers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Content
    title = Column(String(200), nullable=False)
    subtitle = Column(String(300))
    description = Column(String)
    
    # Pricing
    price_amount = Column(Float, default=0.0)
    price_currency = Column(String(3), default="USD")
    price_interval = Column(String(20), default="one-time")
    
    # Features and design
    features = Column(JSON, default=list)
    template = Column(String(50), default="modern")
    brand_colors = Column(JSON)
    logo_url = Column(String(500))
    images = Column(JSON, default=list)
    
    # Edit tracking
    edit_count = Column(Integer, default=0)
    edit_limit = Column(Integer, default=5)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    pdf_url = Column(String(500))

    # Relationships
    user = relationship("User", back_populates="offers")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "description": self.description,
            "price": {
                "amount": self.price_amount,
                "currency": self.price_currency,
                "interval": self.price_interval
            },
            "features": self.features or [],
            "template": self.template,
            "brandColors": self.brand_colors or {},
            "logoUrl": self.logo_url,
            "images": self.images or [],
            "editCount": self.edit_count,
            "editLimit": self.edit_limit,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
            "pdfUrl": self.pdf_url
        }
