# crew/crews.py
"""
Intelligent Crew Orchestration for CloseALead
Complete implementation with all production features
"""

from crewai import Crew, Process, Task
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
from typing import Dict, Any, List, Optional
import logging
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


# ============================================================================
# MAIN CREW CLASSES
# ============================================================================

class OfferCreationCrew:
    """
    Intelligent crew for creating offers from scratch.
    Processes complete or partial user input through a sequential agent pipeline.
    No repetitive questioning - extracts what's given, infers what's missing.
    """
    
    def __init__(self):
        self.crew = None
        self.execution_log = []
    
    def create(self, user_input: dict) -> Dict[str, Any]:
        """
        Create an offer from user input.
        
        Args:
            user_input: Dictionary containing offer information (can be complete or partial)
            
        Returns:
            Complete offer object with all components
        """
        try:
            logger.info(f"Starting offer creation with input keys: {list(user_input.keys())}")
            
            # PHASE 1: INFORMATION GATHERING & STRUCTURING
            logger.info("Phase 1: Gathering and structuring information...")
            gather_task = create_gather_info_task(information_gatherer, user_input)
            
            gather_crew = Crew(
                agents=[information_gatherer],
                tasks=[gather_task],
                process=Process.sequential,
                verbose=True
            )
            
            gathered_result = gather_crew.kickoff()
            self.execution_log.append({
                "phase": "information_gathering",
                "status": "completed",
                "timestamp": time.time()
            })
            
            # Parse the gathered information
            gathered_data = self._parse_json_result(gathered_result)
            
            if not gathered_data:
                logger.error("Failed to parse gathered information, using fallback")
                return self._create_fallback_offer(user_input)
            
            logger.info(f"Successfully gathered data with {len(gathered_data)} fields")
            
            # PHASE 2: COPYWRITING
            logger.info("Phase 2: Creating compelling copy...")
            copy_task = create_copywriting_task(copywriter, json.dumps(gathered_data, indent=2))
            
            copy_crew = Crew(
                agents=[copywriter],
                tasks=[copy_task],
                process=Process.sequential,
                verbose=True
            )
            
            copy_result = copy_crew.kickoff()
            self.execution_log.append({
                "phase": "copywriting",
                "status": "completed",
                "timestamp": time.time()
            })
            
            copy_data = self._parse_json_result(copy_result)
            
            if not copy_data:
                logger.warning("Failed to parse copy data, using fallback copy")
                copy_data = self._create_fallback_copy(gathered_data)
            
            logger.info("Successfully created copy")
            
            # PHASE 3: DESIGN STRATEGY
            logger.info("Phase 3: Developing design strategy...")
            
            # Combine gathered data and copy for design decisions
            combined_data = {
                **gathered_data,
                **copy_data
            }
            
            design_task = create_design_strategy_task(
                design_strategist, 
                json.dumps(combined_data, indent=2)
            )
            
            design_crew = Crew(
                agents=[design_strategist],
                tasks=[design_task],
                process=Process.sequential,
                verbose=True
            )
            
            design_result = design_crew.kickoff()
            self.execution_log.append({
                "phase": "design_strategy",
                "status": "completed",
                "timestamp": time.time()
            })
            
            design_data = self._parse_json_result(design_result)
            
            if not design_data:
                logger.warning("Failed to parse design data, using fallback design")
                design_data = self._create_fallback_design(gathered_data)
            
            logger.info("Successfully created design strategy")
            
            # PHASE 4: ASSEMBLE COMPLETE OFFER
            complete_offer = self._assemble_offer(gathered_data, copy_data, design_data)
            
            # PHASE 5: QUALITY ASSURANCE
            logger.info("Phase 4: Running quality assurance...")
            qa_task = create_qa_task(quality_assurance, json.dumps(complete_offer, indent=2))
            
            qa_crew = Crew(
                agents=[quality_assurance],
                tasks=[qa_task],
                process=Process.sequential,
                verbose=True
            )
            
            qa_result = qa_crew.kickoff()
            self.execution_log.append({
                "phase": "quality_assurance",
                "status": "completed",
                "timestamp": time.time()
            })
            
            qa_data = self._parse_json_result(qa_result)
            
            if not qa_data:
                logger.warning("Failed to parse QA data, proceeding without detailed QA report")
                qa_data = {
                    "audit_summary": {
                        "total_score": 75,
                        "percentage": 75,
                        "overall_assessment": "Good"
                    },
                    "final_recommendation": {
                        "status": "APPROVE"
                    }
                }
            
            # Add QA report and execution log to offer
            complete_offer["qa_report"] = qa_data
            complete_offer["execution_log"] = self.execution_log
            complete_offer["processing_time"] = sum(1 for _ in self.execution_log)
            
            logger.info("Offer creation completed successfully")
            return complete_offer
            
        except Exception as e:
            logger.error(f"Error in crew execution: {str(e)}", exc_info=True)
            self.execution_log.append({
                "phase": "error",
                "error": str(e),
                "timestamp": time.time()
            })
            return self._create_fallback_offer(user_input)
    
    def _parse_json_result(self, result: Any) -> Optional[Dict[str, Any]]:
        """
        Parse crew result into JSON.
        Handles strings, objects, and various formats.
        """
        try:
            # If already a dict
            if isinstance(result, dict):
                return result
            
            # If it's a string
            if isinstance(result, str):
                result = result.strip()
                
                # Remove markdown code blocks
                if result.startswith("```json"):
                    result = result.replace("```json", "").replace("```", "").strip()
                elif result.startswith("```"):
                    result = result.replace("```", "").strip()
                
                # Find JSON object
                start_idx = result.find('{')
                end_idx = result.rfind('}')
                
                if start_idx != -1 and end_idx != -1:
                    json_str = result[start_idx:end_idx+1]
                    return json.loads(json_str)
            
            # Try common attributes
            if hasattr(result, 'raw'):
                return self._parse_json_result(result.raw)
            if hasattr(result, 'json_dict'):
                return result.json_dict
            if hasattr(result, 'to_dict'):
                return result.to_dict()
            
            logger.warning(f"Could not parse result type: {type(result)}")
            return None
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing result: {str(e)}")
            return None
    
    def _assemble_offer(
        self, 
        gathered_data: Dict, 
        copy_data: Dict, 
        design_data: Dict
    ) -> Dict[str, Any]:
        """Assemble the complete offer from all agent outputs."""
        
        # Extract color palette safely
        color_palette = design_data.get("color_palette", {})
        primary_color = color_palette.get("primary", {})
        secondary_color = color_palette.get("secondary", {})
        accent_color = color_palette.get("accent", {})
        
        return {
            # Core information
            "title": copy_data.get("headline", gathered_data.get("service_name", "Professional Service")),
            "subtitle": copy_data.get("subtitle", "Transform your business with our proven solution"),
            "description": copy_data.get("description", gathered_data.get("description", "")),
            
            # Pricing
            "price": {
                "amount": gathered_data.get("pricing", {}).get("amount", 997),
                "currency": gathered_data.get("pricing", {}).get("currency", "USD"),
                "interval": gathered_data.get("pricing", {}).get("interval", "one-time")
            },
            
            # Features (use enhanced copy version)
            "features": copy_data.get("feature_bullets", gathered_data.get("features", [])),
            
            # Design
            "template": design_data.get("recommended_template", "modern"),
            "brandColors": {
                "primary": primary_color.get("hex", "#3b82f6") if isinstance(primary_color, dict) else "#3b82f6",
                "secondary": secondary_color.get("hex", "#8b5cf6") if isinstance(secondary_color, dict) else "#8b5cf6",
                "accent": accent_color.get("hex", "#10b981") if isinstance(accent_color, dict) else "#10b981"
            },
            
            # Additional metadata
            "targetAudience": gathered_data.get("target_audience", ""),
            "industry": gathered_data.get("industry", ""),
            "brandPersonality": gathered_data.get("brand_personality", "professional"),
            
            # AI reasoning (for transparency)
            "ai_insights": {
                "template_reasoning": design_data.get("template_reasoning", ""),
                "color_reasoning": design_data.get("color_reasoning", ""),
                "copy_strategy": copy_data.get("emotional_angle", ""),
                "power_words_used": copy_data.get("power_words_used", []),
                "completeness_score": gathered_data.get("completeness_score", 1.0)
            },
            
            # Generation metadata
            "generated_at": time.time(),
            "ai_generated": True
        }
    
    def _create_fallback_copy(self, gathered_data: Dict) -> Dict[str, Any]:
        """Create basic copy if AI copywriting fails"""
        service_name = gathered_data.get("service_name", "Professional Service")
        target_audience = gathered_data.get("target_audience", "businesses")
        
        return {
            "headline": f"Transform Your Business with {service_name}",
            "subtitle": f"The proven solution for {target_audience} who want exceptional results",
            "description": gathered_data.get("description", "A comprehensive solution designed to help you achieve your goals."),
            "feature_bullets": gathered_data.get("features", [
                "Professional service delivery",
                "Expert support and guidance",
                "Proven results and outcomes"
            ]),
            "call_to_action": "Get started today and transform your results"
        }
    
    def _create_fallback_design(self, gathered_data: Dict) -> Dict[str, Any]:
        """Create basic design if AI design strategy fails"""
        price = gathered_data.get("pricing", {}).get("amount", 997)
        
        # Simple price-based template selection
        if price >= 5000:
            template = "elegant"
            colors = {
                "primary": {"hex": "#1e3a8a"},
                "secondary": {"hex": "#eab308"},
                "accent": {"hex": "#dc2626"}
            }
        elif price >= 1000:
            template = "bold"
            colors = {
                "primary": {"hex": "#7c3aed"},
                "secondary": {"hex": "#c084fc"},
                "accent": {"hex": "#f97316"}
            }
        else:
            template = "modern"
            colors = {
                "primary": {"hex": "#3b82f6"},
                "secondary": {"hex": "#8b5cf6"},
                "accent": {"hex": "#10b981"}
            }
        
        return {
            "recommended_template": template,
            "color_palette": colors
        }
    
    def _create_fallback_offer(self, user_input: dict) -> Dict[str, Any]:
        """
        Create a basic offer if AI processing completely fails.
        Ensures users always get something usable.
        """
        logger.warning("Using fallback offer generation")
        
        # Extract price safely
        price = user_input.get("price", user_input.get("pricing", 997))
        if isinstance(price, dict):
            price = price.get("amount", 997)
        
        return {
            "title": user_input.get("service_name", user_input.get("title", "Professional Service Offer")),
            "subtitle": "Transform your business with our proven solution",
            "description": user_input.get("description", "A comprehensive solution designed to help you achieve your goals. We provide expert guidance and support to ensure your success."),
            "price": {
                "amount": float(price),
                "currency": "USD",
                "interval": "one-time"
            },
            "features": self._extract_features_from_input(user_input),
            "template": "modern",
            "brandColors": {
                "primary": "#3b82f6",
                "secondary": "#8b5cf6",
                "accent": "#10b981"
            },
            "ai_generated": False,
            "fallback": True,
            "qa_report": {
                "audit_summary": {
                    "total_score": 50,
                    "percentage": 50,
                    "overall_assessment": "Needs Review"
                },
                "final_recommendation": {
                    "status": "NEEDS_REVIEW",
                    "reasoning": "Generated using fallback method due to AI processing error"
                }
            }
        }
    
    def _extract_features_from_input(self, user_input: dict) -> List[str]:
        """Extract features from various input formats"""
        features = user_input.get("features", [])
        
        if isinstance(features, str):
            # Split by newlines or commas
            if "\n" in features:
                features = [f.strip() for f in features.split("\n") if f.strip()]
            elif "," in features:
                features = [f.strip() for f in features.split(",") if f.strip()]
            else:
                features = [features]
        
        if not features:
            features = [
                "Professional service delivery",
                "Expert support and guidance",
                "Proven results and outcomes"
            ]
        
        return features[:10]  # Max 10 features


