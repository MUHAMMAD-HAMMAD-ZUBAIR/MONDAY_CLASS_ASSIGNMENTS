import asyncio
from agents import Agent, RunConfig, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool
import os
from dotenv import load_dotenv

set_tracing_disabled(True)
load_dotenv()
api_key = os.getenv("API_KEY")

external_client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=external_client)
config = RunConfig(model=model, model_provider=external_client)

def lookup(data, key):
    return next((v for k, v in data.items() if k.lower() == key.lower()), None) or "Data not found."

def match_country(user_input):
    countries = ["Pakistan", "India", "USA", "France", "Japan"]
    user_input_lower = user_input.lower()
    for country in countries:
        if user_input_lower in country.lower():
            return country
    return None

@function_tool("get_capital")
def get_capital(country: str) -> str:
    return lookup({"Pakistan": "Islamabad", "India": "New Delhi", "USA": "Washington, D.C.", "France": "Paris", "Japan": "Tokyo"}, country)

@function_tool("get_language")
def get_language(country: str) -> str:
    return lookup({"Pakistan": "Urdu", "India": "Hindi", "USA": "English", "France": "French", "Japan": "Japanese"}, country)

@function_tool("get_population")
def get_population(country: str) -> str:
    return lookup({"Pakistan": "241 million", "India": "1.4 billion", "USA": "331 million", "France": "67 million", "Japan": "125 million"}, country)

async def main():
    agent = Agent(name="CountryInfoBot", instructions="If user gives a country name, return its capital, population, and language using tools.", tools=[get_capital, get_language, get_population], model=model)

    country_input = input("Enter a country name: ").strip()
    matched_country = match_country(country_input)

    if not matched_country:
        print("❌ Country not found in the list.")
        return

    prompt = f"Tell me the capital, language, and population of {matched_country}."
    result = await Runner.run(agent, prompt, run_config=config)

    print("\n🎯 Final Output:\n", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())



# # country_info_toolkit.py

# from agents import Agent, RunConfig, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool
# from openai.types.responses import ResponseTextDeltaEvent

# import asyncio
# from dotenv import load_dotenv
# import os

# # Step 1: Disable tracing
# set_tracing_disabled(disabled=True)

# # Step 2: Load API key
# load_dotenv()
# api_key = os.getenv("API_KEY")

# # Step 3: External OpenAI Client (Gemini compatible if needed)
# external_client = AsyncOpenAI(
#     api_key=api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# # Step 4: Model definition
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# # Step 5: Config setup
# config = RunConfig(
#     model=model,
#     model_provider=external_client,
 
# )
# @function_tool("get_capital")
# def get_capital(country: str) -> str:
#     print("cap called")
#     """
#     Return the capital city of the given country.

#     """
#     capitals = {
#         "Pakistan": "Islamabad",
#         "India": "New Delhi",
#         "USA": "Washington, D.C.",
#         "France": "Paris",
#         "Japan": "Tokyo"
#     }
#     return capitals.get(country, "Capital not found.")

# @function_tool("get_language")
# def get_language(country: str) -> str:
#     print("lang called")
#     """
#     Return the official language of the given country.

#     """
#     languages = {
#         "Pakistan": "Urdu",
#         "India": "Hindi",
#         "USA": "English",
#         "France": "French",
#         "Japan": "Japanese"
#     }
#     return languages.get(country, "Language not found.")

# @function_tool("get_population")
# def get_population(country: str) -> str:
#     print("pop called")
#     """
#     Return the approximate population of the given country.

#     """
#     populations = {
#         "Pakistan": "241 million",
#         "India": "1.4 billion",
#         "USA": "331 million",
#         "France": "67 million",
#         "Japan": "125 million"
#     }
#     return populations.get(country, "Population data not found.")


# # Step 7: Orchestrator Agent
# async def main():
#     orchestrator = Agent(
#         name="CountryInfoOrchestrator",
#         instructions="country info agent mgr jab koi pochy country population ya capital  to tools use kru",
#         # instructions="""
#         # # You are a Country Info Bot. When a user gives you a country name,
#         # # you must use the tools to find the capital, official language, and population,
#         # # and then give a complete report.
#         # # """,
#         tools=[get_capital, get_language, get_population],
#         model=model
#     )


#     user_message = input(" Enter a country name:")


    
#     result = await Runner.run( orchestrator, user_message, run_config=config)

#     print("🎯 Final Output:\n", result.final_output)

# asyncio.run(main())
