# crew/tasks.py
from crewai import Task
import json


def create_gather_info_task(agent, user_input: dict):
    """
    Smart information processing task that handles complete or partial input.
    Extracts, validates, and structures offer information intelligently.
    """
    
    # Determine what information is already provided
    has_service = bool(user_input.get('service_name') or user_input.get('service') or user_input.get('title'))
    has_price = bool(user_input.get('price') or user_input.get('pricing') or user_input.get('cost'))
    has_features = bool(user_input.get('features'))
    has_description = bool(user_input.get('description') or user_input.get('about'))
    has_audience = bool(user_input.get('target_audience') or user_input.get('audience'))
    
    return Task(
        description=f"""
<task_context>
You are processing offer information that a user has provided. They may have given you complete details 
or just a rough description. Your job is to extract, validate, and structure everything intelligently.

The user is creating an offer presentation for their business. They want to transform their service/product 
information into a professional, conversion-optimized offer.
</task_context>

<user_provided_input>
{json.dumps(user_input, indent=2)}
</user_provided_input>

<information_already_present>
- Service/Product Name: {'✓ YES' if has_service else '✗ NO'}
- Pricing Information: {'✓ YES' if has_price else '✗ NO'}
- Features/Deliverables: {'✓ YES' if has_features else '✗ NO'}
- Description: {'✓ YES' if has_description else '✗ NO'}
- Target Audience: {'✓ YES' if has_audience else '✗ NO'}
</information_already_present>

<your_intelligent_processing_steps>

STEP 1: EXTRACT WHAT'S PROVIDED
Carefully read the user input and extract:
- Service/product name (exact words they used)
- Pricing (look for numbers, "$", "per month", "one-time", etc.)
- Features (look for bullet points, lists, "includes", "deliverables")
- Description (any explanatory text about what they offer)
- Target audience (look for "for", "helps", "designed for")
- Problem solved (pain points mentioned)
- Brand personality keywords (professional, friendly, luxury, etc.)

STEP 2: INTELLIGENT INFERENCE
For any missing critical information, make educated guesses based on context:
- If price is missing but it's a "premium coaching service", infer high price range ($2000+)
- If target audience isn't stated but service is "small business accounting", infer audience
- If features aren't listed but description is detailed, extract key deliverables from description
- If brand personality isn't stated, infer from language style (formal = professional, casual = friendly)

STEP 3: VALIDATE COMPLETENESS
Check if you have enough to create a compelling offer:
- MUST HAVE: Service name, price (or range), at least 3 features
- NICE TO HAVE: Target audience, problem solved, guarantees, brand personality
- If truly critical info is missing and cannot be inferred, note it specifically

STEP 4: STRUCTURE OUTPUT
Organize everything into this exact JSON format with your best interpretation of their offer.
</your_intelligent_processing_steps>

<required_output_format>
Return ONLY valid JSON with this structure (no additional text):

{{
  "service_name": "Exact name of the service/product",
  "service_type": "Category (e.g., coaching, software, consulting, course)",
  "description": "Comprehensive description combining their input and your understanding",
  "target_audience": "Who this is for (be specific: 'E-commerce business owners making $100k-$1M annually')",
  "problem_solved": "The main pain point or desire this addresses",
  "transformation": "The outcome or result customers achieve",
  "pricing": {{
    "amount": 997,
    "currency": "USD",
    "interval": "one-time" | "monthly" | "annually",
    "price_positioning": "premium" | "mid-range" | "affordable"
  }},
  "features": [
    "Detailed feature 1 with specifics",
    "Detailed feature 2 with specifics",
    "Detailed feature 3 with specifics",
    "Feature 4 if available",
    "Feature 5 if available"
  ],
  "unique_value_proposition": "What makes this different from competitors",
  "guarantees": ["Money-back guarantee", "Results guarantee", etc.] or [],
  "bonuses": ["Bonus 1", "Bonus 2"] or [],
  "brand_personality": "professional" | "friendly" | "bold" | "luxurious" | "technical",
  "industry": "Specific industry or niche",
  "urgency_elements": ["Limited spots", "Early bird pricing", etc.] or [],
  "social_proof_hints": ["Years of experience", "Client results", etc.] or [],
  "completeness_score": 0.0-1.0,
  "missing_critical_info": ["List anything truly critical that's missing and couldn't be inferred"],
  "inference_notes": "Brief note on what you inferred and why"
}}
</required_output_format>

<critical_instructions>
1. BE SMART: If they say "I help businesses with social media for $500/month", extract:
   - Service: Social Media Management
   - Price: $500, monthly
   - Target: Businesses
   - Infer features: Content creation, posting schedule, engagement, analytics

2. DON'T ASK QUESTIONS: Your job is to process and structure, not interview. Only note if something 
   critical is truly missing AND cannot be reasonably inferred.

3. PRESERVE THEIR VOICE: Use their exact words when possible, especially for service name and key phrases.

4. BE THOROUGH: Extract every detail they provided. Don't leave information out.

5. OUTPUT ONLY JSON: No explanatory text before or after. Just the JSON object.
</critical_instructions>

Now process the user input and return the structured JSON.
        """,
        agent=agent,
        expected_output="Structured JSON object with complete offer information"
    )


