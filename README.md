# candidacy

A job-application system rebuilt as a real application. It takes the fixed body of
truth about one person (achievement inventory, profile, career arc) and, for each
specific opening, researches the role, assesses fit, and produces the materials to
win it: a targeted CV, interview prep, and a recruiter brief.

The unit of work is a single **candidacy** (one role, one application), not a whole
career. The career is the input; a candidacy is the output.

## Status

Design phase. This repo is a from-scratch rebuild of the working pipeline currently
living in the `career` repo (`C:\Users\delos\code\career`). That repo stays the live
tool for passive job search until this one reaches parity on a real role. Nothing in
`career` is modified by this work.

## Why a rebuild

The `career` pipeline works, but its orchestration (loops, conditional routing,
resume, gating, QC retries) is written as prose inside Claude Code skills. Prose is a
poor fit for control flow, which is why the skills bloated and still make wrong
inference-driven decisions. Here the orchestration moves into code (a LangGraph state
graph) and the skills shrink to focused judgment steps.

## Stack

- Python
- LangGraph (state graph: explicit state, nodes, conditional edges, human-in-the-loop)
