
# 📚 M.H.Z Intelligent Library Assistant  
**Built With:** [OpenAI Agents SDK – Gemini Edition]  
**👤 Author:** MUHAMMAD HAMMAD ZUBAIR

📌 **Submission Link / Assignment Form:**  
https://forms.gle/PaJHC5qMNQE2VjyK9](https://forms.gle/PaJHC5qMNQE2VjyK9

---

## 🎯 Assignment Objective & Requirements

Develop a **Console-Based AI Library Assistant** using **OpenAI Agents SDK / Gemini AI**, that:  

- Responds to user queries about **books, availability, library timings**  
- Uses **dynamic instructions** personalized per user  
- Implements **tools** for searching, listing, checking availability, and intelligent recommendations  
- Handles **registered vs non-registered members**  
- Includes **input guardrails** to block non-library queries  
- Operates entirely in **CLI (Command Line Interface)**  
- Provides **intelligent suggestions using Gemini AI** if books are not in local DB  
- Supports **fuzzy matching** for book searches  

> ✔️ *All mandatory and optional requirements are implemented.*

---

## ✅ Feature Compliance Table

| 📋 Requirement                     | ✅ Implemented | 🔍 Details |
|-----------------------------------|----------------|-----------|
| **Agent Architecture**            | ✅ Yes         | Single `LibraryAssistant` agent with multiple tools |
| **Function Tools**                 | ✅ Yes         | `list_books`, `search_book`, `check_availability`, `library_timings`, `intelligent_book_search` |
| **Dynamic Instructions**           | ✅ Yes         | Personalized messages using user name |
| **Input Guardrail**                | ✅ Yes         | Blocks non-library queries with clear error messages |
| **Member Validation**              | ✅ Yes         | Availability only for registered members |
| **Fuzzy Search**                   | ✅ Yes         | `difflib.get_close_matches` used for approximate matches |
| **Intelligent Book Suggestions**   | ✅ Yes         | Uses Gemini AI for books not in DB |
| **CLI Interface**                  | ✅ Yes         | `prompt_toolkit` + `rich` panels for interactive UI |
| **Async Safe for Windows**         | ✅ Yes         | `WindowsSelectorEventLoopPolicy` used |
| **Testing**                        | ✅ Yes         | `test_agent.py` runs 3 predefined queries |

---

## 🧠 How It Works: Components & Flow

### 1. 🧭 Agent & Guardrails  
- **LibraryAssistant Agent** is the main AI agent  
- **Input Guardrail** validates user query:  
  - Only allows library-related keywords (`book`, `kitab`, `library`, `timing`, `available`, `copies`)  
  - Uses `LibraryTopicGuard` agent for uncertain queries  

### 2. 🛠 Tools / Functionality  

| Tool | Description |
|------|-------------|
| `list_books` | Lists all available books and copies |
| `search_book(query)` | Searches book locally with fuzzy matching |
| `check_availability(title)` | Shows available copies for registered members |
| `library_timings` | Shows library schedule |
| `intelligent_book_search(topic)` | Suggests books via Gemini AI if not found locally |

### 3. 📦 Databases  
- `BOOK_DB`: Stores book titles and copies  
- `MEMBERS_DB`: Stores registered members  

```python
BOOK_DB = {
    "clean code": 3,
    "python crash course": 2,
    "deep learning": 1,
    "effective java": 2,
    "learning python": 4,
}

MEMBERS_DB = {
    "1111": "HAMMAD",
    "2222": "Anusha",
    "3333": "Sobia",
}
````

### 4. 🖥 CLI Flow & Branding

* Uses `prompt_toolkit` for input and history
* `rich` panels for visually appealing output
* Example session:

```
📚 M.H.Z Intelligent Library Assistant
👤 Name: HAMMAD
🆔 Member ID: 1111

⚡ Query>>> list books
🤖 Agent Reply:
- Clean Code: 3 copies
- Python Crash Course: 2 copies
- Deep Learning: 1 copy
- Effective Java: 2 copies
- Learning Python: 4 copies

⚡ Query>>> check availability Clean Code
🤖 Agent Reply: Title: Clean Code, Copies: 3

⚡ Query>>> Advanced Python suggestions
🤖 Agent Reply: Not found locally. Suggested by AI:
1. Advanced Python Programming by Jane Smith
2. Python Mastery by John Doe
3. Python Tricks by Dan Bader

⚡ Query>>> library timings
🤖 Agent Reply: Library timings: Mon-Fri 09:00-18:00, Sat 10:00-14:00, Sun Closed.
```

---

## 🔧 Tool Gating & Member Validation

* `check_availability()` only works for **registered members**
* If member ID invalid → error message:

```
❌ Not a registered member. Register to check availability.
```

* Fuzzy match ensures near-title queries are handled gracefully

---

## 🚀 Running the Project

1. Clone the repo:

```bash
git clone https://github.com/yourusername/MHZ_Intelligent_Library.git
cd MHZ_Intelligent_Library
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add `.env` file:

```
GEMINI_API_KEY="your_gemini_api_key_here"
```

4. Run the main CLI:

```bash
python main_libraray.py
```

5. Run automated tests:

```bash
python test_agent.py
```

---

## 📁 Project Directory Structure

```
MHZ_Intelligent_Library/
│
├── main_libraray.py        # Main CLI agent
├── test_agent.py           # Test queries
├── .env                    # API Key
├── requirements.txt
└── README.md
```

---

## 📦 Dependencies (`requirements.txt`)

```
agents
pydantic>=2.0
python-dotenv
prompt_toolkit>=3.0
rich>=13.0
nest_asyncio
```

---

## ✅ Assignment Completion Summary

* **All requirements implemented:** search, availability, timings, guardrails ✅
* **Fuzzy matching & intelligent AI suggestions** ✅
* **CLI interface with branded outputs** ✅
* **Async-safe for Windows & Linux** ✅
* Ready for submission using provided Google Form

---

## 🙌 About the Author

**👨‍💻 MUHAMMAD HAMMAD ZUBAIR**
Full-Stack Developer • AI Agent Enthusiast • GIAIC Student
🔗 GitHub: [https://github.com/MUHAMMAD-HAMMAD-ZUBAIR](https://github.com/MUHAMMAD-HAMMAD-ZUBAIR)

```


