# 💊 Smart Store Agent using Gemini API via OpenAI Adapter
# 📁 File: product_suggester.py
# 👨‍💻 Author: Muhammad Hammad Zubair

import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

agent = Agent(
    name="Smart Store Agent",
    instructions="Suggest a medicine based on user symptoms with a short reason. Format: 🤖 Suggestion: [name]\n📌 Reason: [reason]",
    model=model
)

if __name__ == "__main__":
    print("🛒 Smart Store Agent is ready! Type your problem or 'exit' to quit.")
    while True:
        q = input("🗣️ You: ")
        if q.lower() in ["exit", "quit", "bye"]:
            print("👋 Goodbye!")
            break
        print(Runner.run_sync(agent, input=q, run_config=config).final_output)
