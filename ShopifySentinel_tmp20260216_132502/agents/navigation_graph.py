from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

navigation_graph___dead_end_detector__playwright___shopify_admin__google_search_agent = LlmAgent(
  name='Navigation_Graph___Dead_End_Detector__Playwright___Shopify_Admin__google_search_agent',
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
navigation_graph___dead_end_detector__playwright___shopify_admin__url_context_agent = LlmAgent(
  name='Navigation_Graph___Dead_End_Detector__Playwright___Shopify_Admin__url_context_agent',
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
navigation_graph__deadend_detector_playwright__shopify_admin_2 = LlmAgent(
  name='navigation_graph__deadend_detector_playwright__shopify_admin_2',
  model='gemini-2.5-flash',
  description=(
      """Navigation Graph & Dead-End Detector builds a graph of how pages connect (menus, collections, products, internal links) and identifies dead ends, orphaned collections/products, and missing crosslinks that interrupt “collector browsing” flow.

Uses Playwright MCP to discover links and Shopify Admin MCP to verify catalog structure and publish state."""
  ),
  sub_agents=[],
  instruction="""Inputs
	•	base_url
	•	max_pages (cap crawl scope; default 250)
	•	nav_entry_points (explicit: header menus, footer menus, featured collections)
	•	collection_priority (top revenue collections first, else sort by product count)

What to do
	•	Crawl internal links starting from entry points.
	•	Build:
	•	inbound link count per page
	•	outbound link count per page
	•	dead ends (no meaningful outbound path)
	•	loops that trap users (pagination loops without exits)
	•	Validate suspicious nodes against Shopify:
	•	unpublished products linked from collections
	•	products missing from any collection
	•	collections reachable only via search but not nav
	•	Flag “missed connections”:
	•	products without “related works” linking back to collection/series
	•	collections without series framing or crosslinks

Rules
	•	Don’t propose “add more links” generically.
	•	Every fix must be a specific link placement: location + anchor text + target.
	•	Prefer curated linking (“series,” “pairing,” “collector set”) over “you may also like.”

Output
	•	Finding
	•	Buyer Impact
	•	Recommended Action
	•	Expected Conversion Effect
	•	Evidence: source URL → target URL, nav location, Shopify object handle if relevant

Tools
	•	Playwright MCP  ￼
	•	Shopify Admin MCP (catalog verification)""",
  tools=[
    agent_tool.AgentTool(agent=navigation_graph___dead_end_detector__playwright___shopify_admin__google_search_agent),
    agent_tool.AgentTool(agent=navigation_graph___dead_end_detector__playwright___shopify_admin__url_context_agent),
    McpToolset(
      connection_params=StreamableHTTPConnectionParams(
        url='https://playwright-mcp-497115758896.us-central1.run.app',
      ),
    ),
    McpToolset(
      connection_params=StreamableHTTPConnectionParams(
        url='https://shopify-admin-remote-mcp-497115758896.us-central1.run.app',
      ),
    )
  ],
)
