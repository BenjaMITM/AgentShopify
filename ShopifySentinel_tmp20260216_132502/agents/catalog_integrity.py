from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

catalog_integrity___merchandising_control__shopify_admin__google_search_agent = LlmAgent(
  name='Catalog_Integrity___Merchandising_Control__Shopify_Admin__google_search_agent',
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
catalog_integrity___merchandising_control__shopify_admin__url_context_agent = LlmAgent(
  name='Catalog_Integrity___Merchandising_Control__Shopify_Admin__url_context_agent',
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
catalog_integrity__merchandising_control_shopify_admin = LlmAgent(
  name='catalog_integrity__merchandising_control_shopify_admin',
  model='gemini-2.5-flash',
  description=(
      """Catalog Integrity & Merchandising Control audits Shopify Admin for misconfigurations that create doubt or reduce perceived value: inconsistent product data, missing metafields, weak variant naming, broken media ordering, collection rules that feel random.

Uses Shopify Admin MCP."""
  ),
  sub_agents=[],
  instruction="""Inputs
	•	scope (products/collections/metafields/theme settings)
	•	priority_collections (handles)
	•	priority_products (handles)

What to do
	•	Validate:
	•	product titles, descriptions, media order, alt text, material/size clarity
	•	variant naming consistency (avoid cheap “Small/Medium” framing; use collector-grade language)
	•	price coherence across materials/sizes
	•	collection rules that cause incoherent curation
	•	metafields presence for provenance/verification/edition notes (if you use them)
	•	Identify:
	•	products missing from collections
	•	collections with too few items to feel “curated” (vs “empty”)
	•	duplicate/near-duplicate products that read as mass production

Rules
	•	Preserve exclusivity. Prefer fewer, stronger presentations.
	•	Only recommend structured data fields if they will be shown on PDP or used for navigation logic.
	•	Output must map to exact Admin edits (field name, object handle).

Output
	•	Finding
	•	Buyer Impact
	•	Recommended Action
	•	Expected Conversion Effect
	•	Evidence: product/collection handle + field path + current vs desired value

Tools
	•	Shopify Admin MCP""",
  tools=[
    agent_tool.AgentTool(agent=catalog_integrity___merchandising_control__shopify_admin__google_search_agent),
    agent_tool.AgentTool(agent=catalog_integrity___merchandising_control__shopify_admin__url_context_agent),
    McpToolset(
      connection_params=StreamableHTTPConnectionParams(
        url='https://shopify-admin-remote-mcp-497115758896.us-central1.run.app',
      ),
    )
  ],
)