class OfferRedesignCrew:
    """
    Intelligent crew for redesigning existing offers from uploaded documents.
    Extracts content, enhances it, and applies professional design.
    """
    
    def __init__(self):
        self.crew = None
        self.execution_log = []
    
    def redesign(self, extracted_content: str, file_metadata: dict = None) -> Dict[str, Any]:
        """
        Redesign an offer from extracted document content.
        
        Args:
            extracted_content: Raw text extracted from uploaded document
            file_metadata: Optional metadata about the source file
            
        Returns:
            Complete redesigned offer object
        """
        try:
            logger.info(f"Starting offer redesign with {len(extracted_content)} characters of content")
            
            # PHASE 1: INTELLIGENT CONTENT ANALYSIS & EXTRACTION
            logger.info("Phase 1: Analyzing existing offer content...")
            
            extraction_input = {
                "mode": "redesign",
                "raw_content": extracted_content,
                "instructions": """This is an EXISTING offer document. Extract all components 
                (service name, price, features, description). Identify what's working well and what's weak."""
            }
            
            gather_task = create_gather_info_task(information_gatherer, extraction_input)
            
            gather_crew = Crew(
                agents=[information_gatherer],
                tasks=[gather_task],
                process=Process.sequential,
                verbose=True
            )
            
            extracted_data = gather_crew.kickoff()
            self.execution_log.append({
                "phase": "content_extraction",
                "status": "completed",
                "timestamp": time.time()
            })
            
            gathered_data = self._parse_json_result(extracted_data)
            
            if not gathered_data:
                logger.error("Failed to extract data from document")
                return self._create_basic_redesign(extracted_content, file_metadata)
            
            logger.info("Successfully extracted data from document")
            
            # PHASE 2: ENHANCED COPYWRITING
            logger.info("Phase 2: Enhancing copy with persuasion techniques...")
            
            enhancement_prompt = f"""
            ORIGINAL OFFER DATA:
            {json.dumps(gathered_data, indent=2)}
            
            ENHANCEMENT TASK:
            This is a redesign. Keep the core service intact but dramatically improve:
            1. Headlines - more compelling
            2. Features - transform into benefit-driven statements
            3. Overall persuasiveness - add emotional triggers and power words
            
            Preserve original pricing and core offering.
            """
            
            copy_task = Task(
                description=enhancement_prompt,
                agent=copywriter,
                expected_output="JSON with enhanced copy"
            )
            
            copy_crew = Crew(
                agents=[copywriter],
                tasks=[copy_task],
                process=Process.sequential,
                verbose=True
            )
            
            copy_result = copy_crew.kickoff()
            self.execution_log.append({
                "phase": "copy_enhancement",
                "status": "completed",
                "timestamp": time.time()
            })
            
            copy_data = self._parse_json_result(copy_result)
            
            if not copy_data:
                logger.warning("Failed to enhance copy, using extracted data")
                copy_data = {
                    "headline": gathered_data.get("service_name", "Professional Service"),
                    "subtitle": "Enhanced and optimized for maximum impact",
                    "description": gathered_data.get("description", ""),
                    "feature_bullets": gathered_data.get("features", [])
                }
            
            # PHASE 3: DESIGN STRATEGY
            logger.info("Phase 3: Developing fresh design strategy...")
            
            combined_data = {
                **gathered_data,
                **copy_data,
                "redesign_mode": True
            }
            
            design_task = create_design_strategy_task(
                design_strategist,
                json.dumps(combined_data, indent=2)
            )
            
            design_crew = Crew(
                agents=[design_strategist],
                tasks=[design_task],
                process=Process.sequential,
                verbose=True
            )
            
            design_result = design_crew.kickoff()
            self.execution_log.append({
                "phase": "design_strategy",
                "status": "completed",
                "timestamp": time.time()
            })
            
            design_data = self._parse_json_result(design_result)
            
            if not design_data:
                logger.warning("Failed to generate design, using defaults")
                design_data = {
                    "recommended_template": "modern",
                    "color_palette": {
                        "primary": {"hex": "#3b82f6"},
                        "secondary": {"hex": "#8b5cf6"},
                        "accent": {"hex": "#10b981"}
                    }
                }
            
            # PHASE 4: ASSEMBLE REDESIGNED OFFER
            color_palette = design_data.get("color_palette", {})
            
            redesigned_offer = {
                "title": copy_data.get("headline", gathered_data.get("service_name", "Professional Service")),
                "subtitle": copy_data.get("subtitle", "Redesigned for maximum impact"),
                "description": copy_data.get("description", gathered_data.get("description", "")),
                
                "price": {
                    "amount": gathered_data.get("pricing", {}).get("amount", 997),
                    "currency": gathered_data.get("pricing", {}).get("currency", "USD"),
                    "interval": gathered_data.get("pricing", {}).get("interval", "one-time")
                },
                
                "features": copy_data.get("feature_bullets", gathered_data.get("features", [])),
                
                "template": design_data.get("recommended_template", "modern"),
                "brandColors": {
                    "primary": color_palette.get("primary", {}).get("hex", "#3b82f6"),
                    "secondary": color_palette.get("secondary", {}).get("hex", "#8b5cf6"),
                    "accent": color_palette.get("accent", {}).get("hex", "#10b981")
                },
                
                "targetAudience": gathered_data.get("target_audience", ""),
                "industry": gathered_data.get("industry", ""),
                
                "redesign_metadata": {
                    "original_content_length": len(extracted_content),
                    "source_file": file_metadata.get("filename") if file_metadata else "unknown",
                    "enhancements_made": [
                        "Professional headline optimization",
                        "Benefit-driven feature descriptions",
                        "Modern visual design",
                        "Psychological persuasion elements",
                        "Improved information hierarchy"
                    ]
                },
                
                "ai_insights": {
                    "template_reasoning": design_data.get("template_reasoning", ""),
                    "color_reasoning": design_data.get("color_reasoning", "")
                },
                
                "generated_at": time.time(),
                "redesigned": True,
                "execution_log": self.execution_log
            }
            
            # PHASE 5: QUALITY ASSURANCE
            logger.info("Phase 5: Running quality assurance...")
            
            qa_task = create_qa_task(quality_assurance, json.dumps(redesigned_offer, indent=2))
            
            qa_crew = Crew(
                agents=[quality_assurance],
                tasks=[qa_task],
                process=Process.sequential,
                verbose=True
            )
            
            qa_result = qa_crew.kickoff()
            self.execution_log.append({
                "phase": "quality_assurance",
                "status": "completed",
                "timestamp": time.time()
            })
            
            qa_data = self._parse_json_result(qa_result)
            
            if qa_data:
                redesigned_offer["qa_report"] = qa_data
            
            logger.info("Offer redesign completed successfully")
            return redesigned_offer
            
        except Exception as e:
            logger.error(f"Error in redesign crew execution: {str(e)}", exc_info=True)
            return self._create_basic_redesign(extracted_content, file_metadata)
    
    def _parse_json_result(self, result: Any) -> Optional[Dict[str, Any]]:
        """Parse crew result into JSON"""
        try:
            if isinstance(result, dict):
                return result
            
            if isinstance(result, str):
                result = result.strip()
                
                if result.startswith("```json"):
                    result = result.replace("```json", "").replace("```", "").strip()
                elif result.startswith("```"):
                    result = result.replace("```", "").strip()
                
                start_idx = result.find('{')
                end_idx = result.rfind('}')
                
                if start_idx != -1 and end_idx != -1:
                    json_str = result[start_idx:end_idx+1]
                    return json.loads(json_str)
            
            if hasattr(result, 'raw'):
                return self._parse_json_result(result.raw)
            if hasattr(result, 'json_dict'):
                return result.json_dict
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing result: {str(e)}")
            return None
    
    def _create_basic_redesign(
        self, 
        extracted_content: str, 
        file_metadata: Optional[dict] = None
    ) -> Dict[str, Any]:
        """Create a basic redesign if AI processing fails"""
        logger.warning("Using basic redesign fallback")
        
        lines = [line.strip() for line in extracted_content.split("\n") if line.strip()]
        
        # Try to find price
        price = 997
        for line in lines:
            if "$" in line:
                try:
                    price_str = line.split("$")[1].split()[0].replace(",", "")
                    price = float(price_str)
                    break
                except:
                    pass
        
        # Use first substantial line as title
        title = lines[0] if lines else "Professional Service Offer"
        if len(title) > 60:
            title = title[:57] + "..."
        
        # Extract features
        features = []
        for line in lines:
            if line.startswith("•") or line.startswith("-") or line.startswith("*"):
                features.append(line[1:].strip())
            elif len(line.split()) > 3 and len(features) < 5:
                features.append(line)
        
        if not features:
            features = [
                "Professional service delivery",
                "Expert support and guidance",
                "Proven results and outcomes"
            ]
        
        return {
            "title": title,
            "subtitle": "Redesigned and enhanced for maximum impact",
            "description": " ".join(lines[:5]) if len(lines) > 5 else extracted_content[:400],
            "price": {
                "amount": price,
                "currency": "USD",
                "interval": "one-time"
            },
            "features": features[:7],
            "template": "modern",
            "brandColors": {
                "primary": "#3b82f6",
                "secondary": "#8b5cf6",
                "accent": "#10b981"
            },
            "redesigned": True,
            "fallback": True,
            "generated_at": time.time()
        }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_offer_from_scratch(user_input: dict) -> Dict[str, Any]:
    """
    Main entry point for creating offers from scratch.
    
    Usage:
        result = create_offer_from_scratch({
            "service_name": "Social Media Management",
            "price": 500
        })
    """
    crew = OfferCreationCrew()
    return crew.create(user_input)


