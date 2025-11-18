from smolagents import CodeAgent,DuckDuckGoSearchTool, HfApiModel,load_tool,tool
import datetime
import requests
import pytz
import yaml
from tools.final_answer import FinalAnswerTool

from Gradio_UI import GradioUI

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def get_weather(city: str) -> str:
    """Fetches the current weather information for a specified city
        args:
                city: the name of the  city
    """
    
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]

            weather_info = f"""
Weather in {city}:
- Temperature: {current['temp_C']}°C ({current['temp_F']}°F)
- Condition: {current['weatherDesc'][0]['value']}
- Humidity: {current['humidity']}%
- Wind Speed: {current['windspeedKmph']} km/h
- Feels Like: {current['FeelsLikeC']}°C
"""
            return weather_info.strip()
        else:
            return f"Could not find the weather for {city}"
    except Exception as e:
        return f"Error fetching weather: {str(e)}" 

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"



final_answer = FinalAnswerTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

model = HfApiModel(
max_tokens=2096,
temperature=0.5,
model_id='Qwen/Qwen2.5-Coder-32B-Instruct',# it is possible that this model may be overloaded
custom_role_conversions=None,
)



# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[final_answer], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


GradioUI(agent).launch()