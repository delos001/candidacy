# Design Decisions

Foundational decisions for the candidacy rebuild. Append as decisions are made; keep
each entry terse.

## D1 - Rebuild as a LangGraph application, in a new repo

The `career` pipeline works but bloats because orchestration lives as prose inside
skills. Rebuild it as a LangGraph state graph: orchestration in code, skills reduced to
focused judgment steps. New repo (`candidacy`) so the `career` repo stays a stable
working tool for passive search until this reaches parity. `career` is never modified by
this work.

## D2 - Build the spine first, then fill steps

The unit of migration is the graph, not the skill. Design the shared state and the graph
topology first; stand up the skeleton; then fill steps one at a time into slots that
already exist. Porting skills in isolation would recreate capable workers with weak
orchestration - the same disease in a new language.

## D3 - First vertical slice: intake -> retrieval -> gap-analysis

No single deliverable is separable: CV and interview prep both consume the front of the
pipeline. The dependency order dictates the build order. First slice is the shared front
(role-intake -> retrieval -> gap-analysis), ending in a real gap-analysis artifact.
CV is the first downstream consumer added after; interview prep second. Build the trunk,
then the branches.

## D4 - Port via a three-bin sort

Each skill is ported through a quarantine step. Sort every line into: judgment (keep,
becomes step logic), orchestration (delete, the graph owns it), bloat (delete). Done
when every line is assigned. If a line is ambiguous between judgment and orchestration,
that ambiguity is the signal the original skill conflated the two.

## D5 - Step-boundary rule (seams)

A step earns standalone status only if it carries a seam:
- transforms state into a new shape (not merely persists a prior step's output),
- makes a routing / conditional-branch decision,
- gates on human review,
- fans out in parallel,
- is independently retryable.

A step with no seam folds into its neighbor (becomes that neighbor's final action). Any
step that brings prior work forward for the user to read and approve always stays
distinct - the human review is itself the seam.

## D6 - Name: candidacy

The unit of work is a single candidacy (one role, one application), not a career. The
career (inventory, profile, 25-year arc) is the input; a candidacy is the output. Each
application folder in the old repo is one candidacy: intake, fit, CV, prep, follow-up,
close.