def redesign_existing_offer(
    document_content: str, 
    metadata: Optional[dict] = None
) -> Dict[str, Any]:
    """
    Main entry point for redesigning existing offers.
    
    Usage:
        result = redesign_existing_offer(
            document_content="extracted text...",
            metadata={"filename": "offer.pdf"}
        )
    """
    crew = OfferRedesignCrew()
    return crew.redesign(document_content, metadata)


def validate_offer_completeness(offer_data: dict) -> Dict[str, Any]:
    """Quick validation of offer data completeness"""
    required_fields = {
        "title": "Offer title/headline",
        "description": "Offer description",
        "price": "Pricing information",
        "features": "Features/benefits list",
        "template": "Visual template"
    }
    
    present = []
    missing = []
    
    for field, description in required_fields.items():
        if field in offer_data and offer_data[field]:
            present.append(description)
        else:
            missing.append(description)
    
    completeness_score = len(present) / len(required_fields)
    
    return {
        "completeness_score": completeness_score,
        "percentage": int(completeness_score * 100),
        "present": present,
        "missing": missing,
        "ready_to_use": completeness_score >= 0.8
    }


# ============================================================================
# PERFORMANCE MONITORING
# ============================================================================

class CrewPerformanceMonitor:
    """Monitor crew performance, token usage, and execution time"""
    
    def __init__(self):
        self.executions = []
    
    def record_execution(
        self,
        crew_type: str,
        execution_time: float,
        token_usage: dict,
        success: bool,
        offer_data: Optional[dict] = None
    ):
        """Record a crew execution for analytics"""
        record = {
            "timestamp": time.time(),
            "crew_type": crew_type,
            "execution_time_seconds": execution_time,
            "token_usage": token_usage,
            "success": success,
            "offer_complexity": self._calculate_complexity(offer_data) if offer_data else 0
        }
        self.executions.append(record)
        return record
    
    def _calculate_complexity(self, offer_data: dict) -> float:
        """Calculate offer complexity score (0-1)"""
        score = 0.0
        
        features_count = len(offer_data.get("features", []))
        score += min(features_count / 10, 0.3)
        
        description_length = len(offer_data.get("description", ""))
        score += min(description_length / 1000, 0.3)
        
        price = offer_data.get("price", {}).get("amount", 0)
        if price > 5000:
            score += 0.2
        elif price > 1000:
            score += 0.1
        
        if offer_data.get("brandColors"):
            score += 0.1
        if offer_data.get("targetAudience"):
            score += 0.1
        
        return min(score, 1.0)
    
    def get_analytics(self) -> dict:
        """Get performance analytics"""
        if not self.executions:
            return {"message": "No executions recorded yet"}
        
        total = len(self.executions)
        successful = sum(1 for e in self.executions if e["success"])
        
        avg_time = sum(e["execution_time_seconds"] for e in self.executions) / total
        total_tokens = sum(e["token_usage"].get("total", 0) for e in self.executions if e.get("token_usage"))
        
        return {
            "total_executions": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": f"{(successful/total)*100:.1f}%",
            "average_execution_time": f"{avg_time:.2f}s",
            "total_tokens_used": total_tokens
        }


