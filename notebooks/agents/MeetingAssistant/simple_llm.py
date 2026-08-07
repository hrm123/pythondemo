# from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes  # For specifying model types
# from ibm_watsonx_ai import APIClient, Credentials  # For API client and credentials management
# from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams  # For managing model parameters
# from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods  # For defining decoding methods
from langchain_ibm import WatsonxLLM, WatsonxEmbeddings  # For interacting with IBM's LLM and embeddings
# from ibm_watsonx_ai.foundation_models.utils import get_embedding_model_specs  # For retrieving model specifications
# from ibm_watsonx_ai.foundation_models.utils.enums import EmbeddingTypes  # For specifying types of embeddings
from langchain.chains import LLMChain  # For creating chains of operations with LLMs
from langchain.prompts import PromptTemplate  # For defining prompt templates
from langchain_community.llms import Ollama
'''
parameters = {
    GenParams.DECODING_METHOD: "sample",
    GenParams.MAX_NEW_TOKENS: 512,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.TEMPERATURE: 0.5,
    GenParams.TOP_K: 50,
    GenParams.TOP_P: 1,
}

# Set the new model ID for granite-4-h-small
model_id = 'ibm/granite-4-h-small'

# Define the project ID
project_id = "skills-network"

# Initialize the model with the new model_id
granite_llm = WatsonxLLM(
    model_id=model_id,
    url="https://us-south.ml.cloud.ibm.com",
    project_id=project_id,
    params=parameters,
)

# response = granite_llm.invoke("How to read a book effectively?")
'''
def initialize_ollama_llm(model_id="llama3", base_url="http://localhost:11434"):
    # Create and return an instance of the Ollama with the specified configuration
    return Ollama(
        model=model_id,
        base_url=base_url,
        temperature=0.0
    )

response = initialize_ollama_llm().invoke("How to read a book effectively?")


def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i) < 128)


print(response)
