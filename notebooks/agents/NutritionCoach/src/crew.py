import os
import yaml
import base64
from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.tools import (
    ExtractIngredientsTool, 
    FilterIngredientsTool, 
    DietaryFilterTool,
    NutrientAnalysisTool
)
from src.models import RecipeSuggestionOutput, NutrientAnalysisOutput 

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5vl:7b")
LOCAL_LLM = LLM(model=f"ollama/{OLLAMA_MODEL}", base_url=OLLAMA_BASE_URL)

# Get the absolute path to the config directory
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")

'''
This is the foundational class that defines shared logic, including common agents and tasks. It serves as a base class from which the other specialized crews inherit.
'''
@CrewBase
class BaseNourishBotCrew:
    agents_config_path = os.path.join(CONFIG_DIR, 'agents.yaml')
    tasks_config_path = os.path.join(CONFIG_DIR, 'tasks.yaml')
    
    def __init__(self, image_data, dietary_restrictions: str = None):
        self.image_data = image_data
        self.dietary_restrictions = dietary_restrictions

        with open(self.agents_config_path, 'r') as f:
            self.agents_config = yaml.safe_load(f)
        
        with open(self.tasks_config_path, 'r') as f:
            self.tasks_config = yaml.safe_load(f)

    '''
    Uses ExtractIngredientsTool to identify ingredients from the image.
    Uses FilterIngredientsTool to process the extracted ingredients.
    Delegation is disabled (allow_delegation=False), meaning the agent performs all steps independently.
    '''
    @agent
    def ingredient_detection_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ingredient_detection_agent'],
            tools=[
                ExtractIngredientsTool.extract_ingredient, 
                FilterIngredientsTool.filter_ingredients
            ],
            allow_delegation=False,
            max_iter=5,
            llm=LOCAL_LLM,
            verbose=True
        )


    '''
    Filters ingredients based on user-defined dietary restrictions using DietaryFilterTool.
    Limits the number of iterations (max_iter=10).
    '''
    @agent
    def dietary_filtering_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['dietary_filtering_agent'],
            tools=[DietaryFilterTool.filter_based_on_restrictions],
            allow_delegation=True,
            max_iter=6,
            llm=LOCAL_LLM,
            verbose=True
        )

    '''
    Analyzes the nutrient content (calories, macronutrients, micronutrients) using NutrientAnalysisTool.
    '''
    @agent
    def nutrient_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['nutrient_analysis_agent'],
            tools=[NutrientAnalysisTool.analyze_image],
            allow_delegation=False,
            max_iter=4,
            llm=LOCAL_LLM,
            verbose=True
        )

    '''
    Generates creative recipe ideas using detected and filtered ingredients.
    '''
    @agent
    def recipe_suggestion_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['recipe_suggestion_agent'],
            allow_delegation=False,
            llm=LOCAL_LLM,
            verbose=True
        )

    '''
    Tasks represent individual steps in a workflow. Each task is linked to a specific agent and has a clear description and expected output. Tasks can also depend on the output of previous tasks.
    In the CrewAI framework, the output of a task is encapsulated within the TaskOutput class. This class offers a structured approach to accessing task results, supporting various formats such as raw output, JSON, and Pydantic models.
    By default, the TaskOutput includes only the raw output. However, Pydantic or JSON outputs will be included only if the original Task object is explicitly configured with output_pydantic or output_json, respectively. In this project, we opt for output_json to allow for greater flexibility in manipulating the structure of the output. We will go over defining these custom TaskOutput classes later.
    '''
    @task
    def ingredient_detection_task(self) -> Task:
        task_config = self.tasks_config['ingredient_detection_task']

        return Task(
            description=task_config['description'],
            agent=self.ingredient_detection_agent(),
            expected_output=task_config['expected_output']
        )

    @task
    def dietary_filtering_task(self) -> Task:
        task_config = self.tasks_config['dietary_filtering_task']

        return Task(
            description=task_config['description'],
            agent=self.dietary_filtering_agent(),
            depends_on=['ingredient_detection_task'],
            input_data=lambda outputs: {
                'ingredients': outputs['ingredient_detection_task'],
                'dietary_restrictions': self.dietary_restrictions
            },
            expected_output=task_config['expected_output']
        )

    @task
    def nutrient_analysis_task(self) -> Task:
        task_config = self.tasks_config['nutrient_analysis_task']

        return Task(
            description=task_config['description'],
            agent=self.nutrient_analysis_agent(),
            expected_output=task_config['expected_output'],
            output_json=NutrientAnalysisOutput
        )

    @task
    def recipe_suggestion_task(self) -> Task:
        task_config = self.tasks_config['recipe_suggestion_task']

        return Task(
            description=task_config['description'],
            agent=self.recipe_suggestion_agent(),
            depends_on=['dietary_filtering_task'],
            input_data=lambda outputs: {
                'filtered_ingredients': outputs['dietary_filtering_task']
            },
            expected_output=task_config['expected_output'],
            output_json=RecipeSuggestionOutput
        )


'''
This crew handles the Recipe Workflow, which focuses on:

Detecting ingredients in the uploaded image
Filtering ingredients based on dietary restrictions
Generating personalized recipe suggestions
This workflow is designed for users seeking creative and healthy meal ideas tailored to their dietary preferences.

It defines the Recipe Workflow, which includes the following tasks:
Ingredient Detection Task
Dietary Filtering Task
Recipe Suggestion Task
'''
@CrewBase
class NourishBotRecipeCrew(BaseNourishBotCrew):

    @crew
    def crew(self) -> Crew:
        tasks = [
            self.ingredient_detection_task(),
            self.dietary_filtering_task(),
            self.recipe_suggestion_task()
        ]

        agents = [
            self.ingredient_detection_agent(),
            self.dietary_filtering_agent(),
            self.recipe_suggestion_agent()
        ]

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

'''
This crew handles the Analysis Workflow, which focuses on:

Providing a detailed breakdown of the nutritional content of the food
Evaluating the overall healthiness of the meal
This workflow is ideal for users who want to gain insights into the nutritional value of their meals and make informed dietary choices.
Includes only one task, since the Llama instruct model alone is powerful enough to analyze the image and provide insights:
Nutrient Analysis Task
'''
@CrewBase
class NourishBotAnalysisCrew(BaseNourishBotCrew):

    @crew
    def crew(self) -> Crew:
        tasks = [
            self.nutrient_analysis_task(),
        ]

        agents = [
            self.nutrient_analysis_agent(),
        ]

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
