# Session Resume

Read this first when resuming work on candidacy. Update it at session close.

## Where we are

Setup / learning phase of rebuilding the `career` pipeline as a LangGraph app. The
pipeline itself has NOT been designed yet, by intent. Design decisions so far are in
`docs/design-decisions.md` (D1-D6). Software, tooling, and cost are now settled; the
immediate next work is a hands-on LangGraph learning spike to make the primitives concrete
before any real design. The spike is fully specced, its open decisions are locked, and all
setup is done (API key placed, $20 credit funded). Work is moving into the VS Code Claude
Code extension; the immediate next action is a one-line smoke test to confirm the real
Claude call works, then building the spike graph (see Next action).

Convention agreed this session: durable design decisions live in `docs/design-decisions.md`;
findings and work items live in GitHub (issues), not local docs. Keeps decisions in one
place and findings out of the auto-loaded context.

## Done

- Scaffolded repo (README, CLAUDE.md, .gitignore, docs/) and pushed to `delos001/candidacy`.
- Software confirmed, nothing to install: the `agents` conda env (Python 3.13) already has
  the full LangGraph stack (langgraph 1.1.3, langchain, langchain-anthropic, anthropic SDK,
  python-dotenv). Source of truth: `engops/conda/agents.yml`. Activate this env for
  candidacy work (`engops/conda/overview.md`).
- Cost audit of `career` (the metered-API question): ~52 billed LLM calls, ~1.15M input /
  ~35K output tokens per candidacy; ~$2-4/role on a realistic model mix. Recorded as GitHub
  **issue #1** (cross-cutting finding, not attached to a milestone). The model-tier choice,
  especially the retrieval scorers, is DEFERRED to a bake-off when the retrieval node is
  built. Do not lock tiers before then.
- GitHub MCP fixed and documented (see Open questions + `engops/claude/reference.md`).
- Milestone **M1: First slice (intake -> retrieval -> gap-analysis)** exists in GitHub
  (empty; no issues attached). The 5 starter issues from the earlier plan were NOT filed;
  that plan is superseded by doing the learning spike first.
- **LangGraph Studio evaluated:** a later, optional visual debugger (not no-code), to
  revisit once a real graph exists. Build the spike with the built-in Mermaid render first.
  Full write-up + adoption prerequisites (langgraph-cli, langgraph.json, LangSmith, agents.yml
  update) live in GitHub **issue #3**, not here.
- **Spike subagent step RESOLVED: real Claude call** (not stub). Model `claude-haiku-4-5`
  (pennies). Billing prerequisite handled: user added **$20 of API credit in the Anthropic
  Console** (the developer "Pool 2", separate site `console.anthropic.com`). Confirmed via
  Anthropic help center that the claude.ai subscription "usage credits" (Pool 1, ~$99.60)
  do NOT pay for API calls; the API is a separate prepaid balance. **API key DONE:** user
  generated it in the Console and saved it to `spike/.env` as `ANTHROPIC_API_KEY=...`
  (`.env` is covered by `.gitignore`; confirmed the file exists at `candidacy/spike/.env`).
- **Real-call reference check DONE** (claude-api skill, 2026-07-13). Exact model id is the
  plain alias `claude-haiku-4-5` (do NOT append a date suffix). The call path for a LangGraph
  app is `ChatAnthropic` from `langchain-anthropic` (installed), which reads `ANTHROPIC_API_KEY`
  from the env that python-dotenv loads. Haiku is a deliberate spike-only choice (cheapest
  tier); the real pipeline's model is the deferred bake-off, not this.
- **Working style captured** (memory `user-types-code-himself`): the user hand-types the
  code to learn; deliver explained snippets, do NOT author implementation files with
  Write/Edit. Reserve direct writes for scaffolding/config/docs he approves.
- **Environment switch verified.** Moving from a standalone terminal to the **Claude Code VS
  Code extension** (better for hand-typing + a step-debugger for learning; PowerShell remains
  the shell underneath, so the "use PowerShell" rule is unaffected). Extension and CLI share
  the same conversation store, so this session is resumable there.

## Next action (resume here): build the learning spike

A small, throwaway, runnable LangGraph script to make the primitives concrete. Agreed spec:

- One script in candidacy in a clearly-marked `spike/` folder (disposable, separate from any
  real work). Themed lightly on the application pipeline (intake -> retrieve -> gap-check ->
  draft -> qc -> review -> finalize) but fake.
- Must demonstrate: shared state (the notepad), nodes, edges, a fork (conditional edge), a
  re-route back to a previous step (a cycle, with a loop-count guard), a small QC trigger
  (re-route on fail), a subagent trigger (a node that delegates a small sub-task), and a
  human stop-and-wait (interrupt + a checkpointer so it can pause/resume).
