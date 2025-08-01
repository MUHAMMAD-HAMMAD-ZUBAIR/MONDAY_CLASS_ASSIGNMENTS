
# 🤖 Agentic SDK Assignments – MUHAMMAD HAMMAD ZUBAIR

This repository contains 3 intelligent agents built using the `agents` library and **Gemini 2.0 Flash** via OpenAI-compatible wrapper.

These assignments demonstrate core concepts from the **Agentic SDK**, including:
- Agent creation
- Tool usage
- Handoff workflows
- Multi-agent orchestration

## 🧠 Requirements

- Python 3.10+
- `agents` SDK (latest)
- `.env` file with your `GEMINI_API_KEY`
- Internet access to call the Gemini API

Install dependencies:

```bash
pip install -r requirements.txt
````

Create a `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 1️⃣ Smart Store Agent

📁 `product_suggester.py`

Suggests a medicine based on user symptoms using natural language.

### 🧪 Example

```
🗣️ You: I have a headache
🤖 Suggestion: Panadol
📌 Reason: It is commonly used for relieving headaches and mild pain.
```

### 📌 Highlights

* Uses a single `Agent` with instruction-based reasoning.
* Model: `gemini-2.0-flash`
* Simple conversation loop.

---

## 2️⃣ Mood Analyzer with Handoff

📁 `mood_handoff.py`

Detects user mood and hands off to a second agent if emotional support is needed.

### 🧪 Example

```
🗣️ You: I'm feeling really down and tired.
🔍 Detected Mood: sad
🧘 Suggested Activity: Take a short walk outside.
💬 Note: Fresh air and sunlight can lift your mood. You're doing great!
```

### 📌 Highlights

* Two agents:

  * `Mood Detector` (classifies emotion)
  * `Uplift Buddy` (suggests activity)
* Demonstrates **Agent Handoff** via `Runner.run_sync`.

---

## 3️⃣ Country Info Bot (with Tools)

📁 `country_info_toolkit.py`

Combines 3 tool agents to fetch capital, language, and population of any country. Uses a main orchestrator agent to present the info.

### 🧪 Example

```
Enter country name: Pakistan

📘 Country Info Summary:

The capital of Pakistan is Islamabad, the language is Urdu, and the population is 241 million.
```

### 📌 Highlights

* 3 Tool Agents:

  * `Capital Finder`
  * `Language Finder`
  * `Population Finder`
* 1 Orchestrator Agent
* Demonstrates **Tool usage and orchestration**

---

## 🛠 Technologies Used

* [Gemini 2.0 Flash](https://ai.google.dev/)
* [Agentic SDK](https://pypi.org/project/openai-agents/)
* Python 3.10+
* `.env` with API keys

---

## 📂 Folder Structure

```
📁 assignments/
├── .env
├── product_suggester.py
├── mood_handoff.py
├── country_info_toolkit.py
└── README.md
```

---


## ✅ Submission Info

These assignments are part of the Agentic SDK module in the Panaverse AI Agent Engineering Course.

Submit here: [Assignment Submission Form](https://forms.gle/tu5aubQMg4uM1f1w9)

---

## 🚀 Bonus Tip

You can run each file individually from terminal:

```bash
python product_suggester.py
python mood_handoff.py
python country_info_toolkit.py
```

---

## ⭐ Final Note

This project was made with 💙 using **Google Gemini**, not OpenAI, by configuring the SDK via a custom base URL.


## 👨‍🏫 Author

**MUHAMMAD HAMMAD ZUBAIR**
