# # libraray.py  — M.H.Z Library Assistant (memory + follow-up + real LLM book writer)
# import os
# import re
# import asyncio
# from typing import Any, Dict, List, Optional
# from pydantic import BaseModel
# from difflib import get_close_matches
# from dotenv import load_dotenv
# from prompt_toolkit import prompt
# from prompt_toolkit.history import InMemoryHistory
# from rich.console import Console
# from rich.panel import Panel
# from rich.text import Text

# # Agents SDK imports (adjust if your local SDK exposes different names)
# from agents import (
#     Agent,
#     Runner,
#     function_tool,
#     input_guardrail,
#     GuardrailFunctionOutput,
#     InputGuardrailTripwireTriggered,
#     RunContextWrapper,
#     ModelSettings,
#     AsyncOpenAI,
#     OpenAIChatCompletionsModel,
#     RunConfig,
# )

# # ------------------ Windows asyncio fix ------------------
# if os.name == "nt":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# # ------------------ Load Gemini key ------------------
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise RuntimeError("GEMINI_API_KEY not found in .env")

# # ------------------ Setup Gemini client & models ------------------
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# # Model used for book writing / agent runs
# BASE_MODEL = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client,
# )

# GLOBAL_RUN_CONFIG = RunConfig(
#     model=BASE_MODEL,
#     model_provider=external_client,
#     tracing_disabled=True,
# )

# # ------------------ Local DB and context ------------------
# class UserContext(BaseModel):
#     name: str
#     member_id: Optional[str] = None
#     conversation_history: List[str] = []
#     last_book_requested: Optional[str] = None
#     pending_action: Optional[Dict[str, Any]] = None  # e.g., {"action":"generate","topic":"clean code"}

# # Local book DB (lowercase keys)
# BOOK_DB: Dict[str, int] = {
#     "clean code": 3,
#     "python crash course": 2,
#     "deep learning": 1,
#     "effective java": 2,
#     "learning python": 4,
# }
# MEMBERS_DB: Dict[str, str] = {
#     "1111": "Hammad",
#     "M002": "Sara",
#     "M003": "Bilal",
# }

# # ------------------ Guardrail (lenient) ------------------
# class LibraryGuardOutput(BaseModel):
#     is_library_question: bool
#     reason: str

# guardrail_agent = Agent(
#     name="LibraryTopicGuard",
#     instructions=(
#         "Return is_library_question True if the input is about books, library operations, "
#         "or requests to write/generate content about a topic. Be lenient."
#     ),
#     output_type=LibraryGuardOutput,
#     model=BASE_MODEL,
# )

# @input_guardrail
# async def library_input_guardrail(
#     ctx: RunContextWrapper[UserContext],
#     agent: Agent,
#     input: str | List[Any],
# ) -> GuardrailFunctionOutput:
#     # If we have a pending action in context, allow follow-ups (numbers etc.)
#     if getattr(ctx.context, "pending_action", None):
#         return GuardrailFunctionOutput(output_info=None, tripwire_triggered=False)

#     text = input if isinstance(input, str) else " ".join(input)
#     quick_keywords = ["book", "library", "available", "copies", "write", "generate", "summary", "chapter", "give me"]
#     if any(k in text.lower() for k in quick_keywords) or get_close_matches(text.lower(), BOOK_DB.keys(), n=1, cutoff=0.6):
#         return GuardrailFunctionOutput(output_info=None, tripwire_triggered=False)

#     # Otherwise consult LLM guardrail (kept minimal)
#     result = await Runner.run(guardrail_agent, text, context=ctx.context, run_config=GLOBAL_RUN_CONFIG)
#     return GuardrailFunctionOutput(output_info=result.final_output, tripwire_triggered=(not result.final_output.is_library_question))

# # ------------------ Local helper functions (no agent call needed) ------------------
# def list_books_local() -> str:
#     items = [f"{title.title()} ({copies} copies)" for title, copies in BOOK_DB.items()]
#     return "OK. I have the following books: " + ", ".join(items) + "."

# def search_books_local(q: str) -> str:
#     ql = q.lower().strip()
#     matches = [t.title() for t in BOOK_DB.keys() if ql in t]
#     if not matches:
#         close = get_close_matches(ql, BOOK_DB.keys(), n=5, cutoff=0.6)
#         matches = [t.title() for t in close]
#     if matches:
#         return f"I found: {', '.join(matches)}."
#     return f"I couldn't find any exact match for '{q}'. You can ask me to generate a full book on this topic."

