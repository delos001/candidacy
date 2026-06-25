# candidacy - Project Instructions

## What this project is

A from-scratch rebuild of the `career` repo's job-application pipeline as a LangGraph
application. The `career` repo (`C:\Users\delos\code\career`) is the working
predecessor and the source of the skills being ported. It stays live and untouched
until this rebuild reaches parity.

## Tool usage

This is a Windows machine. Always use the PowerShell tool for commands (git, Python,
file operations via CLI). Never use the Bash tool: it runs a POSIX shell that does not
support PowerShell syntax. There are no POSIX scripts in this repo.

## Working directory

Use absolute paths for scripts and for file arguments passed to them.

## Communication

The user is new to LangGraph. Explain concepts in plain English and with small concrete
examples before using framework terminology. Do not assume prior knowledge of nodes,
graphs, state, or edges.

## Migration approach

- Build the graph spine first (state schema + topology), then fill steps one at a time.
  Do not port a skill until the step it belongs to exists in the graph.
- Port each skill through a quarantine step: copy it, then sort every line into one of
  three bins - judgment (keep, becomes step logic), orchestration (delete, the graph
  owns it), bloat (delete). A skill is done being ported when every line is assigned.
- A step earns standalone status only if it carries a seam: it transforms state into a
  new shape, makes a routing decision, gates on human review, fans out in parallel, or
  is independently retryable. A step that does none of these folds into its neighbor.
  Any step that brings prior work forward for the user to review and approve always
  stays distinct (the human review is the seam).