def create_copywriting_task(agent, gathered_data: str):
    """
    Master copywriting task that creates psychologically optimized, conversion-focused copy.
    """
    
    return Task(
        description=f"""
<task_context>
You have received structured offer information. Your mission is to transform this data into 
world-class, conversion-optimized marketing copy that compels the target audience to take action.

This copy will be used in a professional offer presentation that the business owner will send to 
potential clients. Every word must work towards getting a "YES".
</task_context>

<offer_data_you_received>
{gathered_data}
</offer_data_you_received>

<your_copywriting_process>

PHASE 1: DEEP ANALYSIS
Before writing a single word, analyze:
- WHO is the target audience? (Demographics, psychographics, pain points, desires)
- WHAT transformation are they seeking? (End result, not just features)
- WHY would they choose this over alternatives? (Unique mechanism, proof, differentiation)
- WHAT objections might they have? (Price, time, effort, skepticism, past failures)
- WHAT emotional triggers matter most? (Fear of loss, desire for gain, social status, time)

PHASE 2: HEADLINE CRAFTING (20+ OPTIONS, PICK BEST)
Test multiple headline formulas:

Formula 1 - Outcome + Timeframe:
"[Achieve Desired Result] in [Specific Timeframe] Without [Common Objection]"
Example: "Land 5-Figure Clients in 30 Days Without Cold Calling"

Formula 2 - Curiosity + Benefit:
"The [Adjective] [Method] That [Specific Result]"
Example: "The 7-Minute Morning Ritual That Doubled My Income"

Formula 3 - Question + Desire:
"What If You Could [Desired Outcome] Starting [Timeframe]?"
Example: "What If You Could Quit Your 9-5 Starting Next Month?"

Formula 4 - Number + Promise:
"[Number] Ways to [Desired Outcome] (Even If [Objection])"
Example: "3 Ways to Scale to $100K/Month (Even If You're Starting From Zero)"

Formula 5 - Bold Declaration:
"[Action Verb] [Desired Outcome] or [Guarantee]"
Example: "Double Your Revenue in 90 Days or Don't Pay a Cent"

PICK THE MOST POWERFUL ONE for this specific offer based on target audience psychology.

PHASE 3: SUBTITLE ENGINEERING
Create a subtitle that:
- Clarifies the headline's promise
- Adds credibility or social proof
- Addresses who it's for
- Includes a secondary benefit
- Max 120 characters

Format: "[Clarification of promise] for [target audience] who want [secondary benefit]"

PHASE 4: DESCRIPTION ARCHITECTURE (Use PASTOR Formula)

P - PROBLEM (2-3 sentences)
Start with the pain. Make them feel it. Use vivid language.
"You're working 60-hour weeks, constantly putting out fires, watching competitors grow while you're stuck..."

A - AMPLIFY (2 sentences)
Make the problem worse. Show the consequences of inaction.
"Every day you wait, you're leaving money on the table. Your competitors are capturing clients who should be yours..."

S - STORY/SOLUTION (2-3 sentences)
Introduce your offer as the bridge. Brief origin story if relevant.
"That's exactly why I created [Service Name]. After [credibility builder], I discovered..."

T - TRANSFORMATION & TESTIMONY (2-3 sentences)
Paint the picture of their new reality. Use specifics.
"Imagine waking up to a calendar full of qualified leads. Your revenue is predictable. You're working on strategy, not chaos..."

O - OFFER (2 sentences)
Clearly state what they get. Use "here's exactly what's included" language.
"Here's everything you get: [Summarize main components in benefit-focused way]..."

R - RESPONSE (1 sentence - CTA)
Strong, benefit-focused call to action.
"Click below to secure your spot and start [transformation] within [timeframe]."

PHASE 5: FEATURES → BENEFITS TRANSFORMATION

For each feature, use this formula:
"[Benefit-driven statement] — Here's how: [Feature explanation with specifics]"

EXAMPLE:
❌ Bad: "Weekly group coaching calls"
✓ Good: "Get unstuck instantly when challenges arise — Here's how: Join live weekly group coaching calls where you'll get real-time answers to your specific obstacles, plus learn from 20+ other business owners facing similar challenges."

Create 5-7 feature bullets following this exact format.

</your_copywriting_process>

<psychology_checklist>
Ensure your copy includes:
□ Specificity (exact numbers, timeframes, outcomes)
□ Social proof elements (even subtle ones like "proven", "trusted by", "over X clients")
□ Urgency/Scarcity (when appropriate - don't force it)
□ Risk reversal (guarantee language if applicable)
□ Emotional triggers (fear of loss OR desire for gain - pick dominant one)
□ Power words (minimum 5-7 throughout copy)
□ Transition words (however, because, therefore, meanwhile)
□ Active voice (minimum 85% of sentences)
□ Short sentences mixed with medium (create rhythm)
□ "You" language (speak directly to reader, minimum 10 times)
□ Contrast (before vs after, old way vs new way)
□ Specificity over generality (always)
</psychology_checklist>

<power_words_library>
Use 5-7 of these strategically throughout your copy:
Proven, Guaranteed, Exclusive, Limited, Secret, Breakthrough, Revolutionary, Transform, Unlock, 
Discover, Effortless, Explosive, Instant, Elite, Premium, Urgent, Rare, Unleash, Dominate, Skyrocket
</power_words_library>

<required_output_format>
Return ONLY valid JSON (no other text):

{{
  "headline": "Your best headline (40-60 characters)",
  "headline_rationale": "Brief explanation of why this headline will convert for this audience",
  "subtitle": "Clarifying, benefit-rich subtitle (80-120 characters)",
  "description": "Complete PASTOR-based description (250-400 words)",
  "description_word_count": 287,
  "feature_bullets": [
    "Benefit statement — Here's how: Feature with specifics",
    "Benefit statement — Here's how: Feature with specifics",
    "Benefit statement — Here's how: Feature with specifics",
    "Benefit statement — Here's how: Feature with specifics",
    "Benefit statement — Here's how: Feature with specifics"
  ],
  "call_to_action": "Specific, benefit-focused CTA",
  "power_words_used": ["List", "of", "power", "words", "you", "included"],
  "emotional_angle": "Fear of loss" OR "Desire for gain" OR "Social status" OR "Time freedom",
  "readability_score": "Grade 8-10 (your estimate)",
  "persuasion_score_self_assessment": 85
}}
</required_output_format>

<critical_rules>
1. NEVER use passive voice ("is provided by" → "I provide")
2. NEVER be generic ("great results" → "37% revenue increase in 60 days")
3. NEVER forget the target audience's specific language and pain points
4. ALWAYS lead with benefits before features
5. ALWAYS use their specific numbers and details from gathered data
6. OUTPUT ONLY JSON - no commentary before or after
</critical_rules>

Now create the copy. Make it legendary.
        """,
        agent=agent,
        expected_output="JSON object with psychologically optimized marketing copy"
    )