# def availability_local(title: str, ctx: UserContext) -> str:
#     member_id = ctx.member_id
#     if not member_id or member_id not in MEMBERS_DB:
#         return "Not a registered member. Register to check availability."
#     close = get_close_matches(title.lower(), BOOK_DB.keys(), n=1, cutoff=0.6)
#     if not close:
#         return f"No copies found for '{title}'."
#     t = close[0]
#     return f"{t.title()} — {BOOK_DB.get(t,0)} copies available."

# # ------------------ Book writer helper (calls LLM via a small BookWriter agent) ------------------
# def generate_book_with_llm(topic: str, words: int = 10000) -> str:
#     """
#     Calls a BookWriter Agent via Runner.run (async) and returns markdown text.
#     Note: If the model cannot produce entire book in one response, model might return partials.
#     """
#     # Build a very explicit prompt asking for chunking if needed
#     prompt_text = (
#         f"You are an expert author. Write a complete, well-structured book about '{topic}'.\n"
#         f"Target length: approximately {words} words. If the model cannot produce the whole book in one response, "
#         "produce the book in sequential parts and mark them 'PART 1', 'PART 2', etc., continuing until the full length is reached.\n\n"
#         "Format strictly in Markdown. Include a title (H1), at least 10 chapters (H2), subheadings (H3), examples, short code blocks when relevant, emojis in section titles, a conclusion, and a FAQ.\n\n"
#         "Output ONLY the book markdown content, nothing else."
#     )

#     book_writer_agent = Agent(
#         name="BookWriter",
#         instructions="Follow the prompt exactly and output book markdown.",
#         model=BASE_MODEL,
#         model_settings=ModelSettings(temperature=0.25),
#     )

#     # Run agent synchronously via asyncio.run
#     run_result = asyncio.run(Runner.run(book_writer_agent, prompt_text, run_config=GLOBAL_RUN_CONFIG))
#     out = run_result.final_output
#     if isinstance(out, str):
#         return out
#     else:
#         return str(out)

# # ------------------ File utilities ------------------
# def sanitize_filename(s: str) -> str:
#     s = re.sub(r'[^A-Za-z0-9 _-]', '', s)
#     s = s.strip().replace(" ", "_")
#     return s[:120] or "book"

# def save_markdown(title: str, md: str) -> str:
#     fname = sanitize_filename(title) + ".md"
#     i = 1
#     base = fname
#     while os.path.exists(fname):
#         fname = f"{sanitize_filename(title)}_{i}.md"
#         i += 1
#     with open(fname, "w", encoding="utf-8") as f:
#         f.write(md)
#     return fname

# # ------------------ Command parser + intent detection ------------------
# def parse_input(user_input: str) -> Dict[str, Any]:
#     ui = user_input.strip() 
#     low = ui.lower()

#     if low in ("list books", "list", "books", "show books"):
#         return {"action":"list"}
#     if low.startswith(("do you have", "have you", "do you have a", "have")):
#         # extract quoted or remaining
#         m = re.search(r'["\'](.+?)["\']', ui)
#         if m:
#             title = m.group(1)
#         else:
#             # drop leading phrase
#             title = re.sub(r'^(do you have|have you|have|do you have a|is there)\s+', '', low, flags=re.I)
#         return {"action":"search","query": title}
#     if low.startswith(("check availability", "availability", "how many copies", "copies of")):
#         m = re.search(r'(?<=of ).+$', low)
#         if m:
#             title = m.group(0)
#         else:
#             title = ui
#         return {"action":"availability","query": title}
#     # generate/write request with optional params separated by ';'
#     if any(token in low for token in ("write me a book", "write a book", "write book", "generate book", "create book", "give me full book")) or low.startswith("write") or low.startswith("generate"):
#         return {"action":"generate", "query": ui}
#     # "show me book" fallback: user may expect last_book_requested
#     if low.startswith("show me book") or low.strip() == "show me book" or low.startswith("show me"):
#         return {"action":"show_last"}
#     # numeric-only (maybe follow-up word count)
#     if re.fullmatch(r'\d+', low):
#         return {"action":"number","value": int(low)}
#     # By default: treat as search/topic
#     return {"action":"search","query": ui}

