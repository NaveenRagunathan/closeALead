from crewai import Agent
from langchain_openai import ChatOpenAI
from core.config import settings

# Initialize LLM
llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    api_key=settings.OPENAI_API_KEY,
    temperature=0.7
)

# Agent 1: Information Gatherer
information_gatherer = Agent(
    role='Information Gatherer',
    goal='Extract complete offer details through natural conversation',
    backstory="""You are an expert business consultant helping entrepreneurs articulate their service offers.
    Your goal is to extract complete, clear information through natural conversation.
    You ask one question at a time and provide examples if users seem stuck.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Agent 2: Copywriter
copywriter = Agent(
    role='Persuasive Copywriter',
    goal='Transform raw information into compelling sales copy',
    backstory="""You are an award-winning copywriter specializing in high-converting sales presentations.
    Your writing has generated millions in revenue for clients across industries.
    You lead with benefits, not features, and use power words that trigger emotion.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Agent 3: Design Strategist
design_strategist = Agent(
    role='Design Strategist',
    goal='Recommend optimal visual presentation',
    backstory="""You are a senior UX/UI designer with expertise in conversion optimization.
    You understand color theory, typography, visual hierarchy, and psychology of persuasion.
    You match templates to brand personalities and industries.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Agent 4: Quality Assurance
quality_assurance = Agent(
    role='Quality Assurance Specialist',
    goal='Ensure offer completeness and consistency',
    backstory="""You are a meticulous quality assurance specialist ensuring every offer is complete and effective.
    You check for completeness, copy quality, persuasiveness, and brand consistency.
    You provide actionable feedback for improvements.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)
