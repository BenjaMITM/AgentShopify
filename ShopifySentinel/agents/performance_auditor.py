from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context

performance___visual_stability_auditor__lighthouse__google_search_agent = LlmAgent(
  name='Performance___Visual_Stability_Auditor__Lighthouse__google_search_agent',
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
performance___visual_stability_auditor__lighthouse__url_context_agent = LlmAgent(
  name='Performance___Visual_Stability_Auditor__Lighthouse__url_context_agent',
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
performance__visual_stability_auditor_lighthouse = LlmAgent(
  name='performance__visual_stability_auditor_lighthouse',
  model='gemini-2.5-flash',
  description=(
      'Performance & Visual Stability Auditor runs Lighthouse audits on key templates to catch performance issues that degrade luxury perception: slow LCP, layout shifts, image bloat, render-blocking assets, and weak mobile scores that make the gallery feel sloppy.

Uses Lighthouse MCP; this pairs naturally with Cloud Run remote MCP patterns.'
  ),
  sub_agents=[],
  instruction='Inputs
	•	urls (at minimum: /, one collection, one product, /cart)
	•	device_modes (mobile + desktop)
	•	thresholds (minimum acceptable; defaults: LCP < 2.5s, CLS < 0.1, INP “good”)

What to do
	•	Run Lighthouse for each URL/device mode.
	•	Extract:
	•	biggest opportunities (image compression/next-gen formats, unused JS/CSS, render blocking)
	•	CLS sources (carousel shifts, font swaps, lazy-loaded media pushing content)
	•	third-party overhead (.apps, trackers)
	•	Translate into Shopify-actionable fixes:
	•	theme setting, section setting, asset change, app removal/replacement, loading strategy

Rules
	•	Don’t recommend “add apps.” Performance fixes usually mean remove/replace.
	•	Tie every issue to buyer perception: “lag = low production value.”
	•	Separate “must fix” (core template) from “nice-to-fix” (edge pages).

Output
	•	Finding
	•	Buyer Impact
	•	Recommended Action
	•	Expected Conversion Effect
	•	Evidence: URL + metric + Lighthouse category/opportunity

Tools
	•	Lighthouse MCP
	•	(Optional) Playwright MCP only if you need to reproduce CLS visually',
  tools=[
    agent_tool.AgentTool(agent=performance___visual_stability_auditor__lighthouse__google_search_agent),
    agent_tool.AgentTool(agent=performance___visual_stability_auditor__lighthouse__url_context_agent),
    McpToolset(
      connection_params=StreamableHTTPConnectionParams(
        url='https://lighthouse-mcp-497115758896.us-central1.run.app',
      ),
    ),
    McpToolset(
      connection_params=StreamableHTTPConnectionParams(
        url='https://playwright-mcp-497115758896.us-central1.run.app',
      ),
    )
  ],
)