# # ------------------ Console / UI ------------------
# console = Console()

# def preview_and_save_book(md_text: str, suggested_title: Optional[str] = None):
#     # Get title line if exists
#     lines = md_text.splitlines()
#     title_line = lines[0] if lines and lines[0].startswith("#") else (suggested_title or "Generated Book")
#     title_text = re.sub(r'^#+\s*', '', title_line).strip()
#     preview = "\n".join(lines[:40])  # first ~40 lines
#     console.print(Panel(preview if preview else md_text[:1000], title=f"📘 Preview: {title_text}", style="green"))
#     fname = save_markdown(title_text, md_text)
#     console.print(Panel(f"✅ Full book saved to [bold]{fname}[/]. Open the .md to read the full content.", style="bright_blue"))

# # ------------------ Main interactive loop ------------------
# def main():
#     console.print(Panel("📚 [bold cyan]M.H.Z Intelligent Library Assistant — Code Kings v2[/]", subtitle="Made by M.H.Z", style="bright_blue"))
#     name = prompt("👤 Name: ", history=InMemoryHistory()).strip() or "Guest"
#     member_id = prompt("🆔 Member ID (or leave empty if not registered): ", history=InMemoryHistory()).strip() or None
#     ctx = UserContext(name=name, member_id=member_id)

#     console.print("\n[bold green]💬 Type your library query below. (type 'exit' to quit)[/]")
#     console.print("[dim]Examples: 'list books', 'do you have Clean Code', 'check availability Deep Learning',")
#     console.print("[dim] 'write me a book on quantum computing; words=10000; style=beginner-friendly'[/]\n")

#     while True:
#         console.print("\n" + "-"*70, style="grey37")
#         user_input = prompt("⚡ Query>>> ", history=InMemoryHistory()).strip()
#         if not user_input:
#             continue
#         if user_input.lower() == "exit":
#             console.print(Panel("[bold magenta]✅ Thank you for using M.H.Z Library Assistant. Goodbye![/]", style="magenta"))
#             break

#         # Append to conversation history
#         ctx.conversation_history.append(user_input)

#         # If we have a pending_action and user entered a number or short param, handle locally before guardrail
#         if ctx.pending_action:
#             # Example: pending_action = {"action":"generate","topic":"Clean Code", "awaiting":"words"}
#             if ctx.pending_action.get("action") == "generate" and ctx.pending_action.get("awaiting") == "words":
#                 m = re.fullmatch(r'\d+', user_input.strip())
#                 if m:
#                     target_words = int(user_input.strip())
#                     ctx.pending_action.pop("awaiting", None)
#                     ctx.pending_action["words"] = target_words
#                     console.print(Text(f"🧠 Generating book on '{ctx.pending_action['topic']}' ({target_words} words)...", style="bold yellow"))
#                     # call LLM generator (synchronously via asyncio.run)
#                     try:
#                         md = generate_book_with_llm(ctx.pending_action["topic"], target_words)
#                         preview_and_save_book(md, suggested_title=ctx.pending_action["topic"])
#                         ctx.last_book_requested = ctx.pending_action["topic"]
#                         ctx.pending_action = None
#                     except Exception as e:
#                         console.print(Panel(f"[bold red]Error generating book: {e}[/]", style="red"))
#                     continue
#                 # if not numeric, fall through to normal parsing

#         # Normal parse
#         cmd = parse_input(user_input)

#         try:
#             # bypass guardrail if we are handling follow-up (we already handled above)
#             if cmd["action"] == "list":
#                 console.print(Panel(list_books_local(), title="📚 Library", style="green"))
#                 continue

#             if cmd["action"] == "search":
#                 out = search_books_local(cmd.get("query",""))
#                 # save last_book_requested if exact match
#                 q = cmd.get("query","")
#                 close = get_close_matches(q.lower(), BOOK_DB.keys(), n=1, cutoff=0.8)
#                 if close:
#                     ctx.last_book_requested = close[0]
#                 console.print(Panel(out, title="🔎 Search Result", style="green"))
#                 continue

#             if cmd["action"] == "availability":
#                 title = cmd.get("query","")
#                 out = availability_local(title, ctx)
#                 console.print(Panel(out, title="📦 Availability", style="green"))
#                 continue