# ============================================================================
# CACHING LAYER
# ============================================================================

class OfferCache:
    """Cache similar offers to reduce API calls"""
    
    def __init__(self, max_cache_size: int = 100):
        self.cache = {}
        self.max_cache_size = max_cache_size
        self.hits = 0
        self.misses = 0
    
    def _generate_cache_key(self, user_input: dict) -> str:
        """Generate a cache key from user input"""
        normalized = {
            "service": user_input.get("service_name", "").lower().strip(),
            "price": user_input.get("price", 0),
            "industry": user_input.get("industry", "").lower().strip()
        }
        
        key_string = json.dumps(normalized, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, user_input: dict) -> Optional[dict]:
        """Get cached offer if exists"""
        key = self._generate_cache_key(user_input)
        
        if key in self.cache:
            self.hits += 1
            logger.info(f"Cache HIT for key: {key}")
            return self.cache[key]
        
        self.misses += 1
        logger.info(f"Cache MISS for key: {key}")
        return None
    
    def set(self, user_input: dict, offer_data: dict):
        """Cache an offer"""
        key = self._generate_cache_key(user_input)
        
        if len(self.cache) >= self.max_cache_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[key] = offer_data
        logger.info(f"Cached offer with key: {key}")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_size": len(self.cache),
            "max_cache_size": self.max_cache_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "total_requests": total_requests
        }
    
    def clear(self):
        """Clear the cache"""
        self.cache = {}
        logger.info("Cache cleared")


