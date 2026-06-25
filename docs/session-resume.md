# Session Resume

Read this first when resuming work on candidacy. Update it at session close.

## Where we are

Repo just created. Design / setup phase of rebuilding the `career` pipeline as a
LangGraph app. Decisions are in `docs/design-decisions.md` (D1-D6). No code yet, by
intent: setting up engineering process (GitHub issues) before building.

## Done

- Scaffolded repo: README, CLAUDE.md, .gitignore, docs/design-decisions.md.
- Pushed to GitHub: `delos001/candidacy`.
- GitHub MCP is connected and working this session (read/write issues, repos, PRs all
  verified; authenticated as `delos001`).
- Agreed plan: milestone **M1: First slice (intake -> retrieval -> gap-analysis)** with
  5 starter issues:
  1. `chore:` scaffold Python project + add LangGraph (venv, requirements, a hello-world
     import that runs)
  2. `spike:` minimal runnable LangGraph (3-4 steps, one human-approval gate, one
     conditional branch; throwaway, to make the primitives concrete)
  3. `design:` map current intake / retrieval / gap-analysis skills with seam tags
     (extends the role-intake map already sketched in chat)
  4. `design:` shared state schema for the slice (labor over the gap-analysis output
     boundary; two downstream consumers depend on it)
  5. `design:` graph topology for the slice (steps + conditional edges; derived from
     #3 and #4)
  - Order: #2 needs #1; #4 needs #3; #5 needs #3 and #4. #3 can start anytime (no
    LangGraph knowledge required).

## Next action (resume here)

1. Decide labels: enable the toolset (see Open questions) or skip. Skipping is fine;
   the `chore:` / `spike:` / `design:` title prefixes already categorize.
2. Create the milestone **M1: First slice (intake -> retrieval -> gap-analysis)** in the
   GitHub UI (Issues -> Milestones -> New). The MCP cannot create milestones.
3. Have Claude create the 5 issues via the MCP, attached to the milestone, with the type
   prefix in each title.
4. Start issue #3 (map skills) and the #1/#2 learning track.

## Open questions / blockers

- **Labels toolset.** The GitHub MCP `labels` toolset (tool: `label_write`) is OFF by
  default. The Docker MCP Toolkit (beta) GUI did not obviously expose `GITHUB_TOOLSETS`.
  Browsing the catalog, the "GitHub Official" entry warned: "requires secrets to work.
  Configure servers within your created Profiles" (it wants a PAT set via a Toolkit
  Profile).
- **Which server is actually connected?** A GitHub MCP already works this session
  (issue read/write confirmed as `delos001`), so the live server is NOT the unconfigured
  catalog entry that threw the secrets warning. Before enabling labels, identify which
  server Claude Code is talking to and how it is configured (a Docker Toolkit profile vs
  a Claude Code `mcpServers` entry), then add `labels` (or `all`) to `GITHUB_TOOLSETS`
  on THAT server. Fallback: self-manage the server with
  `docker run -e GITHUB_TOOLSETS=all -e GITHUB_PERSONAL_ACCESS_TOKEN=... ghcr.io/github/github-mcp-server`
  (uses a PAT instead of the Toolkit's OAuth).

## Verified reference (do not re-research)

- Official `github-mcp-server` default toolsets: `context`, `repos`, `issues`,
  `pull_requests`, `users`. `labels` and ~14 others must be enabled via `GITHUB_TOOLSETS`
  (comma list; `all` enables everything).
- No milestone create/list/update tool exists at any config. Only `issue_write`'s
  `milestone` parameter, which assigns an issue to an already-existing milestone.
- `gh` CLI is NOT installed on this machine. Milestone creation therefore needs the
  GitHub UI (or install `gh` / call the REST API).
- Repo: `delos001/candidacy`.
