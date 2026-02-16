from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

# Import sub-agents
from ShopifySentinel.agents.friction_scout import frictionscout_playwright_mcp
from ShopifySentinel.agents.luxury_friction_scout import luxury_friction_scout_playwright
from ShopifySentinel.agents.navigation_graph import navigation_graph__deadend_detector_playwright__shopify_admin_2
from ShopifySentinel.agents.performance_auditor import performance__visual_stability_auditor_lighthouse
from ShopifySentinel.agents.search_visibility import search_visibility__index_hygiene_google_search_console_2
from ShopifySentinel.agents.behavioral_funnel_analyst import behavioral_funnel_analyst_google_analytics
from ShopifySentinel.agents.release_regression_watcher import release_regression_watcher_ga__gsc__lighthouse
from ShopifySentinel.agents.luxury_copy_editor import luxury_copy__microtrust_editor_shopify_admin__playwright
from ShopifySentinel.agents.catalog_integrity import catalog_integrity__merchandising_control_shopify_admin

siqening_store_sentinel__coordinator__google_search_agent = LlmAgent(
  name='Siqening_Store_Sentinel__Coordinator__google_search_agent',
  model='gemini-2.5-pro',
  description=(
      'Agent specialized in performing Google searches.'
  ),
  sub_agents=[],
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[
    GoogleSearchTool()
  ],
)
siqening_store_sentinel__coordinator__url_context_agent = LlmAgent(
  name='Siqening_Store_Sentinel__Coordinator__url_context_agent',
  model='gemini-2.5-pro',
  description=(
      'Agent specialized in fetching content from URLs.'
  ),
  sub_agents=[],
  instruction='Use the UrlContextTool to retrieve content from provided URLs.',
  tools=[
    url_context
  ],
)
root_agent = LlmAgent(
  name='Siqening_Store_Sentinel__Coordinator_',
  model='gemini-2.5-pro',
  description=(
      '
Siqening Store Sentinel is a coordinator agent that improves conversion and luxury credibility for Siqening by orchestrating specialized subagents connected via MCP tools (Playwright, Lighthouse, Google Analytics, Google Search Console, Shopify Admin). It continuously produces ranked, implementation-ready tickets that remove friction, fix structural errors, and sharpen gallery-grade presentation without diluting exclusivity. It treats UI quality as product quality, and optimizes for decisive, status-aware buyers who abandon anything that feels templated, cluttered, or uncertain. 
It continuously monitors the store to identify UI/UX friction, broken or incomplete navigation paths, sitemap dead ends, configuration errors, and presentation choices that weaken perceived value, credibility, or collector confidence.

The agent evaluates the site through the lens of a design-savvy, status-aware buyer who expects intentional curation, visual authority, and frictionless purchasing. It then delivers precise, implementation-ready recommendations to improve conversion rate, buyer trust, and aesthetic coherence without diluting exclusivity.

In short: it protects the store from looking accidental, unfinished, or amateur to the exact people who can afford to leave.'
  ),
  sub_agents=[frictionscout_playwright_mcp, luxury_friction_scout_playwright, navigation_graph__deadend_detector_playwright__shopify_admin_2, performance__visual_stability_auditor_lighthouse, search_visibility__index_hygiene_google_search_console_2, behavioral_funnel_analyst_google_analytics, release_regression_watcher_ga__gsc__lighthouse, luxury_copy__microtrust_editor_shopify_admin__playwright, catalog_integrity__merchandising_control_shopify_admin],
  instruction='You are the root coordinator. You do not browse the site yourself unless needed to validate a conflict. You delegate and enforce strict contracts.

Tooling model
	•	Each subagent is called as an “agent-as-tool”: isolated context, stateless inputs, strict output contract.  ￼
	•	MCP tools are integrated through ADK MCP toolsets and remote MCP servers.  ￼
	•	Remote MCP endpoints should be Streamable HTTP on Cloud Run (stable multi-client).  ￼

Dispatch rules
	•	Always run: FrictionScout, PerformanceAuditor, NavGraph, CatalogIntegrity on a full scan.
	•	Run: FunnelAnalyst and IndexHygiene on scheduled cadence or after changes.
	•	Run: CopyEditor only on pages with friction findings or weak trust cues.
	•	Run: RegressionWatcher after any deploy or theme/app change.

Output rules
	•	You output only a ranked backlog of tickets, grouped by template: Home / Collection / PDP / Cart / Policies / Navigation / Performance / Tracking / Catalog.
	•	Every ticket must include:
	•	Finding
	•	Buyer Impact
	•	Recommended Action
	•	Expected Conversion Effect
	•	Evidence (URL + component + reproduction steps or report reference)

Prioritization heuristic (strict)
	•	P0: breaks purchase flow, looks broken/unfinished, or creates trust doubt at price/checkout.
	•	P1: weakens luxury perception or hierarchy on core templates (home/collection/PDP).
	•	P2: reduces discoverability or clarity but doesn’t block purchase.
	•	P3: nice-to-fix polish.',
  tools=[
    agent_tool.AgentTool(agent=siqening_store_sentinel__coordinator__google_search_agent),
    agent_tool.AgentTool(agent=siqening_store_sentinel__coordinator__url_context_agent),
    McpToolset(
      connection_params=StreamableHTTPConnectionParams(
        url='https://gsc-remote-mcp-497115758896.us-central1.run.app',
      ),
    ),
    McpToolset(
      connection_params=StreamableHTTPConnectionParams(
        url='https://ga-remote-mcp-497115758896.us-central1.run.app',
      ),
    ),
    McpToolset(
      connection_params=StreamableHTTPConnectionParams(
        url='https://lighthouse-mcp-497115758896.us-central1.run.app',
      ),
    ),
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
