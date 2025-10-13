from crewai import Task

def create_gather_info_task(agent, user_input: dict):
    """Task to gather and structure offer information"""
    return Task(
        description=f"""
        Analyze the following information provided by the user and structure it into a complete offer format:
        
        User Input: {user_input}
        
        Extract and organize:
        1. Service/product description
        2. Target audience
        3. Pricing details
        4. Key features (at least 3)
        5. Main problem solved
        6. Brand personality
        
        Output a structured JSON with all components clearly defined.
        """,
        agent=agent,
        expected_output="Structured JSON with all offer components"
    )

def create_copywriting_task(agent, gathered_data: dict):
    """Task to create compelling copy"""
    return Task(
        description=f"""
        Using this gathered information: {gathered_data}
        
        Create persuasive marketing copy:
        1. Attention-grabbing headline (max 60 characters)
        2. Benefit-driven subtitle (max 120 characters)
        3. Persuasive description (200-300 words) using the AIDA framework
        4. 5-7 compelling feature bullets that emphasize benefits
        
        Use power words, emotional triggers, and clear benefits.
        Format output as JSON with fields: headline, subtitle, description, features
        """,
        agent=agent,
        expected_output="Polished marketing copy in JSON format"
    )

def create_design_strategy_task(agent, offer_data: dict):
    """Task to recommend design approach"""
    return Task(
        description=f"""
        Analyze this offer data: {offer_data}
        
        Recommend:
        1. Most appropriate template (modern, bold, elegant, or vibrant)
        2. Cohesive color palette (primary, secondary, accent)
        3. Typography recommendations
        4. Visual hierarchy suggestions
        
        Provide reasoning for each recommendation based on:
        - Brand personality
        - Industry standards
        - Target audience
        - Price point
        
        Output as JSON with template, colors, and reasoning.
        """,
        agent=agent,
        expected_output="Design specification with visual recommendations in JSON"
    )

def create_qa_task(agent, complete_offer: dict):
    """Task to review and validate the offer"""
    return Task(
        description=f"""
        Review this complete offer: {complete_offer}
        
        Check for:
        1. All required fields present
        2. Copy quality and grammar
        3. Brand consistency
        4. Visual coherence
        5. Persuasiveness score (0-100)
        
        Provide:
        - Overall score (0-100)
        - List of issues with severity (minor/major/critical)
        - Suggestions for improvements
        - Final recommendation (approve/revise/reject)
        
        Output as JSON with score, issues, and recommendations.
        """,
        agent=agent,
        expected_output="Quality report with pass/fail and suggestions in JSON"
    )