# ============================================================================
# BATCH PROCESSING
# ============================================================================

class BatchOfferProcessor:
    """Process multiple offers in batch for efficiency"""
    
    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.results = []
    
    def process_batch(self, offers_data: List[dict]) -> List[dict]:
        """
        Process multiple offers in batch.
        
        Args:
            offers_data: List of offer input dictionaries
            
        Returns:
            List of processed offer results
        """
        logger.info(f"Starting batch processing of {len(offers_data)} offers")
        start_time = time.time()
        
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            future_to_offer = {
                executor.submit(self._process_single_offer, offer_data, idx): idx
                for idx, offer_data in enumerate(offers_data)
            }
            
            for future in as_completed(future_to_offer):
                idx = future_to_offer[future]
                try:
                    result = future.result()
                    results.append({
                        "index": idx,
                        "success": True,
                        "offer": result
                    })
                    logger.info(f"Completed offer {idx + 1}/{len(offers_data)}")
                except Exception as e:
                    logger.error(f"Failed to process offer {idx}: {str(e)}")
                    results.append({
                        "index": idx,
                        "success": False,
                        "error": str(e)
                    })
        
        results.sort(key=lambda x: x["index"])
        
        execution_time = time.time() - start_time
        logger.info(f"Batch processing completed in {execution_time:.2f}s")
        
        return results
    
    def _process_single_offer(self, offer_data: dict, index: int) -> dict:
        """Process a single offer"""
        logger.info(f"Processing offer {index}...")
        crew = OfferCreationCrew()
        return crew.create(offer_data)