#             if cmd["action"] == "show_last":
#                 if ctx.last_book_requested:
#                     # ask user whether they want summary or full book
#                     console.print(Panel(f"I have previously noted '{ctx.last_book_requested.title()}'. Do you want a summary or the full generated book? (reply: 'summary' or 'full' or give word count)", style="green"))
#                     # set pending action so next reply is handled
#                     ctx.pending_action = {"action":"generate", "topic": ctx.last_book_requested, "awaiting":"choice"}
#                     continue
#                 else:
#                     console.print(Panel("I don't have a previously requested book in this session. Tell me the topic.", style="yellow"))
#                     continue

#             if cmd["action"] == "number":
#                 # if user just typed a number without pending_action, treat as word target only if last_book_requested exists
#                 if ctx.pending_action and ctx.pending_action.get("action") == "generate" and ctx.pending_action.get("awaiting") in (None, "choice"):
#                     target = cmd["value"]
#                     topic = ctx.pending_action.get("topic") or ctx.last_book_requested
#                     if not topic:
#                         console.print(Panel("No topic available to generate a book for. Provide a topic.", style="red"))
#                         ctx.pending_action = None
#                         continue
#                     ctx.pending_action["words"] = target
#                     ctx.pending_action.pop("awaiting", None)
#                     console.print(Text(f"🧠 Generating book on '{topic}' ({target} words)...", style="bold yellow"))
#                     try:
#                         md = generate_book_with_llm(topic, target)
#                         preview_and_save_book(md, suggested_title=topic)
#                         ctx.last_book_requested = topic
#                         ctx.pending_action = None
#                     except Exception as e:
#                         console.print(Panel(f"[bold red]Error generating book: {e}[/]", style="red"))
#                     continue
#                 else:
#                     console.print(Panel("I received a number but I wasn't expecting it. If you want a book, ask 'write me a book on <topic>'.", style="yellow"))
#                     continue

#             if cmd["action"] == "generate":
#                 # parse the query for topic and optional params (words)
#                 raw = cmd.get("query","")
#                 # try to extract "on <topic>" or the remainder after "book"
#                 # also support "write me a book on quantum computing; words=10000; style=..."
#                 parts = [p.strip() for p in raw.split(";")]
#                 topic_part = parts[0]
#                 # try cleanup
#                 topic = re.sub(r'^(write me a book on|write me a book|write a book on|write a book|generate book on|generate book|create book on|give me full book about)\s*', '', topic_part, flags=re.I).strip()
#                 if not topic:
#                     console.print(Panel("Please tell me the topic, e.g., 'write me a book on quantum computing; words=10000'.", style="yellow"))
#                     # set pending expecting topic
#                     ctx.pending_action = {"action":"generate", "awaiting":"topic"}
#                     continue

#                 # look for words param
#                 words = None
#                 for p in parts[1:]:
#                     if "=" in p:
#                         k,v = p.split("=",1)
#                         if k.strip().lower() in ("words","word","wordcount","length"):
#                             try:
#                                 words = int(re.sub(r'\D','',v))
#                             except:
#                                 words = None

#                 if not words:
#                     # ask user for desired wordcount (store pending)
#                     console.print(Panel(f"How many words do you want for '{topic}'? Reply with a number (e.g. 5000). Default 10000 if you just press Enter.", style="green"))
#                     ctx.pending_action = {"action":"generate","topic": topic, "awaiting":"words"}
#                     continue

#                 # we have topic and words immediately — generate
#                 console.print(Text(f"🧠 Generating book on '{topic}' ({words} words)... This may take a while.", style="bold yellow"))
#                 try:
#                     md = generate_book_with_llm(topic, words)
#                     preview_and_save_book(md, suggested_title=topic)
#                     ctx.last_book_requested = topic
#                     ctx.pending_action = None
#                 except Exception as e:
#                     console.print(Panel(f"[bold red]Error generating book: {e}[/]", style="red"))
#                 continue

#             # Default fallback
#             console.print(Panel("Sorry, I didn't understand. Try: 'list books', 'do you have <title>', 'check availability <title>' or 'write me a book on <topic>; words=10000'", style="yellow"))

#         except InputGuardrailTripwireTriggered:
#             console.print(Panel("[bold red]❌ That doesn't look like a library request. Ask about books, availability, or request a generated book.[/]", style="red"))
#         except Exception as e:
#             console.print(Panel(f"[bold red]Unexpected error: {e}[/]", style="red"))

#     # end loop

