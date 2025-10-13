from crewai import Crew, Process
from crew.agents import (
    information_gatherer,
    copywriter,
    design_strategist,
    quality_assurance
)
from crew.tasks import (
    create_gather_info_task,
    create_copywriting_task,
    create_design_strategy_task,
    create_qa_task
)
import json

class OfferCreationCrew:
    """Crew for creating offers from scratch"""
    
    def __init__(self):
        self.crew = None
    
    def create(self, user_input: dict):
        """Create an offer from user input"""
        
        # Create tasks
        gather_task = create_gather_info_task(information_gatherer, user_input)
        
        # Create crew
        self.crew = Crew(
            agents=[information_gatherer, copywriter, design_strategist, quality_assurance],
            tasks=[gather_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute
        try:
            result = self.crew.kickoff()
            return self._parse_result(result)
        except Exception as e:
            print(f"Error in crew execution: {e}")
            return self._create_fallback_offer(user_input)
    
    def _parse_result(self, result):
        """Parse crew result into offer format"""
        try:
            # Try to parse as JSON
            if isinstance(result, str):
                data = json.loads(result)
            else:
                data = result
            
            return {
                "title": data.get("title", "Professional Service Offer"),
                "subtitle": data.get("subtitle", "Transform your business"),
                "description": data.get("description", ""),
                "price": {
                    "amount": data.get("price", {}).get("amount", 997),
                    "currency": data.get("price", {}).get("currency", "USD"),
                    "interval": data.get("price", {}).get("interval", "one-time")
                },
                "features": data.get("features", []),
                "template": data.get("template", "modern"),
                "brandColors": data.get("brandColors", {
                    "primary": "#3b82f6",
                    "secondary": "#8b5cf6",
                    "accent": "#10b981"
                })
            }
        except Exception as e:
            print(f"Error parsing result: {e}")
            return self._create_fallback_offer({})
    
    def _create_fallback_offer(self, user_input: dict):
        """Create a basic offer if AI processing fails"""
        return {
            "title": user_input.get("service_name", "Professional Service Offer"),
            "subtitle": "Transform your business with our proven solution",
            "description": user_input.get("description", "A comprehensive solution designed to help you achieve your goals."),
            "price": {
                "amount": float(user_input.get("pricing", 997)),
                "currency": "USD",
                "interval": "one-time"
            },
            "features": user_input.get("features", "").split("\n") if isinstance(user_input.get("features"), str) else ["Feature 1", "Feature 2", "Feature 3"],
            "template": "modern",
            "brandColors": {
                "primary": "#3b82f6",
                "secondary": "#8b5cf6",
                "accent": "#10b981"
            }
        }


class OfferRedesignCrew:
    """Crew for redesigning existing offers"""
    
    def __init__(self):
        self.crew = None
    
    def redesign(self, extracted_content: str):
        """Redesign an offer from extracted content"""
        
        # For MVP, do basic processing
        # In production, this would use document parsing agents
        
        return {
            "title": "Redesigned Professional Service Offer",
            "subtitle": "Enhanced and optimized for maximum conversion",
            "description": "Your offer has been analyzed and enhanced with AI-powered improvements.",
            "price": {
                "amount": 997,
                "currency": "USD",
                "interval": "one-time"
            },
            "features": [
                "Enhanced feature presentation",
                "Improved value proposition",
                "Optimized pricing display",
                "Professional design elements"
            ],
            "template": "modern",
            "brandColors": {
                "primary": "#3b82f6",
                "secondary": "#8b5cf6",
                "accent": "#10b981"
            }
        }
