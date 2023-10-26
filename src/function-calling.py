import os
import json

import openai
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
# from langchain.chat_models import AzureChatOpenAI
from langchain.chat_models import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "xxx"

def get_current_weather(location, unit="fahrenheit"):
  """Get the current weather of the location."""
  weather_info = {
    "location": location,
    "temperature": 72,
    "unit": unit,
    "forecast": ["sunny", "windy"]
  }
  return json.dumps(weather_info)

tools = [
 Tool(
  name="get_current_weather",
  func=get_current_weather,
  description="Get the current weather of the location.",
 ) 
]

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS)

result = agent.run("What is the weather in Boston?")
print(result)
