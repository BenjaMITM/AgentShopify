from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context
from ..tools import maybe_mcp_toolset

search_visibility___index_hygiene__google_search_console__google_search_agent = LlmAgent(
  name='Search_Visibility___Index_Hygiene__Google_Search_Console__google_search_agent',
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
search_visibility___index_hygiene__google_search_console__url_context_agent = LlmAgent(
  name='Search_Visibility___Index_Hygiene__Google_Search_Console__url_context_agent',
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
search_visibility__index_hygiene_google_search_console_2 = LlmAgent(
  name='search_visibility__index_hygiene_google_search_console_2',
  model='gemini-2.5-flash',
  description=(
      """Search Visibility & Index Hygiene monitors indexing and search appearance issues that create “collector distrust” through broken previews, wrong canonicals, thin pages, or pages Google won’t index.

Uses Google Search Console MCP."""
  ),
  sub_agents=[],
  instruction="""Inputs
	•	site_property (exact GSC property)
	•	priority_urls (home, collections, top products)
	•	monitor_window_days (default 28)

What to do
	•	Pull:
	•	indexing coverage errors/warnings
	•	canonical problems
	•	sitemaps submitted vs discovered
	•	pages excluded that should be indexed (collections/products)
	•	rich result eligibility problems (if applicable)
	•	Identify “luxury harm” cases:
	•	titles/descriptions look spammy
	•	duplicates cause inconsistent previews
	•	thin category pages that look auto-generated

Rules
	•	Don’t optimize for generic SEO.
	•	Optimize for clean presence and authority signals.
	•	Every recommendation must map to Shopify actions: theme meta settings, template edits, redirects, sitemap configuration.

Output
	•	Finding
	•	Buyer Impact
	•	Recommended Action
	•	Expected Conversion Effect
	•	Evidence: property + report segment + affected URLs

Tools
	•	Google Search Console MCP""",
  tools=[
    agent_tool.AgentTool(agent=search_visibility___index_hygiene__google_search_console__google_search_agent),
    agent_tool.AgentTool(agent=search_visibility___index_hygiene__google_search_console__url_context_agent),
    *maybe_mcp_toolset("SHOPIFY_SENTINEL_MCP_GSC_URL"),
  ],
)
