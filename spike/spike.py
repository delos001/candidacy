"""
Description: This script will contain variety of basic langgraph commands to
support learning

Date: 2026-21-07
Author: Jason Delosh
"""

##############################################################################
### Load Libraries
##############################################################################

from typing import TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

##############################################################################
### Configuration
##############################################################################
"""
Loads thh API key from spike/.env and builds the Claude client once so the node
can reuse it on every call intstead of rebuilding each time
"""

load_dotenv("spike/.env")  # put the anthropic api key into the env
llm = ChatAnthropic(model="claude-haiku-4-5", max_tokens=60)


##############################################################################
# ==> Section: State
##############################################################################
"""
A class is a blue print to define things that bundle data and actions together
- different than dict in that a class can define actions (methods)
"""


class State(TypedDict):
    """Defines the blueprint for the shape of the notepad.
    - the fields and the field spcs (ie: role: string) and each step will add to the it.
    - every node recieves (reads) and writes back to it so the graph needs an
        agreed upon shape: State is that single source of truth
    - TypedDict: langgraph notepad is a Python dictionary (key/value pairs) so TypedDict
        is a way to describe the keys and values for the graph to understand
    """

    role: str
    notes: list[str]
    fit: str  # the verdict a later node writes: 'ready' or 'gaps'
    attempts: int  # loop guard: how many times draft has run
    qc_result: str  # QC verdict on the draft: 'pass' or 'fail'
    summary: str  # a blank space for claude's reply to go into


##############################################################################
# ==> Section: Nodes
##############################################################################
"""
A node is a function that recieves the notepad and returns a small update to it.
Every node has the same shape
Langgraph takes a returned dict adn merges it onto the notepad
"""


# --> Node (intake)
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


# --> Node (retrieve)
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


# --> Node (gap_check)
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


# --> Router (from gap_check)
def route_after_gap_check(state: State):
    """the router reads the state['fit'] and the verdict that the gap_check
    node wrote and executes a fork to send the notepad to the approrpiate branch
    (draft or flag_gaps)
    It doesn't modify the notepad; it just points to next node
    """
    if state["fit"] == "ready":
        return "draft"
    else:
        return "flag_gaps"


# --> Node (Fork Destination1 from route_after_gap_check)
def draft(state: State):  # verdict is 'ready'
    """
    draft is the recipient from the fork if verdit is 'ready'
    -It appends a line to the log saying it is ready to proceed.
    """
    return {"notes": state["notes"] + ["draft: wrote a first pass"]}


# --> Fork Destination2 (from route_after_gap_check)
def flag_gaps(state: State):
    """
    -flag_gaps recipient from the fork if verdit is 'gaps'
    -It appends a line to the log saying logged missing skills.
    """
    return {"notes": state["notes"] + ["flag_gaps: logged missing skills"]}


# --> Node (qc)
def qc(state: State):
    """
    Judges the draft, bumps the attempt counter, writes a pass/fail verdict.
    Contrived rule: fail the first attempt, pass the second so the loop runs once.
    """
    attempt = state["attempts"] + 1
    verdict = "pass" if attempt >= 2 else "fail"
    return {
        "notes": state["notes"] + ["qc: attempt" + str(attempt) + " -> " + verdict],
        "attempts": attempt,
        "qc_result": verdict,
    }


# --> Router (from qc)
def route_after_qc(state: State):
    """
    Reads the QC verdict and the attempt count, then routes based on verdict:
    - pass -> move on (END)
    - fail but out of attempts -> give up, move on (END)
    - fail and atempts remain -> go BACK to draft (a cycle)
    """
    if state["qc_result"] == "pass":
        return "done"
    elif state["attempts"] >= 3:
        return "done"
    else:
        return "draft"


# --> Node (subagent 1)
def subagent(state: State):
    """
    Delegates a small sub-task to a real LLM: ask claude for a one-line pitch.
    This is the only node that reaches over the network to Claude (spends API credit)
    """
    prompt = "In one sentence, pitch a candidate for this role: " + state["role"]
    reply = llm.invoke(prompt).content
    return {
        "notes": state["notes"] + ["subagent: Claude said -> " + reply],
        "summary": reply,
    }


# --> Node (human review)
def human_review(state: State):
    """
    Pauses teh run and waits for a human decision on LLMs output or response.
    interrupt() stops the graph here and hands its payload back to the caller;
    whatever values you resume with becomes 'decision'.
    """
    decision = interrupt({"pitch": state["summary"], "ask": "approve or revise?"})
    return {"notes": state["notes"] + ["human_review: human said " + decision]}


##############################################################################
# ==> Section: Graph Assembly
##############################################################################

"""
Builder defines the shape of the notepad (but it has no nodes yet)
Once the builder is created, the nodes can be added and defined
"""
builder = StateGraph(State)

## add nodes and label them as string label
builder.add_node("intake", intake)
builder.add_node("retrieve", retrieve)
builder.add_node("gap_check", gap_check)
builder.add_node("draft", draft)
builder.add_node("flag_gaps", flag_gaps)
builder.add_node("qc", qc)
builder.add_node("subagent", subagent)
builder.add_node("human_review", human_review)


# --> Edge Assembly
"""
create the arrows to connect the nodes together.
START and END are special labels that represent the beginning and end of the graph.
The arrows are directed, so the order matters.
"""

builder.add_edge(START, "intake")  # when program starts, go to intake first
builder.add_edge("intake", "retrieve")  # after intake finishes, go to retrieve
builder.add_edge("retrieve", "gap_check")  # after retrieve finishes, gap_check


builder.add_conditional_edges(  # conditional edges (foks from a node)
    "gap_check",
    route_after_gap_check,  # gets 'draft' or 'flag_gaps' from the node
    {"draft": "draft", "flag_gaps": "flag_gaps"},  # for png creation to show the forks
)  # calls the router node

builder.add_edge("draft", "qc")
builder.add_conditional_edges(
    "qc",
    route_after_qc,  # gets pass/fail from the node
    {"draft": "draft", "done": "subagent"},  # 'draft' = the cycle back; 'done' = stop
)

builder.add_edge("flag_gaps", END)
builder.add_edge("subagent", "human_review")
builder.add_edge("human_review", END)


##############################################################################
# ==> Compile and Run
##############################################################################

"""
compile takes finished blueprint from builder and produces the actual run-able
program that is stored as 'graph' variable
'graph' is for running assembled nodes and edges
"""

graph = builder.compile(checkpointer=MemorySaver())  # use memorysaver stores state in RAM


config = {"configurable": {"thread_id": "run-1"}}

# first invoke:
# - starts program with fresh notepad and sets values for each field in state
# -runs until the human_reivew interrupt, then pauses
# - returns final notepad (state) as final
state = graph.invoke(
    {
        "role": "Engineer",
        "notes": [],
        "fit": "",
        "attempts": 0,
        "qc_result": "",
        "summary": "",
    },
    config,
)

print("--- paused, waiting for human ---")
print(state["__interrupt__"])  # payload human review handed back

# Resume: send the human's decision back into the interrupt
final = graph.invoke(Command(resume="approve"), config)

print("--- resumed and finished ---")
for line in final["notes"]:  # loops walks notepad, prints each line on its own row
    print(line)


##############################################################################
# ==> Section: Print Graph
##############################################################################

##obsolete (uses grandalf and produces low quality graph)
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