# if __name__ == "__main__":
#     main()

# M.H.Z Intelligent Library Assistant v3 — Combined & Advanced
import os
import re
import asyncio
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from difflib import get_close_matches
from dotenv import load_dotenv
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from agents import (
    Agent,
    Runner,
    function_tool,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    ModelSettings,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
)

# ------------------ Windows asyncio fix ------------------
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ------------------ Load Gemini API Key ------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in .env file")

# ------------------ Setup LLM ------------------
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

BASE_MODEL = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

GLOBAL_RUN_CONFIG = RunConfig(
    model=BASE_MODEL,
    model_provider=external_client,
    tracing_disabled=True
)

# ------------------ Local DB & Context ------------------
class UserContext(BaseModel):
    name: str
    member_id: Optional[str] = None
    conversation_history: List[str] = []
    last_book_requested: Optional[str] = None
    pending_action: Optional[Dict[str, Any]] = None

BOOK_DB: Dict[str, int] = {
    "clean code": 3,
    "python crash course": 2,
    "deep learning": 1,
    "effective java": 2,
    "learning python": 4,
}
MEMBERS_DB: Dict[str, str] = {
"1111": "HAMMAD",
    "2222": "Anusha",
    "3333": "Sobia",
}

# ------------------ Guardrail ------------------
class LibraryGuardOutput(BaseModel):
    is_library_question: bool
    reason: str

guardrail_agent = Agent(
    name="LibraryTopicGuard",
    instructions=(
        "Return is_library_question True if input is about books, library operations, "
        "or requests to write/generate content about a topic. Be lenient."
    ),
    output_type=LibraryGuardOutput,
    model=BASE_MODEL
)

@input_guardrail
async def library_input_guardrail(
    ctx: RunContextWrapper[UserContext],
    agent: Agent,
    input: str | List[Any],
) -> GuardrailFunctionOutput:
    if getattr(ctx.context, "pending_action", None):
        return GuardrailFunctionOutput(output_info=None, tripwire_triggered=False)

    text = input if isinstance(input, str) else " ".join(input)
    keywords = ["book", "library", "available", "copies", "write", "generate", "summary", "chapter", "give me"]
    if any(k in text.lower() for k in keywords) or get_close_matches(text.lower(), BOOK_DB.keys(), n=1, cutoff=0.6):
        return GuardrailFunctionOutput(output_info=None, tripwire_triggered=False)

    result = await Runner.run(guardrail_agent, text, context=ctx.context, run_config=GLOBAL_RUN_CONFIG)
    return GuardrailFunctionOutput(output_info=result.final_output, tripwire_triggered=(not result.final_output.is_library_question))

# ------------------ Tools ------------------
@function_tool
def list_books(wrapper: RunContextWrapper[UserContext]) -> dict:
    return {"available_books": [{title.title(): copies} for title, copies in BOOK_DB.items()]}

@function_tool
def search_book(wrapper: RunContextWrapper[UserContext], query: str) -> dict:
    query_lower = query.lower()
    matches = [t.title() for t in BOOK_DB.keys() if query_lower in t]
    if not matches:
        close = get_close_matches(query_lower, BOOK_DB.keys(), n=3, cutoff=0.6)
        matches = [t.title() for t in close]
    return {"found": bool(matches), "matches": matches}

@function_tool
def check_availability(wrapper: RunContextWrapper[UserContext], title: str) -> dict:
    member_id = getattr(wrapper.context, "member_id", None)
    if not member_id or member_id not in MEMBERS_DB:
        return {"error": "Not a registered member. Register to check availability."}
    close = get_close_matches(title.lower(), BOOK_DB.keys(), n=1, cutoff=0.6)
    if not close:
        return {"title": title.title(), "copies": 0}
    title_match = close[0]
    copies = BOOK_DB.get(title_match, 0)
    return {"title": title_match.title(), "copies": copies}

@function_tool
def library_timings(wrapper: RunContextWrapper[UserContext]) -> str:
    return "Library timings: Mon-Fri 09:00-18:00, Sat 10:00-14:00, Sun Closed."