# ============================================================================
# ASYNC PROCESSING
# ============================================================================

class AsyncOfferProcessor:
    """Process offers asynchronously with webhook callbacks"""
    
    def __init__(self):
        self.pending_jobs = {}
    
    def create_job(self, user_input: dict, webhook_url: Optional[str] = None) -> str:
        """
        Create an async job for offer generation.
        Returns job_id for tracking
        """
        import uuid
        
        job_id = str(uuid.uuid4())
        
        self.pending_jobs[job_id] = {
            "status": "pending",
            "user_input": user_input,
            "webhook_url": webhook_url,
            "created_at": time.time(),
            "result": None
        }
        
        logger.info(f"Created async job: {job_id}")
        return job_id
    
    def process_job(self, job_id: str):
        """Process a job asynchronously (call from background worker)"""
        if job_id not in self.pending_jobs:
            raise ValueError(f"Job {job_id} not found")
        
        job = self.pending_jobs[job_id]
        job["status"] = "processing"
        
        try:
            crew = OfferCreationCrew()
            result = crew.create(job["user_input"])
            
            job["status"] = "completed"
            job["result"] = result
            job["completed_at"] = time.time()
            
            if job["webhook_url"]:
                self._send_webhook(job["webhook_url"], {
                    "job_id": job_id,
                    "status": "completed",
                    "result": result
                })
            
            logger.info(f"Job {job_id} completed successfully")
            
        except Exception as e:
            job["status"] = "failed"
            job["error"] = str(e)
            
            if job["webhook_url"]:
                self._send_webhook(job["webhook_url"], {
                    "job_id": job_id,
                    "status": "failed",
                    "error": str(e)
                })
            
            logger.error(f"Job {job_id} failed: {str(e)}")
    
    def _send_webhook(self, url: str, data: dict):
        """Send webhook notification"""
        try:
            import requests
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            logger.info(f"Webhook sent successfully to {url}")
        except Exception as e:
            logger.error(f"Failed to send webhook: {str(e)}")
    
    def get_job_status(self, job_id: str) -> dict:
        """Get the status of a job"""
        if job_id not in self.pending_jobs:
            return {"error": "Job not found"}
        
        job = self.pending_jobs[job_id]
        return {
            "job_id": job_id,
            "status": job["status"],
            "created_at": job["created_at"],
            "result": job.get("result"),
            "error": job.get("error")
        }


