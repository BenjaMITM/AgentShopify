from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context
from ShopifySentinel.tools import maybe_mcp_toolset

release_regression_watcher__ga___gsc___lighthouse__google_search_agent = LlmAgent(
  name='Release_Regression_Watcher__GA___GSC___Lighthouse__google_search_agent',
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
release_regression_watcher__ga___gsc___lighthouse__url_context_agent = LlmAgent(
  name='Release_Regression_Watcher__GA___GSC___Lighthouse__url_context_agent',
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
release_regression_watcher_ga__gsc__lighthouse = LlmAgent(
  name='release_regression_watcher_ga__gsc__lighthouse',
  model='gemini-2.5-flash',
  description=(
      """Release Regression Watcher runs scheduled checks after deployments/changes and flags regressions: performance drops, indexing changes, funnel degradation.

This is your “nothing quietly broke” agent."""
  ),
  sub_agents=[],
  instruction="""Inputs
	•	baseline_window_days (default 14)
	•	compare_window_days (default 2)
	•	urls (templates)
	•	events (key events)
	•	severity_thresholds (explicit deltas that trigger alerts)

What to do
	•	Compare current vs baseline:
	•	GA: add_to_cart rate, begin_checkout rate, revenue per session (direction only)
	•	GSC: sudden drops in indexed pages or spikes in excluded
	•	Lighthouse: LCP/CLS regressions on templates
	•	Output only:
	•	what changed
	•	likely cause categories
	•	which subagent should investigate next (handoff)

Rules
	•	No “maybe.” If uncertain, label as “needs validation by X agent.”
	•	Report only deltas that cross thresholds.

Output
	•	Finding
	•	Buyer Impact
	•	Recommended Action
	•	Expected Conversion Effect
	•	Evidence: metric + baseline vs current + window

Tools
	•	Google Analytics MCP
	•	Google Search Console MCP
	•	Lighthouse MCP""",
  tools=[
    agent_tool.AgentTool(agent=release_regression_watcher__ga___gsc___lighthouse__google_search_agent),
    agent_tool.AgentTool(agent=release_regression_watcher__ga___gsc___lighthouse__url_context_agent),
    *maybe_mcp_toolset("SHOPIFY_SENTINEL_MCP_GA_URL"),
    *maybe_mcp_toolset("SHOPIFY_SENTINEL_MCP_GSC_URL"),
    *maybe_mcp_toolset("SHOPIFY_SENTINEL_MCP_LIGHTHOUSE_URL"),
  ],
)