@function_tool
async def intelligent_book_search(wrapper: RunContextWrapper[UserContext], topic: str) -> dict:
    query_lower = topic.lower()
    matches = [t.title() for t in BOOK_DB.keys() if query_lower in t]
    if not matches:
        close = get_close_matches(query_lower, BOOK_DB.keys(), n=3, cutoff=0.6)
        matches = [t.title() for t in close]
    if matches:
        return {"source": "local", "matches": matches}

    prompt_text = f"Suggest 3 popular and useful books for learning about '{topic}'. Provide book titles and authors."
    result = await Runner.run(
        Agent(
            name="BookRecommender",
            instructions="You are a helpful AI that recommends books.",
            model=BASE_MODEL,
            model_settings=ModelSettings(temperature=0.7)
        ),
        prompt_text,
        run_config=GLOBAL_RUN_CONFIG
    )
    suggestions = result.final_output.strip()
    return {"source": "llm", "matches": suggestions.split("\n")}

# ------------------ Book Generator ------------------
def generate_book_with_llm(topic: str, words: int = 10000) -> str:
    prompt_text = (
        f"You are an expert author. Write a complete, well-structured book about '{topic}'. "
        f"Target length: approximately {words} words. "
        "Format in Markdown with chapters, examples, short code blocks, conclusion, FAQ, and emojis."
    )

    book_writer_agent = Agent(
        name="BookWriter",
        instructions="Follow the prompt exactly and output book markdown.",
        model=BASE_MODEL,
        model_settings=ModelSettings(temperature=0.25)
    )
    run_result = asyncio.run(Runner.run(book_writer_agent, prompt_text, run_config=GLOBAL_RUN_CONFIG))
    out = run_result.final_output
    return str(out) if isinstance(out, str) else ""

# ------------------ File Utilities ------------------
def sanitize_filename(s: str) -> str:
    s = re.sub(r'[^A-Za-z0-9 _-]', '', s)
    s = s.strip().replace(" ", "_")
    return s[:120] or "book"

def save_markdown(title: str, md: str) -> str:
    fname = sanitize_filename(title) + ".md"
    i = 1
    base = fname
    while os.path.exists(fname):
        fname = f"{sanitize_filename(title)}_{i}.md"
        i += 1
    with open(fname, "w", encoding="utf-8") as f:
        f.write(md)
    return fname

def preview_and_save_book(md_text: str, suggested_title: Optional[str] = None):
    lines = md_text.splitlines()
    title_line = lines[0] if lines and lines[0].startswith("#") else (suggested_title or "Generated Book")
    title_text = re.sub(r'^#+\s*', '', title_line).strip()
    preview = "\n".join(lines[:40])
    console.print(Panel(preview if preview else md_text[:1000], title=f"📘 Preview: {title_text}", style="green"))
    fname = save_markdown(title_text, md_text)
    console.print(Panel(f"✅ Full book saved to [bold]{fname}[/].", style="bright_blue"))

# ------------------ Dynamic Instructions ------------------
def dynamic_instructions(context: RunContextWrapper[UserContext], agent: Agent) -> str:
    name = getattr(context.context, "name", "Guest")
    return (
        f"You are a helpful library assistant for {name}. "
        "You can: search books, check availability, list all books, provide timings, "
        "or generate full books on request."
    )

# ------------------ Main Agent ------------------
library_agent = Agent[UserContext](
    name="MHZLibraryAssistant",
    instructions=dynamic_instructions,
    tools=[list_books, search_book, check_availability, library_timings, intelligent_book_search],
    output_type=dict,
    model=BASE_MODEL,
)

# ------------------ CLI ------------------
console = Console()

def parse_input(user_input: str) -> Dict[str, Any]:
    ui = user_input.strip()
    low = ui.lower()

    if low in ("list books", "list", "books", "show books"):
        return {"action": "list"}
    if low.startswith(("do you have", "have you", "have")):
        m = re.search(r'["\'](.+?)["\']', ui)
        title = m.group(1) if m else re.sub(r'^(do you have|have you|have|do you have a|is there)\s+', '', low, flags=re.I)
        return {"action": "search", "query": title}
    if low.startswith(("check availability", "availability", "how many copies", "copies of")):
        m = re.search(r'(?<=of ).+$', low)
        title = m.group(0) if m else ui
        return {"action": "availability", "query": title}
    if any(token in low for token in ("write me a book", "write a book", "generate book", "create book", "give me full book")) or low.startswith(("write","generate")):
        return {"action": "generate", "query": ui}
    if low.startswith("show me book") or low.strip() == "show me book" or low.startswith("show me"):
        return {"action": "show_last"}
    if re.fullmatch(r'\d+', low):
        return {"action": "number","value": int(low)}
    return {"action":"search","query": ui}