- Auto-generate a diagram each run: a PNG via LangGraph's built-in Mermaid render, plus the
  Mermaid text saved alongside. (LangGraph Studio is a later, optional upgrade.)
- Subagent step is a **real Claude call** (`claude-haiku-4-5`) via `ChatAnthropic` from
  `langchain-anthropic`, key loaded from `spike/.env` via python-dotenv. Confirm the exact
  model id and `ChatAnthropic` usage against the claude-api reference when writing that node.

IMMEDIATE next step (in VS Code, session resumed there):
1. **Smoke test the real call.** Type this into `spike/smoke_test.py` (throwaway, delete after):

   ```python
   from dotenv import load_dotenv
   from langchain_anthropic import ChatAnthropic

   load_dotenv("spike/.env")
   llm = ChatAnthropic(model="claude-haiku-4-5", max_tokens=50)
   print(llm.invoke("Say hello in exactly five words.").content)
   ```

   Run from the project root: `conda activate agents; python spike/smoke_test.py`. A
   five-word greeting = billing + key + env all confirmed. On error, a bad key vs an unfunded
   account give distinct messages.
2. **Build the spike** per the sequence below (deliver as snippets the user types, not file
   writes). The `spike/` folder already exists; `spike/.env` holds the key.

Environment-switch reference (mostly done): VS Code extension installed + signed in; resume
this conversation via the Claude Code panel's **Session history** button (extension + CLI
share one store). CLI `claude --continue` / `--resume` also works but needs the standalone
CLI on PATH (`irm https://claude.ai/install.ps1 | iex`), separate from the extension's bundle.

Agreed build sequence for the spike: (1) state schema + node stubs + wiring, run dry;
(2) add fork/cycle/loop-guard; (3) add interrupt + checkpointer; (4) swap gap_check to the
real Claude call; (5) add diagram output (write `spike/graph.mmd` + render `spike/graph.png`,
render wrapped in try/except). Deliver as snippets for the user to type, not file writes.

After the spike lands, the real design work begins (map the intake/retrieval/gap-analysis
skills, the shared state schema, the graph topology).

## Open questions / blockers

- **Setup fully done** (was: API key placement). Stub-vs-real resolved to real; $20 Console
  credit funded; API key generated and saved to `spike/.env`. Next is the smoke test, then
  the build. No setup blockers remain.
- **Model-tier bake-off deferred** to the retrieval-node build (issue #1). Scorers are graded
  relevance judgments, not mechanical lookups; whether Haiku holds quality is unknown.
- **GitHub MCP: resolved.** Connected server is the self-managed
  `docker run ... ghcr.io/github/github-mcp-server` defined in `~/.claude.json` top-level
  `mcpServers`. Full config, the two-tier token model, and the 403-on-write gotcha are in
  `engops/claude/reference.md` > GitHub MCP.
- **Optional, deferred: extra MCP toolsets.** No `GITHUB_TOOLSETS` set, so `labels` etc. are
  off; add `-e GITHUB_TOOLSETS=all` to the docker args to enable. Not needed for issue/PR work.

## Verified reference (do not re-research)

- `agents` conda env carries the LangGraph stack; activate it for candidacy (`engops/conda/`).
- Cost numbers + pricing snapshot: GitHub issue #1.
- Decisions -> `docs/design-decisions.md`; findings/work -> GitHub. (A cost "D7" was drafted
  then removed; the cost finding lives in issue #1, not the decisions file.)
- `github-mcp-server` default toolsets: `context`, `repos`, `issues`, `pull_requests`,
  `users`. Others (incl. `labels`) need `GITHUB_TOOLSETS`.
- Milestones: readable via the REST API with the PAT (confirmed). No MCP tool to create or
  list them; `issue_write` can only assign an issue to an existing milestone. Create in the
  GitHub UI. `gh` CLI is not installed.
- Repo: `delos001/candidacy`.
- VS Code extension (verified 2026-07-13 vs `code.claude.com/docs/en/vs-code.md`): resume
  past sessions via the panel's **Session history** button; extension + CLI share one
  conversation store; extension install is marketplace + browser sign-in (no API key). The
  bundled CLI is NOT on PATH; running `claude` in the integrated terminal needs the separate
  standalone CLI install. Unconfirmed by docs: whether opening the project folder as the
  workspace is strictly required (open it to be safe).
- Billing pools (verified vs Anthropic help center): Pool 1 = claude.ai subscription "usage
  credits" (covers claude.ai + Claude Code terminal usage), bought at `claude.ai`. Pool 2 =
  developer API prepaid credits, bought separately at `console.anthropic.com`. They do not
  cross over. The spike's real call spends Pool 2.
