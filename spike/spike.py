"""
Description: This script will contain variety of basic langgraph commands to
support learning

Date: 2026-21-07
Author: Jason Delosh
"""

##################################
### Loading the necessary libraries
##################################

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

##################################
### Define Classes
##################################


class State(TypedDict):
    """Shared notepad: one input filed (roles) and a running log (notes) that
    each step will add to."""

    role: str
    notes: list[str]
    fit: str  # the verdict a later node writes: 'ready' or 'gaps'


##################################
### Define the Nodes
##################################


def intake(state: State):
    """
    defines a node (junction) that receives whole notepad as state and appends one
    line to the log saying it saw the role
    """
    return {"notes": state["notes"] + ["intake: received role " + state["role"]]}
    # reads current list of notes;
    # + ["..."] glues new line to existing 'notes' list
    # hands back only the field it changed.
    # Langraph merges that onto the notepad


def retrieve(state: State):
    """
    defines a node (junction) that receives whole notepad as state and appends one
    line to the log saying it saw the role
    """
    return {"notes": state["notes"] + ["retrieve: pulled matching experience"]}
    # reads current list of notes;
    # + ['intake:...] glues string to existing 'notes' list
    # hands back only the field it changed.
    # Langraph merges that onto the notepad


def gap_check(state: State):
    """defines a node to produce a verdit to route to next node.
    in this example: if role is Engineer, verdict is 'ready', else 'gaps'
    """
    verdict = "ready" if "Engineer" in state["role"] else "gaps"
    # checks if the role is as needed and produces verdict 'ready' or 'gaps' along with
    # notes to the log.
    return {
        "notes": state["notes"] + ["gap_check: verdict = " + verdict],
        "fit": verdict,  # The verdict is stored in the notepad as 'fit' field.
    }


"""
Two receipt nodes from the gap_check node, depending on the verdict.
Only a fork will chose between them instead of running both.
-draft is the recipient if verdit is ready
-flag_gaps is the recipient if verdit is gaps
-It appends a line to the log saying it is ready to proceed or logged missing skills.
"""


def draft(state: State):  # verdict is 'ready'
    return {"notes": state["notes"] + ["draft: wrote a first pass"]}


def flag_gaps(state: State):  # verdict is 'gaps'
    return {"notes": state["notes"] + ["flag_gaps: logged missing skills"]}


##################################
## Define the Router (Decision Maker)
##################################

"""
Decision maker node: returns a string (not notepade update) that names the next
node to run. The string must match the name of a node in the graph.
In this example: the router reads the state['fit'] and the verdict that the gap_check
node wrote and picks the approrpiate branch (draft or flag_gaps)
It doesn't modify the notepad; it just points to next node
"""


def route_after_gap_check(state: State):
    if state["fit"] == "ready":
        return "draft"
    else:
        return "flag_gaps"


##################################
## Add nodes to the graph
##################################

"""
Create the graph builder: knows the shape of the notepad but has no nodes yet
"""
builder = StateGraph(State)

## add nodes and label them as string label
builder.add_node("intake", intake)
builder.add_node("retrieve", retrieve)
builder.add_node("gap_check", gap_check)
builder.add_node("draft", draft)
builder.add_node("flag_gaps", flag_gaps)

##################################
## Add edges to the graph
##################################
"""
create the arrows to connect the nodes together. START and END are special labels
that represent the beginning and end of the graph. The arrows are directed, so the
order matters.
'builder' is for assembling nodes and edges
"""
builder.add_edge(START, "intake")  # when program starts, go to intake first
builder.add_edge("intake", "retrieve")  # after intake finishes, go to retrieve
builder.add_edge("retrieve", "gap_check")  # after retrieve finishes, gap_check

## conditional edges (foks from a node)
## in this example it calls the router node (route_after_gap_check) and that router
## returns either 'draft' or 'flag_gaps'
builder.add_conditional_edges(
    "gap_check",
    route_after_gap_check,
    {"draft": "draft", "flag_gaps": "flag_gaps"},  # for png creation to show the forks
)  # calls the router node

## whichever branch the fork choses, that node runs and the program stops
builder.add_edge("draft", END)
builder.add_edge("flag_gaps", END)


##################################
## Compile the graph and run it
##################################

"""
compile takes finished blueprint from builder and produces the actual runnable
program that is stored as 'grap' variable
'graph' is for running assembled nodes and edges
"""
graph = builder.compile()

result = graph.invoke({"role": "Product Manager", "notes": [], "fit": ""})
# starts program with fresh notepad (notes starts empty) and
# role set to Data Engineer
# runs intake then retrieve, and returns the final notepad (state) as 'result'
for line in result["notes"]:
    # loops walks the notes list and prints each line on its own row so log is readable
    print(line)


##################################
## Print ASCII Diagram
##################################

## obsolete (uses grandalf and produces low quality graph)
##print(graph.get_graph().draw_ascii())

mermaid_text = graph.get_graph().draw_mermaid()  # returns graph as mermaid text string
with open("spike/graph.mmd", "w") as f:  # creat file to write into
    f.write(mermaid_text)  # puts text in it
##print(mermaid_text)  # also dumps to terminal so it can be seen immediately

try:  # try/except used to handle failures possible from reaching ouver network to render
    png_bytes = graph.get_graph().draw_mermaid_png()  # render diagram into PNG image
    with open("spike/graph.png", "wb") as f:  # writes to spike/graph.png (write binary)
        f.write(png_bytes)
    print("Wrote spike/graph.png")

except Exception as e:
    print("PNG render failed, but graph.mmd is fine:", e)