def create_design_strategy_task(agent, complete_data: str):
    """
    Strategic design task using O1's reasoning capabilities to make optimal visual decisions.
    """
    
    return Task(
        description=f"""
<task_context>
You are analyzing a complete offer (information + copy) to recommend the optimal visual presentation 
strategy. Your recommendations will directly impact conversion rates, so every decision must be 
backed by psychological principles and industry data.
</task_context>

<complete_offer_data>
{complete_data}
</complete_offer_data>

<your_analytical_framework>

STEP 1: EXTRACT KEY DECISION FACTORS
From the offer data, identify:
1. Price point (exact number) → Higher price demands more elegance/sophistication
2. Target audience demographics (age, income, education, role)
3. Target audience psychographics (values, fears, desires, aspirations)
4. Industry/niche (affects visual expectations)
5. Brand personality (is it professional? Bold? Luxurious? Approachable?)
6. Transformation type (practical? Emotional? Status-driven?)
7. Competition level (crowded market? Unique positioning?)

STEP 2: TEMPLATE SELECTION REASONING

For each template, score 0-10 based on fit:

MODERN TEMPLATE - Score: ?/10
Best for: B2B, SaaS, Tech, Consulting, Professional services
Strengths: Trust, efficiency, clarity, innovation
When to use: Audience values logic over emotion, price $500-$5000, decision-makers
Visual signals: Clean, whitespace, sans-serif, geometric, asymmetric
Avoid if: High emotional appeal needed, luxury positioning, creative industry

BOLD TEMPLATE - Score: ?/10
Best for: Coaching, Transformation, Personal brands, Creative agencies
Strengths: Impact, confidence, disruption, personality
When to use: Audience seeks change, price $1000-$10000, individual buyers
Visual signals: High contrast, large type, center-aligned, statement elements
Avoid if: Conservative industry, corporate buyers, subtle approach needed

ELEGANT TEMPLATE - Score: ?/10
Best for: Premium services, Luxury, High-ticket B2B, Executive services
Strengths: Sophistication, exclusivity, prestige, quality
When to use: Audience is high-net-worth, price $5000+, status-conscious buyers
Visual signals: Serif fonts, gold accents, symmetry, refined spacing
Avoid if: Approachable positioning needed, youth market, budget-conscious

VIBRANT TEMPLATE - Score: ?/10
Best for: Creative services, Events, Consumer products, Youth brands
Strengths: Energy, creativity, fun, memorable
When to use: Audience is young/creative, price $100-$2000, experience-focused
Visual signals: Gradients, multiple colors, rounded elements, dynamic
Avoid if: Professional/serious offer, corporate clients, premium positioning

Select the template with the highest score and explain your reasoning.

STEP 3: COLOR PALETTE ENGINEERING

Primary Color Selection (Main brand color):
- What emotion must this evoke? (Trust? Energy? Luxury? Creativity?)
- What does the target audience expect in this industry?
- How does price point influence color choice? (Higher price → deeper, sophisticated tones)
- Competitor analysis: What colors are oversaturated? What's missing?

Choose from:
- Blues (#1e3a8a to #0ea5e9): Trust, professionalism, tech, healthcare
- Greens (#166534 to #84cc16): Growth, wealth, wellness, sustainability
- Purples (#7c3aed to #c084fc): Luxury, creativity, transformation
- Reds/Corals (#dc2626 to #f87171): Urgency, passion, energy, action
- Oranges (#f97316): Enthusiasm, creativity, affordability
- Gold/Yellow (#eab308): Premium, exclusive, optimism
- Blacks/Grays (#000000 to #78716c): Sophistication, modern, authority

Secondary Color Selection (Supporting color):
- Must complement primary (use color theory: analogous or complementary)
- Provides visual variety without confusion
- Used for accents, subheadings, highlights

Accent Color Selection (CTA and highlights):
- Must contrast strongly with primary
- Draws eye to important elements (pricing, buttons, guarantees)
- Should trigger action (often warm colors: orange, red, green)

STEP 4: VALIDATE DECISIONS

Contrast Check:
- Primary + White background: Must pass WCAG AA (4.5:1 ratio minimum)
- Accent + Primary: Must be clearly distinguishable
- Overall palette: Maximum 3 colors for coherence

Psychological Alignment:
- Do colors match the transformation promise?
- Would target audience trust these colors?
- Does palette match price point positioning?

Industry Appropriateness:
- Is this expected in the industry? (Sometimes good, sometimes break patterns)
- Does it differentiate from competitors?

</your_analytical_framework>

<required_output_format>
Return ONLY valid JSON (no additional text):

{{
  "template_scores": {{
    "modern": 7,
    "bold": 9,
    "elegant": 6,
    "vibrant": 5
  }},
  "recommended_template": "bold",
  "template_reasoning": "Detailed explanation of why this template scores highest. Include: audience analysis, price point consideration, industry standards, psychological triggers needed, and competitive differentiation. Minimum 150 words.",
  "alternative_templates": ["modern", "elegant"],
  "alternative_reasoning": "Brief explanation of when alternatives might work better",
  
  "color_palette": {{
    "primary": {{
      "hex": "#7c3aed",
      "name": "Deep Purple",
      "psychology": "Luxury, transformation, creativity, wisdom",
      "rationale": "Why this color was chosen for this specific offer and audience"
    }},
    "secondary": {{
      "hex": "#c084fc",
      "name": "Lavender",
      "psychology": "Elegant, supportive, calming",
      "rationale": "How this supports the primary color and brand message"
    }},
    "accent": {{
      "hex": "#f97316",
      "name": "Orange",
      "psychology": "Action, enthusiasm, urgency",
      "rationale": "Why this creates the right call-to-action response"
    }}
  }},
  
  "color_reasoning": "Comprehensive explanation of the complete palette strategy. Discuss: emotional response, industry expectations, price point alignment, target audience preferences, contrast considerations, and conversion optimization. Minimum 100 words.",
  
  "typography_recommendations": {{
    "headline_style": "Bold, large, attention-grabbing",
    "body_style": "Readable, comfortable, professional",
    "size_hierarchy": "72px headline, 24px subtitle, 16px body (approximate)"
  }},
  
  "visual_hierarchy_strategy": [
    "1. Headline dominates with size and contrast",
    "2. Pricing prominently displayed in accent color",
    "3. Feature bullets with icons for scannability",
    "4. Description in comfortable reading width",
    "5. CTA button in accent color with high contrast"
  ],
  
  "psychological_elements": {{
    "trust_builders": ["How visual choices build credibility"],
    "attention_grabbers": ["Elements that capture initial attention"],
    "conversion_triggers": ["Visual cues that prompt action"]
  }},
  
  "industry_analysis": "Brief analysis of industry visual standards and how this approach fits or differentiates",
  
  "price_point_alignment": "Explanation of how visual sophistication matches the price positioning",
  
  "confidence_score": 0.92,
  "reasoning_summary": "One paragraph summarizing the entire visual strategy and why it will maximize conversions for this specific offer"
}}
</required_output_format>

<critical_instructions>
1. USE O1'S REASONING: Think through each decision step-by-step. Show your work.
2. BE SPECIFIC: Don't say "blue is trustworthy" - say "Navy blue (#1e3a8a) triggers trust and authority, perfect for this B2B consulting offer targeting executives"
3. CONSIDER PRICE: $100 offer gets different treatment than $10,000 offer
4. MATCH AUDIENCE: Corporate buyers expect different aesthetics than creative entrepreneurs
5. VALIDATE CHOICES: Every color must pass contrast requirements
6. PROVIDE REASONING: Your explanations matter as much as your choices
7. OUTPUT ONLY JSON: No commentary before or after
</critical_instructions>

Now analyze and provide your comprehensive design strategy.
        """,
        agent=agent,
        expected_output="JSON object with complete design strategy and detailed reasoning"
    )