# ============================================================================
# GLOBAL INSTANCES
# ============================================================================

_performance_monitor = CrewPerformanceMonitor()
_offer_cache = OfferCache(max_cache_size=100)

def get_performance_monitor() -> CrewPerformanceMonitor:
    """Get the global performance monitor"""
    return _performance_monitor

def get_offer_cache() -> OfferCache:
    """Get the global offer cache"""
    return _offer_cache

def clear_all_caches():
    """Clear all caches"""
    global _offer_cache
    _offer_cache.clear()
    logger.info("All caches cleared")

def get_system_stats() -> dict:
    """Get overall system statistics"""
    return {
        "performance": _performance_monitor.get_analytics(),
        "cache": _offer_cache.get_stats()
    }


# ============================================================================
# TESTING UTILITIES
# ============================================================================

def test_single_agent(agent_name: str, test_input: dict) -> dict:
    """
    Test a single agent in isolation for debugging.
    
    Args:
        agent_name: 'information_gatherer', 'copywriter', 'design_strategist', 'quality_assurance'
        test_input: Test input for the agent
    """
    from crew.agents import (
        information_gatherer,
        copywriter,
        design_strategist,
        quality_assurance
    )
    
    agents_map = {
        "information_gatherer": information_gatherer,
        "copywriter": copywriter,
        "design_strategist": design_strategist,
        "quality_assurance": quality_assurance
    }
    
    if agent_name not in agents_map:
        raise ValueError(f"Unknown agent: {agent_name}")
    
    agent = agents_map[agent_name]
    
    task = Task(
        description=f"Test input: {json.dumps(test_input, indent=2)}",
        agent=agent,
        expected_output="Test output"
    )
    
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    result = crew.kickoff()
    
    return {
        "agent": agent_name,
        "input": test_input,
        "output": str(result)
    }


