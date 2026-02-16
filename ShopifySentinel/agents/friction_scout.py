from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

friction_scout__playwright_mcp__google_search_agent = LlmAgent(
  name='FrictionScout__Playwright_MCP__google_search_agent',
  model='gemini-2.5-flash',
  description=(
      'Agent specialized in performing Google searches.'
  ),
  sub_agents=[],
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[
    GoogleSearchTool()
  ],
)
friction_scout__playwright_mcp__url_context_agent = LlmAgent(
  name='FrictionScout__Playwright_MCP__url_context_agent',
  model='gemini-2.5-flash',
  description=(
      'Agent specialized in fetching content from URLs.'
  ),
  sub_agents=[],
  instruction='Use the UrlContextTool to retrieve content from provided URLs.',
  tools=[
    url_context
  ],
)
frictionscout_playwright_mcp = LlmAgent(
  name='frictionscout_playwright_mcp',
  model='gemini-2.5-flash',
  description=(
      'Runs deterministic page inspections and critical flows using a real browser to detect anything that makes Siqening feel broken, templated, cheap, or confusing on mobile and desktop.'
  ),
  sub_agents=[],
  instruction='	•	Use Playwright MCP to visit all routes for each device_profile.
	•	Validate: header/nav, hero, collection grid, PDP media, variant selection, ATC, cart drawer/page.
	•	Detect: clipped layouts, overlapping elements, missing/weak CTAs, unclear next action, trust gaps, “promo-looking” UI.
	•	Output only reproducible issues (two runs minimum).

Tool: Playwright MCP.',
  tools=[
    agent_tool.AgentTool(agent=friction_scout__playwright_mcp__google_search_agent),
    agent_tool.AgentTool(agent=friction_scout__playwright_mcp__url_context_agent)
  ],
)