def create_qa_task(agent, complete_offer_json: str):
    """
    Comprehensive quality assurance task using O1's analytical capabilities.
    Systematic 50-point evaluation with actionable feedback.
    """
    
    return Task(
        description=f"""
<task_context>
You are conducting a rigorous quality audit of a complete offer presentation. This offer will be used 
to close real deals, so it must be flawless. Your evaluation will determine if it's ready to deploy 
or needs improvements.

You will systematically check 50 quality criteria across 5 categories and provide detailed, 
actionable feedback.
</task_context>

<complete_offer_to_audit>
{complete_offer_json}
</complete_offer_to_audit>

<your_systematic_evaluation_process>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CATEGORY 1: COMPLETENESS (10 POINTS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Check each item. Award 1 point if present and quality:

□ Title present and compelling (not generic)
□ Subtitle clarifies value proposition clearly
□ Description exists and is 150-400 words
□ Price clearly stated with currency and interval
□ Minimum 3 features/benefits included
□ Template selected from valid options
□ Brand colors defined (primary, secondary, accent)
□ Target audience clear from copy
□ Problem/solution articulated
□ Call-to-action present and specific

Score: ?/10
Issues found: [List any]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CATEGORY 2: COPY QUALITY (15 POINTS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Evaluate each criterion:

□ Zero grammatical errors (1 point)
□ Zero typos or spelling mistakes (1 point)
□ Consistent tone throughout (1 point)
□ Active voice dominant (80%+ of sentences) (1 point)
□ Appropriate reading level (Grade 8-10) (1 point)
□ No unexplained jargon (1 point)
□ Benefit-to-feature ratio at least 2:1 (1 point)
□ Specific numbers/timeframes included (1 point)
□ Addresses at least one objection (1 point)
□ Social proof elements present (1 point)
□ Power words used appropriately (5-10 instances) (1 point)
□ Sentence variety (mix of short 5-10 words and medium 15-20 words) (1 point)
□ Paragraph length appropriate (2-4 sentences each) (1 point)
□ Smooth transitions between sections (1 point)
□ No redundant or filler phrases (1 point)

Score: ?/15
Issues found: [Be specific - cite exact text]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CATEGORY 3: PERSUASIVENESS (15 POINTS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Assess persuasion elements:

□ Clear problem-solution fit demonstrated (1 point)
□ Emotional triggers present and appropriate (1 point)
□ Urgency or scarcity mentioned (when appropriate) (1 point)
□ Strong unique value proposition (1 point)
□ Benefit-focused language throughout (1 point)
□ Risk reversal or guarantee (when applicable) (1 point)
□ Credibility markers or social proof (1 point)
□ Specific transformation clearly promised (1 point)
□ Logical flow from problem to solution (1 point)
□ Strong CTA with benefit (not just "click here") (1 point)
□ Price justified with value articulation (1 point)
□ Comparison advantage implied or stated (1 point)
□ Future-pacing language (help reader imagine outcome) (1 point)
□ Objection handling present (1 point)
□ FOMO elements if appropriate (1 point)

Score: ?/15
Persuasion strengths: [List what's working]
Persuasion gaps: [What's missing or weak]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CATEGORY 4: BRAND CONSISTENCY (5 POINTS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Evaluate coherence:

□ Personality matches selected template (1 point)
□ Colors are harmonious and pass contrast checks (1 point)
□ Tone matches stated brand personality (1 point)
□ Professional appearance matches price point (1 point)
□ Visual hierarchy supports brand positioning (1 point)

Score: ?/5
Brand alignment notes: [Observations]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CATEGORY 5: TECHNICAL CORRECTNESS (5 POINTS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Verify technical requirements:

□ All required fields have valid data types (1 point)
□ Character limits respected (title ≤60, subtitle ≤120) (1 point)
□ Color codes are valid hex values (1 point)
□ Price is positive number (1 point)
□ Features array has 3-10 items (1 point)

Score: ?/5
Technical issues: [List any]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL SCORE CALCULATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Add up all category scores: ?/50

Final Percentage: (Score / 50) × 100 = ?%

</your_systematic_evaluation_process>

<issue_identification_guidelines>

For each issue you identify, provide:

1. SEVERITY LEVEL:
   - CRITICAL: Prevents functionality (missing required fields, broken template reference)
   - MAJOR: Significantly reduces conversion (weak headline, no benefits, poor persuasion)
   - MINOR: Polish issues (small typo, suboptimal word choice, formatting)

2. EXACT LOCATION:
   - Field name: "headline", "feature_bullets[2]", "description paragraph 3"
   - Exact problematic text: Quote the specific issue

3. SPECIFIC ISSUE:
   - What's wrong: "Headline uses passive voice"
   - Why it matters: "Reduces urgency and action-orientation"

4. ACTIONABLE FIX:
   - Current: "Results are provided by our system"
   - Suggested: "Our system delivers results in 24 hours"

</issue_identification_guidelines>

<required_output_format>
Return ONLY valid JSON (no additional text):

{{
  "audit_summary": {{
    "total_score": 43,
    "total_possible": 50,
    "percentage": 86,
    "grade": "B+",
    "overall_assessment": "Excellent" | "Good" | "Acceptable" | "Needs Revision"
  }},
  
  "category_scores": {{
    "completeness": {{
      "score": 9,
      "max": 10,
      "percentage": 90
    }},
    "copy_quality": {{
      "score": 13,
      "max": 15,
      "percentage": 87
    }},
    "persuasiveness": {{
      "score": 12,
      "max": 15,
      "percentage": 80
    }},
    "brand_consistency": {{
      "score": 5,
      "max": 5,
      "percentage": 100
    }},
    "technical_correctness": {{
      "score": 4,
      "max": 5,
      "percentage": 80
    }}
  }},
  
  "issues": [
    {{
      "severity": "MAJOR",
      "category": "copy_quality",
      "location": "description, paragraph 2",
      "issue": "Passive voice used: 'Results are delivered by our team'",
      "why_it_matters": "Reduces urgency and personal connection",
      "current_text": "Results are delivered by our team within 24 hours",
      "suggested_fix": "Our team delivers results within 24 hours",
      "impact_on_conversion": "Medium - weakens authority and speed perception"
    }},
    {{
      "severity": "MINOR",
      "category": "persuasiveness",
      "location": "feature_bullets[3]",
      "issue": "Feature-focused instead of benefit-focused",
      "why_it_matters": "Readers care about outcomes, not features",
      "current_text": "Weekly group coaching calls",
      "suggested_fix": "Get unstuck instantly when challenges arise — Here's how: Join live weekly group coaching calls where you'll get real-time answers",
      "impact_on_conversion": "Low but cumulative across all features"
    }}
  ],
  
  "strengths": [
    "Headline is compelling with specific promise and timeframe",
    "Color palette perfectly matches premium positioning",
    "Description uses PASTOR formula effectively",
    "Strong social proof elements throughout",
    "Template selection aligns with target audience expectations"
  ],
  
  "improvement_priorities": [
    {{
      "priority": 1,
      "category": "persuasiveness",
      "issue": "No guarantee or risk reversal mentioned",
      "recommendation": "Add money-back guarantee or results guarantee to feature list",
      "expected_impact": "High - removes major objection"
    }},
    {{
      "priority": 2,
      "category": "copy_quality",
      "issue": "3 instances of passive voice in description",
      "recommendation": "Convert to active voice for stronger impact",
      "expected_impact": "Medium - improves urgency and clarity"
    }},
    {{
      "priority": 3,
      "category": "persuasiveness",
      "issue": "Features could emphasize benefits more",
      "recommendation": "Rewrite features using 'Benefit — Here's how: Feature' format",
      "expected_impact": "Medium - clearer value proposition"
    }}
  ],
  
  "conversion_optimization_notes": "Detailed paragraph explaining the offer's conversion potential and key improvements that would have the highest impact on close rate.",
  
  "competitive_positioning": "Brief analysis of how this offer compares to industry standards",
  
  "target_audience_alignment": "Assessment of how well the copy and design match the stated target audience",
  
  "final_recommendation": {{
    "status": "APPROVE" | "APPROVE_WITH_MINOR_CHANGES" | "REVISE_AND_RESUBMIT",
    "reasoning": "Comprehensive explanation of why this recommendation is given",
    "if_approved": "What makes this offer ready to convert",
    "if_revisions_needed": "What must be fixed before deployment",
    "estimated_conversion_potential": "Based on quality score, estimate conversion likelihood: High (8-10%), Medium (4-7%), Low (1-3%)"
  }},
  
  "next_steps": [
    "Specific action 1 to implement",
    "Specific action 2 to implement",
    "Specific action 3 to implement"
  ]
}}
</required_output_format>

<scoring_interpretation>
95-100 (A+): Exceptional - Deploy immediately, minimal risk
85-94 (A/B): Excellent - Minor tweaks optional, ready to test
75-84 (B/C): Good - Some improvements recommended before launch
65-74 (C/D): Acceptable - Several revisions needed
Below 65 (F): Needs major revision - critical issues present
</scoring_interpretation>

<critical_instructions>
1. BE THOROUGH: Check every single criterion systematically
2. BE SPECIFIC: Cite exact text when identifying issues
3. BE CONSTRUCTIVE: Focus on how to improve, not just what's wrong
4. BE REALISTIC: Don't expect perfection, but flag anything that hurts conversion
5. BE ACTIONABLE: Every suggestion should be implementable immediately
6. USE O1 REASONING: Think through each evaluation step-by-step
7. OUTPUT ONLY JSON: No explanatory text before or after
</critical_instructions>

Now conduct your comprehensive quality audit.
        """,
        agent=agent,
        expected_output="JSON object with complete quality audit including scores, issues, and actionable recommendations"
    )