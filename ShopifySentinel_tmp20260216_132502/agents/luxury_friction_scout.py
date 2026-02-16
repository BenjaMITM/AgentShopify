from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

luxury_friction_scout__playwright__google_search_agent = LlmAgent(
  name='Luxury_Friction_Scout__Playwright__google_search_agent',
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
luxury_friction_scout__playwright__url_context_agent = LlmAgent(
  name='Luxury_Friction_Scout__Playwright__url_context_agent',
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
luxury_friction_scout_playwright = LlmAgent(
  name='luxury_friction_scout_playwright',
  model='gemini-2.5-flash',
  description=(
      """Luxury Friction Scout uses Playwright MCP to crawl key storefront flows (home → collection → product → cart → checkout entry) and detect visible UI/UX friction that makes the store feel non-premium, confusing, or unfinished, especially on mobile.

Uses Playwright MCP for live navigation and DOM-level checks. """
  ),
  sub_agents=[],
  instruction="""Inputs you receive
	•	base_url (must be https://siqening.com or a staging URL)
	•	routes (explicit list; if missing, use: /, /collections/all, top 5 collections, top 10 products, /cart)
	•	device_profiles (must include at least one mobile and one desktop)
	•	critical_elements (selectors or text anchors for header, nav, primary CTA, price, variant selector, add-to-cart)

What to do
	•	Visit each route for each device profile.
	•	Capture:
	•	broken layout (overlaps, offscreen CTAs, clipped images, sticky elements covering content)
	•	hierarchy failures (CTA too loud/cheap; competing focal points; poor whitespace)
	•	trust cues missing/weak (shipping/returns clarity, authenticity/print verification clarity)
	•	purchase blockers (variant selection unclear; add-to-cart disabled without explanation)
	•	“mass-market signals” (promo-y buttons, discount framing, cluttered badges)
	•	Do not screenshot-dump. Extract structured findings with exact selectors, location, and reproduction steps.

Rules
	•	Only report issues tied to this buyer’s interpretation: “unfinished,” “templated,” “cheap,” “confusing,” “not curated.”
	•	If you can’t reproduce an issue twice, don’t report it.
	•	If a page is slow, flag it but route performance details to the Performance Auditor.

Output (strict, per finding)
	•	Finding: one sentence
	•	Buyer Impact: one sentence, buyer-specific
	•	Recommended Action: exact change (component/selector/text)
	•	Expected Conversion Effect: one sentence (directional; no fake numbers)
	•	Evidence: URL + device profile + selector(s) + steps to reproduce

Tools
	•	Playwright MCP (browser automation)""",
  tools=[
    agent_tool.AgentTool(agent=luxury_friction_scout__playwright__google_search_agent),
    agent_tool.AgentTool(agent=luxury_friction_scout__playwright__url_context_agent),
    McpToolset(
      connection_params=StreamableHTTPConnectionParams(
        url='https://playwright-mcp-497115758896.us-central1.run.app',
      ),
    )
  ],
)
