# 🤖 M.H.Z Console-Based Support Agent System  
**Built With:** [OpenAI Agents SDK – Console Edition]  
**👤 Author:** MUHAMMAD HAMMAD ZUBAIR

📌 **Here is complete assignment details**:
https://docs.google.com/document/d/1gZwuQuW5HTjNEVTfaGX56brdR5I0oj11/edit?usp=sharing&ouid=103459919058078389355&rtpof=true&sd=true  

📌 **Submission Link / Assignment Form**:  
https://forms.gle/1uwdntcc2CsjRRWe7

---

## 🎯 Assignment Objective & Details

You are required to implement a **Console-Based Support Agent System** using the **OpenAI Agents SDK (or a mock structured version)**, that:

- Routes user queries across **billing**, **technical**, and **general** categories  
- Uses **agent-to-agent handoffs** (e.g. triage agent handing off to specialized agents)  
- Implements **tools** per agent with **dynamic `is_enabled()` logic**  
- Passes **user context** (e.g. name, `is_premium_user`, `issue_type`) across agents  
- Operates entirely in **CLI** (Command-Line Interface), no GUI  
- *Bonus:* Includes **output guardrails** to avoid apologetic responses (e.g. “sorry”)  
- *Bonus:* Uses `stream_events()` to show tool execution steps  

> ✔️ *All requirements have been fully implemented* in this project.  
>&nbsp;

---

## ✅ Feature Compliance Table

| 📋 Requirement                    | ✅ Implemented | 🔍 Details |
|----------------------------------|----------------|-----------|
| **Agents (4 total)**             | ✅ Yes         | TriageAgent, BillingAgent, TechnicalAgent, GeneralAgent |
| **Tools per Agent**              | ✅ Yes         | Tools defined in `tools/` modules (billing_tools, technical_tools, general_tools) |
| **Dynamic `is_enabled()` Logic** | ✅ Yes         | `refund()` and `restart_service()` gated by `UserContext` |
| **Agent Handoff Logic**          | ✅ Yes         | Triage routes based on intent (refund, logs, general) |
| **Context Passing**              | ✅ Yes         | Context defined via Pydantic in `context_model.py` |
| **CLI Interface**                | ✅ Yes         | Built with `prompt_toolkit` & `rich` for a professional UI |
| **Guardrails (optional)**        | ✅ Yes         | `guardrails.py` filters “sorry”, “apologize”, etc |
| **Streaming (optional)**         | ✅ Yes         | Optional `stream_events()` simulation included |

---

## 🧠 How It Works: Components & Flow

### 1. 🧭 Gallery of Agents  
- **Triage Agent**: acts as dispatcher, detecting intent and handing off to the right agent  
- **Specialized Agents**:  
  - *Billing Agent* (handles refund, pay‑status)  
  - *Technical Agent* (handles logs, restart_service)  
  - *General Agent* (handles FAQ/general queries)  

The triage logic delegates the conversation based on detected intent and current context :contentReference[oaicite:1]{index=1}.

### 2. 🛠 Tools & `is_enabled()` Behavior  
- Billing Tools: `pay_status()`, `refund()` (refund only enabled for premium users)  
- Technical Tools: `check_logs()`, `restart_service()` (only if issue_type == 'technical')  
- General Tools: `faq_response()` available always  

### 3. 🧰 Context Modeling  
User context is captured using Pydantic in `context_model.py` with fields:  
`name: str`, `is_premium_user: bool`, `issue_type: str` — passed across all agents and tools :contentReference[oaicite:2]{index=2}.

### 4. 👥 Guardrails & Output Safety  
Implemented via `utils/guardrails.py`: any tool response containing “sorry”, “not allowed” or “apologize” is replaced with a professional fallback message.

### 5. 🖥 CLI Experience & Branding  
Built with `prompt_toolkit` for interactive input (history, clean prompt) and `rich` for colored panels, separators, and attractive visuals. Every output is labeled with **M.H.Z branded identity**, delivering a high-quality UI.

---

## 📁 Project Directory Structure

```
console_agent_project/
│
├── main.py                     # Entry point for the CLI system
├── context_model.py            # Pydantic-based user context
├── requirements.txt             # Install dependencies
│
├── agents/
│   ├── __init__.py
│   ├── triage_agent.py         # Dispatches queries based on intent
│   ├── billing_agent.py
│   ├── technical_agent.py
│   └── general_agent.py
│
├── tools/
│   ├── __init__.py
│   ├── billing_tools.py
│   ├── technical_tools.py
│   └── general_tools.py
│
└── utils/
    ├── __init__.py
    ├── intent_classifier.py    # Simplified NLP to detect intent
    └── guardrails.py           # Filters undesired apology phrases
```

---

## 🔧 Tool Gating Decision Table

| 🛠️ Tool              | ✅ Enable Condition                                  |
|----------------------|-----------------------------------------------------|
| `refund()`           | `context.is_premium_user == True`                  |
| `restart_service()`  | `context.issue_type == "technical"`                |
| `faq_response()`     | Enabled by default for general queries              |

---

## 🚀 Quick Start & Running Instructions

1. **Clone the repo or download ZIP**, ensure `main.py` is at project root.  
2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Launch**:
    ```bash
    python main.py
    ```
4. **Begin interacting**:
   - Enter your name, premium status, issue type.
   - Ask questions like “I want a refund” or “Restart service”, or say “exit” to end.

---

## 🎬 Sample Session

```
🔥 M.H.Z Intelligent Support Console
────────────────────────────────────
👤 Name: Hammad
💎 Premium user (yes/no): yes
❓ Issue type: technical

⚡ Query>>> My service is down
🤖 Routing to: Technical Agent
🛠️ Using Tool: restart_service()

📤 Output:
🔁 Service restarted successfully — M.H.Z Agents handles it!

⚡ Query>>> exit

✅ Thank you for using M.H.Z Agents. Goodbye!
```

---

## 📦 Dependencies (`requirements.txt`)

```txt
openai-agents>=0.1.18
pydantic>=2.0
prompt_toolkit>=3.0
rich>=13.0
```

---

## ✅ Assignment Completion Summary

- **All mandatory features** implemented ✅  
- **Bonus requirements** (guardrails, streaming) also included ✅  
- Clean, modular architecture with error handling and professional branding 💡  
- Ready for submission — works from root with `python main.py`

---

## 🙌 About the Author

**👨‍💻 Muhammad Hammad Zubair**  
Full-Stack Developer • AI Agent Enthusiast • Panaverse Student  
🔗 GitHub: https://github.com/MUHAMMAD‑HAMMAD‑ZUBAIR

---

