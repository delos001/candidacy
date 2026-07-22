# Session Resume

Read this first when resuming work on candidacy. Update it at session close.

## Where we are

Rebuilding the `career` pipeline as a LangGraph app. Design decisions so far are in
`docs/design-decisions.md` (D1-D6). Software, tooling, and cost are settled. The hands-on
LangGraph learning spike is COMPLETE: every core primitive was built by hand and verified
(state/nodes/edges, conditional fork, cycle + loop guard, QC re-route, a real Claude
subagent call, and a human interrupt + checkpointer, plus auto-generated diagram). The
`spike/` folder is being MOVED OUT of candidacy into a separate `programming-sandbox` repo
for future reference, so `spike/` will no longer exist here (do not reference its paths).
Next phase is the real pipeline design (M1). Work is in the VS Code Claude Code extension.

Teaching cadence (important for how the next session must run): the user hand-types every
line and learns by doing. Deliver ONE small snippet at a time (a few lines), explain it, and
WAIT for him to type/save/run before the next piece. Do not dump large code blocks; he
explicitly will not tolerate scrolling between code and explanation. Flag any contrived
teaching example as contrived up front (memory `flag-contrived-teaching-examples`).

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
- **Learning spike COMPLETE and verified.** Built by hand, every core primitive: state/
  nodes/edges, conditional fork, cycle + loop guard (`attempts`), QC re-route, real Claude
  subagent call (`ChatAnthropic` + `claude-haiku-4-5`), and human interrupt + `MemorySaver`
  checkpointer, plus auto diagram (`graph.mmd`/`graph.png`). The user is moving the whole
  `spike/` folder (incl. `smoke_test.py`) to a separate `programming-sandbox` repo, so it
  will be GONE from candidacy; do not reference `spike/` paths going forward.
- **`.env` key incident (resolved):** the original API key in `spike/.env` was accidentally
  blanked (the file was open in the editor and autoSave persisted an emptied buffer; VS Code
  local history confirmed a 130-byte -> 4-byte write). User generated a new key. Lessons for
  the real build: keep `.env` closed in the editor, keep a durable backup (password manager),
  and remember API keys are shown only once at creation.

## Next action (resume here): begin M1 pipeline design

The learning spike is COMPLETE (see Done) and its folder is being moved out to a separate
`programming-sandbox` repo, so do not reference `spike/` paths. The real design work starts
now. First slice is M1: intake -> retrieval -> gap-analysis.

Per CLAUDE.md migration approach:
- Build the graph spine first (real shared-state schema + topology), then fill steps one at a
  time. Do not port a skill until its step exists in the graph.
- Port each `career` skill through the quarantine step: copy it, sort every line into judgment
  (keep -> becomes step logic or loadable prompt text), orchestration (delete, the graph owns
  it), or bloat (delete). A skill is done being ported when every line is assigned.
- A step earns standalone status only if it carries a seam (reshapes state, routes, gates on
  human review, fans out, or is independently retryable); otherwise it folds into a neighbor.
  Any step that brings prior work forward for user review always stays distinct.

Concrete first moves: (1) read the `career` repo (`C:\Users\delos\code\career`) intake/
retrieval/gap-analysis skills to inventory what each does; (2) draft the real State schema for
M1; (3) sketch the M1 topology. Teaching cadence still applies: one small snippet at a time,
the user hand-types, flag contrived examples.

Design patterns confirmed during the spike (carry these into the real build):
- Skill/instruction CONTENT lives in flat files (`.md`/`.txt`) that a node reads into its
  prompt at runtime; the `.py` holds only orchestration. Sorting a career skill splits it:
  judgment -> loadable prompt text; orchestration -> graph topology.
- Run state/history goes to a checkpointer (RAM `MemorySaver` for dev; SQLite/Postgres for
  durable, survives process exit). This is a separate "memory" from the instruction files.
- LLM node call path: `ChatAnthropic` from `langchain-anthropic`, model id `claude-haiku-4-5`
  (spike only; real tiers are the deferred bake-off, issue #1), key from a gitignored `.env`
  via `load_dotenv`. Human stop-and-wait = `interrupt()` in a node + `Command(resume=...)` on
  the second `invoke`, with the same `thread_id` config on both calls.

A script-organization convention was also developed this session (greppable banner tokens:
`# ==> Section:` for top-level sections, `# --> Node/Router (name)` for members, each router
kept directly under the node it reads). The user may reuse it for the real app; it lives in
his head / the moved spike, not in a doc here.

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
