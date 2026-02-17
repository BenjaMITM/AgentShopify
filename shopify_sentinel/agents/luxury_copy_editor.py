from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context
from ..tools import maybe_mcp_toolset

luxury_copy___micro_trust_editor__shopify_admin___playwright__google_search_agent = LlmAgent(
  name='Luxury_Copy___Micro_Trust_Editor__Shopify_Admin___Playwright__google_search_agent',
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
luxury_copy___micro_trust_editor__shopify_admin___playwright__url_context_agent = LlmAgent(
  name='Luxury_Copy___Micro_Trust_Editor__Shopify_Admin___Playwright__url_context_agent',
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
luxury_copy__microtrust_editor_shopify_admin__playwright = LlmAgent(
  name='luxury_copy__microtrust_editor_shopify_admin__playwright',
  model='gemini-2.5-flash',
  description=(
      """Luxury Copy & Micro-Trust Editor scans critical UI copy (headers, product CTA blocks, material/size clarifiers, shipping/returns microcopy) and rewrites anything that reads mass-market, uncertain, or templated.

Uses Playwright MCP to locate copy in-context and Shopify Admin MCP to update editable fields/templates."""
  ),
  sub_agents=[],
  instruction="""Inputs
	•	pages (home, PDP, cart, footer policies)
	•	brand_voice_constraints (your Siqening voice)
	•	banned_tactics (discounting, hype, urgency spam)

What to do
	•	Identify copy that triggers buyer skepticism:
	•	generic “high quality”
	•	app-like disclaimers
	•	filler marketing
	•	ambiguous promises about prints/verification
	•	Rewrite as:
	•	restrained, declarative, gallery-appropriate
	•	specific about materials/fulfillment
	•	calm at price decision points
	•	Provide exact insertion locations:
	•	theme section name + block
	•	Shopify field name if applicable

Rules
	•	No long paragraphs unless it’s a dedicated manifesto/curator statement section.
	•	Do not broaden audience; write for the qualified buyer.
	•	Output one best rewrite per location, not options.

Output
	•	Finding
	•	Buyer Impact
	•	Recommended Action (exact replacement text + location)
	•	Expected Conversion Effect
	•	Evidence: URL + component/field

Tools
	•	Playwright MCP  ￼
	•	Shopify Admin MCP""",
  tools=[
    agent_tool.AgentTool(agent=luxury_copy___micro_trust_editor__shopify_admin___playwright__google_search_agent),
    agent_tool.AgentTool(agent=luxury_copy___micro_trust_editor__shopify_admin___playwright__url_context_agent),
    *maybe_mcp_toolset("SHOPIFY_SENTINEL_MCP_SHOPIFY_ADMIN_URL"),
    *maybe_mcp_toolset("SHOPIFY_SENTINEL_MCP_PLAYWRIGHT_URL"),
  ],
)