# ------------------ Main Loop ------------------
def main():
    console.print(Panel("📚 [bold cyan]M.H.Z Intelligent Library Assistant v3 — Code Kings[/]", subtitle="Made by M.H.Z", style="bright_blue"))
    name = prompt("👤 Name: ", history=InMemoryHistory()).strip() or "Guest"
    member_id = prompt("🆔 Member ID (or leave empty if not registered): ", history=InMemoryHistory()).strip() or None
    ctx = UserContext(name=name, member_id=member_id)

    console.print("\n[bold green]💬 Type your query (type 'exit' to quit)[/]")
    console.print("[dim]Examples: 'list books', 'do you have Clean Code', 'check availability Deep Learning',")
    console.print("[dim] 'write me a book on quantum computing; words=10000'[/]\n")

    while True:
        console.print("\n" + "-"*70, style="grey37")
        user_input = prompt("⚡ Query>>> ", history=InMemoryHistory()).strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            console.print(Panel("[bold magenta]✅ Thank you for using M.H.Z Library Assistant. Goodbye![/]", style="magenta"))
            break

        ctx.conversation_history.append(user_input)

        # Handle follow-up pending actions
        if ctx.pending_action:
            if ctx.pending_action.get("action") == "generate" and ctx.pending_action.get("awaiting") == "words":
                if user_input.isdigit():
                    words = int(user_input)
                    topic = ctx.pending_action.get("topic")
                    console.print(Text(f"🧠 Generating book on '{topic}' ({words} words)...", style="bold yellow"))
                    try:
                        md = generate_book_with_llm(topic, words)
                        preview_and_save_book(md, suggested_title=topic)
                        ctx.last_book_requested = topic
                        ctx.pending_action = None
                    except Exception as e:
                        console.print(Panel(f"[bold red]Error generating book: {e}[/]", style="red"))
                    continue

        cmd = parse_input(user_input)
        try:
            if cmd["action"] == "list":
                console.print(Panel(list_books_local(), title="📚 Library", style="green"))
            elif cmd["action"] == "search":
                console.print(Panel(search_books_local(cmd.get("query","")), title="🔎 Search Result", style="green"))
            elif cmd["action"] == "availability":
                console.print(Panel(availability_local(cmd.get("query",""), ctx), title="📦 Availability", style="green"))
            elif cmd["action"] == "generate":
                topic = cmd.get("query","")
                console.print(Text(f"🧠 Generating book on '{topic}' (default 10000 words)...", style="bold yellow"))
                md = generate_book_with_llm(topic, 10000)
                preview_and_save_book(md, suggested_title=topic)
            else:
                console.print(Panel("❌ Command not recognized. Try 'list books', 'do you have <title>', 'check availability <title>', or 'write me a book on <topic>'", style="yellow"))

        except InputGuardrailTripwireTriggered:
            console.print(Panel("[bold red]❌ That doesn't look like a library request. Ask about books or generate a book.[/]", style="red"))
        except Exception as e:
            console.print(Panel(f"[bold red]Unexpected error: {e}[/]", style="red"))

# ------------------ Local Helper Functions ------------------
def list_books_local() -> str:
    return "OK. I have the following books: " + ", ".join([f"{title.title()} ({copies} copies)" for title, copies in BOOK_DB.items()]) + "."

def search_books_local(q: str) -> str:
    ql = q.lower().strip()
    matches = [t.title() for t in BOOK_DB.keys() if ql in t]
    if not matches:
        close = get_close_matches(ql, BOOK_DB.keys(), n=5, cutoff=0.6)
        matches = [t.title() for t in close]
    return f"I found: {', '.join(matches)}." if matches else f"No exact match for '{q}'. You can ask me to generate a full book."

def availability_local(title: str, ctx: UserContext) -> str:
    member_id = ctx.member_id
    if not member_id or member_id not in MEMBERS_DB:
        return "Not a registered member. Register to check availability."
    close = get_close_matches(title.lower(), BOOK_DB.keys(), n=1, cutoff=0.6)
    if not close:
        return f"No copies found for '{title}'."
    t = close[0]
    return f"{t.title()} — {BOOK_DB.get(t,0)} copies available."

# ------------------ Run ------------------
if __name__ == "__main__":
    main()