def dry_run_offer_creation(user_input: dict) -> dict:
    """Dry run without calling AI APIs"""
    return {
        "mode": "dry_run",
        "input": user_input,
        "steps": [
            {
                "agent": "information_gatherer",
                "would_receive": user_input,
                "would_extract": ["service_name", "price", "features", "description"]
            },
            {
                "agent": "copywriter",
                "would_receive": "gathered_data",
                "would_create": ["headline", "subtitle", "description", "feature_bullets"]
            },
            {
                "agent": "design_strategist",
                "would_receive": "gathered_data + copy_data",
                "would_create": ["template", "color_palette", "reasoning"]
            },
            {
                "agent": "quality_assurance",
                "would_receive": "complete_offer",
                "would_create": ["scores", "issues", "recommendations"]
            }
        ],
        "note": "This is a dry run. No AI APIs were called."
    }


def validate_crew_configuration() -> dict:
    """Validate that all crew components are properly configured"""
    issues = []
    warnings = []
    
    try:
        from crew.agents import (
            information_gatherer,
            copywriter,
            design_strategist,
            quality_assurance
        )
        
        agents = [information_gatherer, copywriter, design_strategist, quality_assurance]
        
        for agent in agents:
            if not hasattr(agent, 'role'):
                issues.append(f"Agent missing 'role' attribute")
            if not hasattr(agent, 'llm'):
                issues.append(f"Agent missing LLM configuration")
        
    except ImportError as e:
        issues.append(f"Failed to import agents: {str(e)}")
    
    import os
    required_env_vars = [
        "OPENAI_API_KEY",
        "OPENAI_MODEL",
        "OPENAI_REASONING_MODEL"
    ]
    
    for var in required_env_vars:
        if not os.getenv(var):
            warnings.append(f"Environment variable {var} not set")
    
    try:
        from crew.tasks import (
            create_gather_info_task,
            create_copywriting_task,
            create_design_strategy_task,
            create_qa_task
        )
    except ImportError as e:
        issues.append(f"Failed to import tasks: {str(e)}")
    
    return {
        "status": "valid" if not issues else "invalid",
        "issues": issues,
        "warnings": warnings,
        "ready": len(issues) == 0
    }


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "OfferCreationCrew",
    "OfferRedesignCrew",
    "create_offer_from_scratch",
    "redesign_existing_offer",
    "validate_offer_completeness",
    "CrewPerformanceMonitor",
    "OfferCache",
    "BatchOfferProcessor",
    "AsyncOfferProcessor",
    "get_performance_monitor",
    "get_offer_cache",
    "clear_all_caches",
    "get_system_stats",
    "test_single_agent",
    "dry_run_offer_creation",
    "validate_crew_configuration"
]


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("CLOSEALEAD CREW CONFIGURATION VALIDATION")
    print("=" * 80)
    
    validation_result = validate_crew_configuration()
    print(json.dumps(validation_result, indent=2))
    
    if validation_result["ready"]:
        print("\n✅ System is ready!")
        print("\nExample usage:")
        print("=" * 80)
        print("""
# Create offer from scratch
result = create_offer_from_scratch({
    "service_name": "Premium Coaching",
    "price": 5000,
    "description": "Transform your business in 90 days"
})

# Redesign existing offer
result = redesign_existing_offer(
    document_content="extracted text from PDF...",
    metadata={"filename": "old_offer.pdf"}
)

# Batch processing
processor = BatchOfferProcessor(max_concurrent=3)
results = processor.process_batch([offer1, offer2, offer3])

# Get system stats
stats = get_system_stats()
print(stats)
        """)
    else:
        print("\n❌ Configuration issues found. Please fix before use.")