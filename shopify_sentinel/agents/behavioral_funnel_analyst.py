from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context
from ..tools import maybe_mcp_toolset

behavioral_funnel_analyst__google_analytics__google_search_agent = LlmAgent(
  name='Behavioral_Funnel_Analyst__Google_Analytics__google_search_agent',
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
behavioral_funnel_analyst__google_analytics__url_context_agent = LlmAgent(
  name='Behavioral_Funnel_Analyst__Google_Analytics__url_context_agent',
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
behavioral_funnel_analyst_google_analytics = LlmAgent(
  name='behavioral_funnel_analyst_google_analytics',
  model='gemini-2.5-flash',
  description=(
      """Behavioral Funnel Analyst reads GA data to locate where qualified buyers hesitate or abandon: product-page exits, add-to-cart drop-offs, checkout entry failures, and device-specific issues.

Uses Google Analytics MCP"""
  ),
  sub_agents=[],
  instruction="""Inputs
	•	ga_property_id
	•	date_range (explicit)
	•	key_events (add_to_cart, begin_checkout, purchase; plus any custom events)

What to do
	•	Produce:
	•	product template funnel: view_item → add_to_cart → begin_checkout
	•	collection to product click-through rate by collection
	•	device split for key events and bounce/exit patterns
	•	anomalies after recent changes (regression detection)
	•	Generate diagnostic hypotheses that can be validated by Playwright:
	•	“Mobile ATC below fold”
	•	“Variant selection confusion”
	•	“Shipping/returns uncertainty”

Rules
	•	No vanity metrics.
	•	No generic CRO advice.
	•	Every finding must end with a testable, page-level action.

Output
	•	Finding
	•	Buyer Impact
	•	Recommended Action
	•	Expected Conversion Effect
	•	Evidence: report name + dimension + time window + delta direction

Tools
	•	Google Analytics MCP""",
  tools=[
    agent_tool.AgentTool(agent=behavioral_funnel_analyst__google_analytics__google_search_agent),
    agent_tool.AgentTool(agent=behavioral_funnel_analyst__google_analytics__url_context_agent),
    *maybe_mcp_toolset("SHOPIFY_SENTINEL_MCP_GA_URL"),
  ],
)
