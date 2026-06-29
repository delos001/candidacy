# Session Resume

Read this first when resuming work on candidacy. Update it at session close.

## Where we are

Setup / learning phase of rebuilding the `career` pipeline as a LangGraph app. The
pipeline itself has NOT been designed yet, by intent. Design decisions so far are in
`docs/design-decisions.md` (D1-D6). Software, tooling, and cost are now settled; the
immediate next work is a hands-on LangGraph learning spike to make the primitives concrete
before any real design.

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
- DECIDE FIRST: the subagent step is stub (free, deterministic) vs a real tiny Claude call.
  User leaned "real" to understand it, but a real call needs Anthropic **API** billing set
  up on the Console (separate from the $100/mo subscription; pennies, but a one-time setup
  step) plus an `ANTHROPIC_API_KEY` in a gitignored `.env` loaded via python-dotenv. Confirm
  stub vs real at the start, since real has the billing prerequisite.

After the spike lands, the real design work begins (map the intake/retrieval/gap-analysis
skills, the shared state schema, the graph topology).

## Open questions / blockers

- **Spike subagent step: stub vs real Claude call.** Real needs API billing on the Console +
  an `ANTHROPIC_API_KEY` in a gitignored `.env`. Decide at start.
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
